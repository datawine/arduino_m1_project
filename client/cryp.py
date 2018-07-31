from Crypto.Cipher import AES

class AEScrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        byte_text = bytes([ord(i) for i in text])
        byte_text = byte_text + (b'\0' * (16-len(byte_text)))
        byte_ciphertext = cryptor.encrypt(byte_text)
        self.ciphertext = "".join([chr(int(i)) for i in byte_ciphertext])
        return self.ciphertext

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        byte_text = bytes([ord(i) for i in text])
        byte_plain_text = cryptor.decrypt(byte_text)
        plain_text = "".join([chr(int(i)) for i in byte_plain_text])
        return plain_text

if __name__ == '__main__':
    text = 'jiuchuisidamaoyu'
    print(text)
    key = 'miaomiaomiaomiao'
    ac = AEScrypt(key)
    cipher = ac.encrypt(text)
    print(cipher)
    text_de = ac.decrypt(cipher)
    print(text_de)