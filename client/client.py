import requests
from tool import *
from check import *

SERVER = '127.0.0.1' #主机IP  
PORT = '8000' #端口号
# START = '^MyP 1.0' 
# START2 = '^MyP 1.0' 
# START3 = '[^st]' 
# BUFLEN = 1024 
# USER_list = ['user01', 'user02']
url = 'http://' + SERVER + ':' + PORT + '/testdb'

def test_create():
    url = 'http://' + SERVER + ':' + PORT + '/testdb'
    #req = urllib.request.urlopen(url)
    res=requests.get(url)
    req = res.text
    req = req[3:-4]
    print(req)

def test_get():
    name = 'chuimaoyu'
    data = {'username':name}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    print('good')

def test_post():
    name = 'chuimaoyu'
    data = {'username':name}
    res=requests.post(url,data=data)
    # req = res.text
    # req = req[3:-4]
    print(res.text)
    print('good')

def check_entrance():
    while(True):
        print('Hold on~')
        if check_valid():
            print('身份验证，请进！')
    return False
 
if __name__ == '__main__':
    #test_create()
    #test_get()
    while(True):
        print('choose the mode:')
        print('0.exit')
        print('1.entrance')
        print('2.test_get')
        choice = int(input("Choice: "))
        if choice == 0:
            print('Bye bye')
            break
        elif choice == 1:
            print('当做门禁！')
            check_entrance()
        elif choice == 2:
            test_get()
        else:
            break
