from django.db import models
import datetime
# Create your models here.

class basic_info(models.Model): 
    IDENTITY = (
        ('A', '本科生'),
        ('B', '硕士生'),
        ('C', '博士生'),
    )
    SEX = (
        ('A','男'),
        ('B','女'),
        ('C','不详'),
    )
    name = models.CharField(max_length=10, default="")              #姓名
    department = models.CharField(max_length=10, default="")    #院系
    identifies = models.CharField(max_length=1, choices=IDENTITY, default='A')          #类别
    sex = models.CharField(max_length=1, choices=SEX, default='C')          #性别
    idnumber = models.IntegerField(default=2015000000) #学号


