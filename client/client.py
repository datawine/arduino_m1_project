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
my_site_name = ''

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
    try:
        while(True):
            print('Hold on~')
            if check_valid() == SUCCESS:
                print('身份验证，请进！')
    except:
        print('出问题了！')
    else:
        pass
    return False

def create_new():
    name = input("name: ")
    sex = int(input("sex(boy:1, girl:2): "))
    ty = int(input("type: "))
    department = input("department: ")
    ID = int(input("ID: "))
    start_date = input("valid start date: ")
    end_date = input("valid end date: ")
    flag = False
    try:
        flag = create_new_member(name, sex, ty, department, ID, start_date, end_date) 
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('创建成功！')
    elif flag == FAILED:
        print('创建失败！')
    elif flag == CONSTRUCTIONERROR:
        print('创建失败！格式错误！！')
    return True

def create_test():
    flag = False
    try:
        flag = create_new_member('猫鱼', 1, 1, '计算机', 2015011251, "20150901", "20190730")
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('创建成功！')
    elif flag == FAILED:
        print('创建失败！')
    elif flag == CONSTRUCTIONERROR:
        print('创建失败！格式错误！！')
    return True

def clear_card():
    try:
        clear_card_info()
        print('清空成功！')
    except:
        print('出问题了！')
    else:
        pass
    return False

def clear_info():
    try:
        clear_user_info()
        print('开除成功！')
    except:
        print('出问题了！')
    else:
        pass
    return True

def renew_card():
    ID = int(input("ID: "))
    flag = False
    try:
        flag = renew_from_sql(ID)
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('获取成功！')
    elif flag == FAILED:
        print('获取失败！')
    elif flag == CONSTRUCTIONERROR:
        print('获取失败！信息错误！！')
    return True

def refresh_card():
    new_end_date = input("new date: ")
    flag = False
    try:
        flag = refresh_end_date(new_end_date)
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('注册成功！')
    elif flag == FAILED:
        print('注册失败！')
    elif flag == CONSTRUCTIONERROR:
        print('注册失败！信息错误！！')
    return True

def query_info():
    try:
        check_money()
        print('查询成功！')
    except:
        print('出问题了！')
    else:
        pass
    return True
 
def regain_money():
    flag = False
    try:
        flag = regain_money_from_sql()
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('获取成功！且之前的交易记录已丢失！')
    elif flag == FAILED:
        print('获取失败！')
    elif flag == CONSTRUCTIONERROR:
        print('获取失败！信息错误！！')
    return True

def charge_money(site_name):
    number = int(input("How much: "))
    flag = False
    try:
        flag = charge_in_client(number, site_name)
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('充值成功！')
    elif flag == FAILED:
        print('充值失败！')
    elif flag == CONSTRUCTIONERROR:
        print('充值失败！信息错误！！')
    return True

def consume_money(site_name):
    number = int(input("How much: "))
    flag = False
    try:
        flag = consume_in_client(number, site_name)
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('消费成功！')
    elif flag == FAILED:
        print('消费失败！')
    elif flag == CONSTRUCTIONERROR:
        print('消费失败！信息错误！！')
    return True

def get_all_info(site_name):
    flag = False
    try:
        flag = get_info_from_sql(site_name)
    except:
        flag = False
    else:
        pass
    if flag == SUCCESS:
        print('获取成功！')
    elif flag == FAILED:
        print('获取失败！')
    elif flag == CONSTRUCTIONERROR:
        print('获取失败！信息错误！！')
    return False

def add_valid():
    ids = input("Input ID : ")
    id_list = []
    id_list.append(ids)
    flag = add_valid_user(id_list)
    if flag == SUCCESS:
        print('添加成功！')
    elif flag == FAILED:
        print('添加失败！')
    elif flag == CONSTRUCTIONERROR:
        print('添加失败！信息错误！！')
    return False

def delete_valid():
    ids = input("Input ID : ")
    id_list = []
    id_list.append(ids)
    flag = delete_valid_user(id_list)
    if flag == SUCCESS:
        print('删除成功！')
    elif flag == FAILED:
        print('删除失败！')
    elif flag == CONSTRUCTIONERROR:
        print('删除失败！信息错误！！')
    return False

if __name__ == '__main__':
    #test_create()
    #test_get()
    my_site_name = '小卖部一'
    while(True):
        print('choose the mode:')
        print('0.exit')
        print('1.entrance')
        print('2.test_get')
        print('3.create new')
        print('4.create test')
        print('5.clean card')
        print('6.clean info (delete the information in db)')
        print('7.ask for info')
        print('8.refresh the card')
        print('9.query')
        print('10.get money record from server')
        print('11.charge money')
        print('12.consume money')
        print('13.get info from server')
        print('14.add valid users')
        print('15.delete valid users')
        choice = int(input("Choice: "))
        if choice == 0:
            print('Bye bye')
            break
        elif choice == 1:
            print('当做门禁！')
            check_entrance()
        elif choice == 2:
            test_get()
        elif choice == 3:
            print('创建新卡！')
            create_new()
        elif choice == 4:
            print('测试建卡！')
            create_test()
        elif choice == 5:
            print('清除卡片！')
            clear_card()
        elif choice == 6:
            print('清除学籍信息！')
            clear_info()
        elif choice == 7:
            print('获得卡片信息！')
            renew_card()
        elif choice == 8:
            print('注册并延长有效期！')
            refresh_card()
        elif choice == 9:
            print('查询卡内余额和交易记录！')
            query_info()
        elif choice == 10:
            print('挂失获取余额！')
            regain_money()
        elif choice == 11:
            print('充钱！！！')
            charge_money(my_site_name)
        elif choice == 12:
            print('花钱！！！')
            consume_money(my_site_name)
        elif choice == 13:
            print('从服务器申请获取信息！！')
            get_all_info(my_site_name)
        elif choice == 14:
            print('添加新的门禁！')
            add_valid()
        elif choice == 15:
            print('删除旧的门禁！')
            add_valid()
        else:
            break
