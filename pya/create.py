#coding: utf-8
import sys
import zerorpc

class CreateSystem(object):
    def create_card(self, name, sex, ty, department, ID, start_date, end_date):
        global create
        try:
            string = "name: "+name+"\nsex: "+sex+"\nty: "+ty+"\ndepartment: "+department
            string += "\nID: "+ID+"\nvalid_date: "+start_date+"---"+end_date
            return string
            #info = create(name, int(sex), int(ty), department, int(ID), start_date, end_date)
            #return str(info)
        except Exception as e:
            return 0
    def echo(self, text):
        return text

def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)
    
def main():
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(CreateSystem())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
    operate_end(ser)

