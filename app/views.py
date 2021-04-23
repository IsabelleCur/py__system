from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import hashlib
import rsa
# Create your views here.'
from Crypto.Cipher import AES
import base64
import random

# django as back end
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.decorators import action


from app.models import User, Favorite, History, Record
from app.serializer import UserSerializer, FavoriteSerializer, HistorySerializer

# 获取当前时间
import datetime

def rsaEncrypt(par,pubkey):
    # 明文编码格式
    par = par.encode()#K RA RB是string，转成bytes
    # 公钥加密
    crypto = rsa.encrypt(par, pubkey)
    return crypto


# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    #con = content.decode("utf-8")
    return content

class Aescrypt():
    def __init__(self,key,model,iv):
        self.key = self.add_16(key)
        self.model = model
        self.iv = iv

    def add_16(self,par):
        if type(par) == str:
            par = par.encode()
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self,text):
        text = self.add_16(text)
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key,self.model,self.iv) 
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key,self.model) 
        self.encrypt_text = self.aes.encrypt(text)
        return self.encrypt_text

    def aesdecrypt(self,text):
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key,self.model,self.iv) 
        elif self.model == AES.MODE_ECB:
            self.aes = AES.new(self.key,self.model) 
        self.decrypt_text = self.aes.decrypt(text)
        self.decrypt_text = self.decrypt_text.strip(b"\x00")
        return self.decrypt_text

# 将返回所有的用户信息
# 建立一个用户的视图集合
# 实质上会通过不同的http请求做出不同的数据库操作
class UserViewSet(viewsets.ModelViewSet):
    # 所有的用户信息结果
    # order_by('-account')表示desc，不加默认表示asc
    queryset = User.objects.all().order_by('account')
    # serializer的对象
    serializer_class = UserSerializer

    # 接口为 http://127.0.0.1:8000/api/user/login/
    @action(methods = ['post'], detail = False)
    def login(self,request, pk = None):
        account = request.data["params"]["account"]
        password = request.data["params"]["password"]

        sha=hashlib.sha1(password.encode("utf8"))#encrypt password sha1
        password=sha.hexdigest()

        user = User.objects.filter(
            account = account, 
            password = password
        ).first()

        if(user):
            user.lastLogDate = datetime.datetime.now()
            user.save()
            print(datetime.datetime.now())
            return JsonResponse({
                "status":0,
                "mes" : "success",
                "data" : {
                    "userInfo":{
                        "nickname" : user.nickname,
                        "account" : user.account,
                        "balance" : user.balance,
                        "password" : password,
                        "lastLogDate" :  user.lastLogDate
                    }
                }
            })
        else:
            return JsonResponse({
                "status":1,
                "mes" : "fail"
            })

    # 接口为 http://127.0.0.1:8000/api/user/register/
    @action(methods = ['post'], detail = False)
    def register(self,request, pk = None):
        account = request.data["params"]["account"]
        nickname = request.data["params"]["nickname"]
        password = request.data["params"]["password"]
        name = request.data["params"]["name"]
        number = request.data["params"]["number"]
        gender = request.data["params"]["gender"]
        birth = request.data["params"]["birth"]

        sha=hashlib.sha1(password.encode("utf8"))#encrypt password sha1
        password=sha.hexdigest()#w=hash(password)

    

        user = User.objects.filter(account = account).first()
        print(user == None)
        try:
            # 系统总没有该用户，则注册成功
            if(user == None):
                User.objects.create(
                    account = account,
                    nickname = nickname,
                    password = password,
                    name = name,
                    number = number,
                    gender = gender,
                    birth = birth,
                    
                )
                print(user.balance)
                return JsonResponse({
                    "status" : 0,
                    "mes" : "success",
                    "data" : {
                        "userInfo" : {
                            "nickname" : user.nickname,
                            "account" : user.account,
                            "balance" : user.balance,
                            "password" : password,
                            "lastLogDate" :  user.lastLogDate
                        }
                    }
                })
            else:
                return JsonResponse({
                    "status":1,
                    "mes" : "user account exists"
                })
        except:
            # 注册失败
            return JsonResponse({
                "status":1,
                "mes" : "fail"
            })
    
    # 接口为 http://127.0.0.1:8000/api/user/changeNickname/
    @action(methods = ['post'], detail = False)
    def changeNickname(self,request, pk = None):
        account = request.data["params"]["account"]
        nickname = request.data["params"]["nickname"]
        try:
            User.objects.filter(account = account).update(nickname = nickname)
            # 系统总没有该用户，则注册成功
            return JsonResponse({
                "status" : 0,
                "mes" : "success",
                "data" : {
                    "userInfo" : {
                        "account" : account,
                        "nickname" : nickname,
                        "balance" : user.balance,
                        "password" : password,
                    }
                }
            })
        except:
            # 注册失败
            return JsonResponse({
                "status":1,
                "mes" : "fail"
            })

    # 接口为 http://127.0.0.1:8000/api/user/changePassword/
    @action(methods = ['post'], detail = False)
    def changePassword(self,request, pk = None):
        account = request.data["params"]["account"]
        password = request.data["params"]["password"]
        try:
            User.objects.filter(account = account).update(password = password)
            # 系统总没有该用户，则注册成功
            return JsonResponse({
                "status" : 0,
                "mes" : "success",
            })
        except:
            # 注册失败
            return JsonResponse({
                "status":1,
                "mes" : "fail"
            })

    # 接口为 http://127.0.0.1:8000/api/user/changeBalance/
    @action(methods = ['post'], detail = False)
    def changeBalance(self,request, pk = None):
        account = request.data["params"]["account"]
        balance = request.data["params"]["balance"]
        user = User.objects.filter(account = account).first()
        #price = user.balance-balance
        password=user.password

        (pubkey, privkey) = rsa.newkeys(1024)
        # 生成公钥
        pub = pubkey.save_pkcs1()
        # 生成私钥
        pri = privkey.save_pkcs1()
        text=pub

        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (b'\00'*add)

        key=password#key=password=w=hash(password)
        key=key[:16]
        print("key=",key)
        iv = '1234567812345678'

        aescryptor = Aescrypt(key,AES.MODE_CBC,iv)
        #print(aescryptor.key)
        en_text = aescryptor.aesencrypt(text)#text, en_text, de_text都与pubkey有关
        de_text = aescryptor.aesdecrypt(en_text)#都是byte格式 

        Rlist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
       '1','2','3','4','5','6','7','8','9','0',
       'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
       ',','.','_','-','?','!','@','#','$','%','^','&','*','(',')']
        #K,RA,RB are string
        K=""
        n=random.sample(Rlist, 16)
        for i in n:
            K=K+i
        print("K=",K)

        RA=""
        n=random.sample(Rlist, 16)
        for i in n:
            RA=RA+i
        print("RA=",RA)

        RB=""
        n=random.sample(Rlist, 16)
        for i in n:
            RB=RB+i
        print("RB=",RB)

        #B->A: Encw(PKE(K))
        RSAK=rsaEncrypt(K,pubkey)#秘文， bytes
        aK = Aescrypt(key,AES.MODE_CBC,iv)#W as key
        en_K = aK.aesencrypt(RSAK)#encrypt PKE(K)

        #A->B: Enck(RA)
        de_RSAK = aK.aesdecrypt(en_K)#decrypted_RSAK
        K_de_private=rsaDecrypt(de_RSAK, privkey)#decrypted_K
        print("de_K=",K_de_private)
        aRA = Aescrypt(K_de_private,AES.MODE_CBC,iv)#decrypted_K as key
        en_RA = aRA.aesencrypt(RA)#encrypt RA

        #B->A: Enck(RA,RB)
        de_RA = aRA.aesdecrypt(en_RA)
        print("de_RA=",de_RA)
        RARB=de_RA.decode("utf-8")+RB
        print("RARB",RARB)
        aRARB = Aescrypt(K,AES.MODE_CBC,iv)
        en_RARB=aRARB.aesencrypt(RARB)

        #A->B: Enck(RB)
        de_RARB=aRARB.aesdecrypt(en_RARB)
        print("de_RARB",de_RARB)
        de_RARB_RB=de_RARB[16:32]
        aRB = Aescrypt(K_de_private,AES.MODE_CBC,iv)
        en_RB = aRB.aesencrypt(de_RARB_RB)

        #B: Deck(text)
        de_RB=aRB.aesdecrypt(en_RB)
        print(de_RB.decode("utf-8")==RB)
        print(de_RB)
        print(RB)

        ID =""
        n=random.sample(Rlist, 16)
        for i in n:
            ID=ID+i
        record = Record.objects.filter(ID = ID).first()
        print(record == None)
        try:
            User.objects.filter(account = account).update(balance = balance)
            return JsonResponse({
                    "status":0,
                    "mes" : "success",
                    
                })
        except:
            # 注册失败
            return JsonResponse({
                "status":1,
                "mes" : "fail"
            })
        
    

# 用户收藏视图集
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    # 用户收藏了一条新闻
    def create(self, request, *args, **kwargs):
        print('create')
        try:
        
            account = request.query_params.dict()["account"]
            newsID = request.query_params.dict()["newsID"]
            pubDate = request.query_params.dict()["pubDate"]
            title =request.query_params.dict()["title"]
            source = request.query_params.dict()["source"]
            content =request.query_params.dict()["content"]
            link = request.query_params.dict()["link"]
            imageurls = request.query_params.dict()["imageurls"]
            havePic = request.query_params.dict()["havePic"]
            # 由于收藏新闻数据外码依赖与user 故需要先获取user 
            # 这里使用get 而不是filter 返回的是一个结果而不是一个结果集合
            user = User.objects.get(account = account)
            # js和python 语法问题
            if(havePic == 'false'):
                havePic = False
            else:
                havePic = True
            # 防止重复收藏
            # 表没有见好。。
            favorite = Favorite.objects.filter(user = user, newsID = newsID).first()
            
            if(favorite == None): # 如果没有这条记录
                newRecord = Favorite.objects.create(
                    user = user,
                    newsID = newsID,
                    pubDate = pubDate,
                    title = title,
                    source = source,
                    content = content,
                    link = link,
                    havePic = havePic,
                    imageurls = imageurls
                )
                print("1111111111111111111111111111111111111111111111111")

                newRecord.save()
                print("1111111111111111111111111111111111111111111111111")

                return JsonResponse({
                    "status":0,
                    "mes" : "success",
                    "data" : {
                        "id": newRecord.id,
                        "newsID" : newRecord.newsID,
                    }
                })
            else:
                return JsonResponse({
                    "status":1,
                    "mes" : "重复收藏！",
                })
        except:
            return JsonResponse({
                "status":1,
                "mes" : "fail",
            })

    # 用户删除了一条新闻
    def delete(self, request, *args, **kwargs):
        print("delete")
        try:
            print(request.query_params.dict())
            id = request.query_params.dict()["id"]
            Favorite.objects.filter(id = id).delete()
            return JsonResponse({
                "status":0,
                "mes" : "success",
            })
        except:
            return JsonResponse({
                "status":1,
                "mes" : "fail",
            })

    # 传入用户account，返回所有的收藏新闻的数据
    def list(self, request, pk=None):
        print("list")
        try:
            account = request.query_params.dict()["account"]
            # 由于存在外码依赖 需要先获取依赖的user,
            user = User.objects.filter(account = account).first()
            favorite = Favorite.objects.filter(user = user)
            favorite_s = FavoriteSerializer(favorite, many=True)

            # print(favorite_s.data)
            return JsonResponse({
                "status":0,
                "mes" : "success",
                "data" : {
                    "newsList" : favorite_s.data
                }
            })
        except:
            return JsonResponse({
                "status":1,
                "mes" : "fail",
            })
       


# 用户浏览历史记录视图集
class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

        # 用户浏览了一条新闻
    def create(self, request, *args, **kwargs):
        account = request.data["params"]["account"]
        newsID = request.data["params"]["newsID"]
        try:
            newRecord = History(
                account= account,
                newsID = newsID,
            )
            newRecord.save()
            return JsonResponse({
                "status":0,
                "mes" : "success",
                "data" : {
                    "id": newRecord.id
                }
            })
        except:
            return JsonResponse({
                    "status":1,
                    "mes" : "fail",
                })

    # 用户删除了一条历史记录
    def delete(self, request, *args, **kwargs):
        ids = request.data["params"]["id"]
        try:
            for id in ids:
                History.objects.get(id = id).delete()
            return JsonResponse({
                "status":0,
                "mes" : "success",
            })
        except:
            return JsonResponse({
                    "status":1,
                    "mes" : "fail",
                })
       
    # 传入用户account，返回所有的历史浏览新闻数据
    def list(self, request, pk=None):
        try:
            # account = request.data["params"]["account"]
            account = 11
            history = History.objects.filter(account = account).all()
            history_s = HistorySerializer(history, many=True)
            return JsonResponse({
                "status":0,
                "mes" : "success",
                "data" : history_s.data
            })
        except:
            return JsonResponse({
                    "status":1,
                    "mes" : "fail",
                })