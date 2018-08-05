#include <SPI.h>
#include <MFRC522.h>
#include <string.h>

constexpr uint8_t RST_PIN = 9;     // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = 10;     // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

MFRC522::MIFARE_Key key;

const byte magic_number = 2018;
const byte date_blockaddr = 4;
const byte stuinfo_block[2] = {5, 6};
const byte money_sum_block = 7;
const byte money_record_block[5] = {8, 9, 10, 11, 12};

byte dataBlock[16];
byte databuffer[18];
byte datasize = sizeof(databuffer);


/**
 * Initialize.
 */
void setup() {
    Serial.begin(9600); // Initialize serial communications with the PC
    while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
    SPI.begin();        // Init SPI bus
    mfrc522.PCD_Init(); // Init MFRC522 card

    // Prepare the key (used both as key A and as key B)
    // using FFFFFFFFFFFFh which is the default at chip delivery from the factory
    for (byte i = 0; i < 6; i++) {
        key.keyByte[i] = 0xFF;
    }

//    print_basic_info();
}

/**
 * Main loop.
 */
void loop() {

    // Look for new cards
    if ( ! mfrc522.PICC_IsNewCardPresent())
        return;

    // Select one of the cards
    if ( ! mfrc522.PICC_ReadCardSerial())
        return;

    /*
    // Show some details of the PICC (that is: the tag/card)
    Serial.print(F("Card UID:"));
    dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
    Serial.println();
    Serial.print(F("PICC type: "));
    MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
    Serial.println(mfrc522.PICC_GetTypeName(piccType));

    // Check for compatibility
    if (    piccType != MFRC522::PICC_TYPE_MIFARE_MINI
        &&  piccType != MFRC522::PICC_TYPE_MIFARE_1K
        &&  piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
        Serial.println(F("This sample only works with MIFARE Classic cards."));
        return;
    }

    byte sector = 1;

    // Show the whole sector as it currently is
    Serial.println(F("Current data in sector:"));
    mfrc522.PICC_DumpMifareClassicSectorToSerial(&(mfrc522.uid), &key, sector);
    Serial.println();

    char s[] = "this is a trap!";

    byte endposi = trans_char_byte(dataBlock, s, 0);

    
    read_block_data(stuinfo_block, databuffer, datasize);
    dump_byte_array(databuffer, 16); 

    write_block_data(stuinfo_block, dataBlock, datasize);
    read_block_data(stuinfo_block, databuffer, datasize);
    dump_byte_array(databuffer, 16); 
    write_check(dataBlock, databuffer);

    // Show the whole sector as it currently is
    Serial.println(F("Current data in sector:"));
    mfrc522.PICC_DumpMifareClassicSectorToSerial(&(mfrc522.uid), &key, sector);
    Serial.println();
    */
    Serial.println(F("Detected Card!"));
    byte current_sector = 100;
    
    
    while (1){
      String readstr;
      while (!Serial.available()) {}
      while (Serial.available()) {
          delay(30);
          if (Serial.available() > 0) {
              char c = Serial.read();
              readstr += c;
          }
      }
      if (readstr.length() > 0) {
        Serial.print(F("Arduino recieved: "));
        //Serial.print(F(readstr.length()));
        if(readstr[0]=='w' && readstr.length() == 21){ //command(1)+' '+index(2)+' '+data(16)
          Serial.println(F("write command "));
          byte blockIndex;
          blockIndex = 10*(readstr[2]-'0')+(readstr[3]-'0');
          if(current_sector != blockIndex/4){
            current_sector = blockIndex/4;
            authentication(current_sector);
          }
          write_block_data(blockIndex, &readstr[5], 16);
          
        }else if(readstr[0]=='r' && readstr.length() == 4){ //command(1) index(2)
          Serial.println(F("read command "));
          byte blockIndex;
          blockIndex = 10*(readstr[2]-'0')+(readstr[3]-'0');
          if(current_sector != blockIndex/4){
            current_sector = blockIndex/4;
            authentication(current_sector);
          }
          read_block_data(blockIndex, databuffer, datasize);
          Serial.print(F("read block ")); Serial.print(blockIndex); Serial.println(F(": "));
          dump_byte_array(databuffer, 16); Serial.println();
          
        }else if(strncmp(readstr.c_str(),"clear",5)==0){
          Serial.print(F("clear")); Serial.println(F(": "));
          
        }else if(strncmp(readstr.c_str(),"close",5)==0){
          Serial.print(F("close commuication")); Serial.println(F(": "));
          break;
        }
      }
    }


    
    // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD
    mfrc522.PCD_StopCrypto1();
    
}

byte trans_char_byte(byte *databuffer, char *s, byte start) {
    int len = strlen(s);

    byte posi = start;
    for (posi = start; posi - start < 16; posi ++)  {
        databuffer[posi - start] = (byte)s[posi];
    }
    
    return posi;
}

void dump_byte_array(byte *databuffer, byte bufferSize) {
    for (byte i = 0; i < bufferSize; i++) {
        Serial.print(databuffer[i] < 0x10 ? " 0" : " ");
        Serial.print(databuffer[i], HEX);
    }
    Serial.println();
    Serial.println();
}

void dump_sector(byte sector) {
    Serial.println(F("Current data in sector:"));
    mfrc522.PICC_DumpMifareClassicSectorToSerial(&(mfrc522.uid), &key, sector);
    Serial.println();
}

void read_block_data(byte blockAddr, byte* databuffer, byte datasize) {
    Serial.print(F("Reading data from block ")); Serial.print(blockAddr);
    Serial.println(F(" ..."));

    MFRC522::StatusCode status;

    status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(blockAddr, databuffer, &datasize);
    if (status != MFRC522::STATUS_OK) {
        Serial.print(F("MIFARE_Read() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
    }
}

void write_block_data(byte blockAddr, byte* _databuffer, byte datasize) {
    Serial.print(F("Writing data into block ")); Serial.print(blockAddr);
    Serial.println(F(" ..."));

    MFRC522::StatusCode status;

    status = (MFRC522::StatusCode) mfrc522.MIFARE_Write(blockAddr, _databuffer, 16);
    if (status != MFRC522::STATUS_OK) {
        Serial.print(F("MIFARE_Write() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
    }
}

void write_check(byte* data_in_pc, byte* data_in_card) {
    Serial.println(F("Checking result..."));
    byte count = 0;
    for (byte i = 0; i < 16; i++) {
        if (data_in_pc[i] == data_in_card[i])
            count++;
    }
    
    Serial.print(F("Number of bytes that match = ")); Serial.println(count);
    if (count == 16) {
        Serial.println(F("Success :-)"));
    } else {
        Serial.println(F("Failure, no match :-("));
    }
    Serial.println();
}

void print_basic_info() {
    Serial.println(F("Scan a MIFARE Classic PICC to demonstrate read and write."));
    Serial.print(F("Using key (for A and B):"));
    dump_byte_array(key.keyByte, MFRC522::MF_KEY_SIZE);
    Serial.println();
}

void authentication(byte sector) {
    MFRC522::StatusCode status;

    byte trailerBlock = sector*4+3;
    // Authenticate using key A
    Serial.println(F("Authenticating using key A..."));
    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        Serial.print(F("PCD_Authenticate() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
    }
    Serial.println(F("Authenticating again using key B..."));
    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_B, trailerBlock, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        Serial.print(F("PCD_Authenticate() failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
    }
}
