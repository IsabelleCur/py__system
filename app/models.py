from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length = 32)
    nickname = models.CharField(max_length = 32)
    account = models.CharField(max_length = 32, primary_key = True)
    number = models.CharField(max_length = 32)
    gender=models.CharField(max_length = 32)
    birth=models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)
    money=models.CharField(max_length = 32)
    # 上次登录时间
    lastLogDate = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name 


class History(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False)
    newsID = models.CharField(max_length = 64 )
    data = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.data 

class Favorite(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False)
    newsID = models.CharField(max_length = 64)
    data = models.DateField(auto_now_add=True)

    # 根据Favorite card渲染需求添加
    pubDate = models.CharField(max_length=16, default=" ")
    title = models.CharField(max_length = 32, default=" ")
    source = models.CharField(max_length = 16, default=" ")
    content = models.CharField(max_length = 512, default=" ") 
    link = models.CharField(max_length = 512, default=" ")
    havePic = models.BooleanField(default = False)
    imageurls = models.CharField(max_length= 512, default=" ")
    def __str__(self):
        return self.data 
