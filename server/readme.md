# README

## 一、本地使用MySQL配置教程：

### 1.安装MySQL，各个系统要求不同。

Mac下载链接https://dev.mysql.com/downloads/file/?id=471631
Linux可使用指令
```shell
sudo apt-get install mysql-server mysql-client
```
进行安装
注意初始密码的设定
### 2.更改初始密码

Linux上会让你在一开始就设置一个初始密码，直接设为：*arduino* 即可。
Mac需要记录初始密码（也有可能没有初始密码）
输入指令
```shell
mysql -u root -p
```
然后输入密码，进行登录。
### 3.设置mysql用户
进入了mysql之后，输入和运行如下指令
```mysql
create user 'arduino'@'localhost' identified by 'arduino';
#建立用户arduino，在localhost，密码为arduino
```
### 4.创建字符编码为utf-8的库（新）

依次输入和运行如下指令

```mysql
create database arduino_pro character set utf8;
#建立数据库，名字为webproject，并将其字符编码默认设置为utf-8
grant all privileges on webproject.* to 'arduino'@'localhost' identified by 'arduino';
grant all privileges on webproject.* to 'arduino'@'%' identified by 'arduino';
#给数据库授权
flush privileges;
#刷新权限
show databases;
#可显示当前拥有的数据库
show grants for 'arduino'@'localhost';
show grants for 'arduino'@'%';
#可显示myproject的数据库的权限
exit;
#退出
```