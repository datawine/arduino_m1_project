from django.db import models
import datetime
# Create your models here.

class Basic_info(models.Model): 
    IDENTITY = (
        ('1', '本科生'),
        ('2', '硕士生'),
        ('3', '博士生'),
    )
    SEX = (
        ('1','男'),
        ('2','女'),
        ('3','不详'),
    )
    idnumber = models.IntegerField(default=2015000000, unique=True, db_index=True) #学号
    name = models.CharField(max_length=10, default="")              #姓名
    department = models.CharField(max_length=10, default="")    #院系
    identifies = models.CharField(max_length=1, choices=IDENTITY, default='1')          #类别
    sex = models.CharField(max_length=1, choices=SEX, default='3')          #性别 
    validdate = models.CharField(max_length=17, default="20150101-20190730")  #有效期限
    money = models.IntegerField(default=0)


