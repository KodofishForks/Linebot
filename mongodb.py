# -*- coding: utf-8 -*-

import time
import datetime
from bs4 import BeautifulSoup
import requests
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import urllib.parse
from pymongo import MongoClient


# Authentication Database認證資料庫
Authdb='klas9802'

##### 資料庫連接 #####
def constructor():
    client = MongoClient('mongodb://klas9802:klas9804@cluster0-shard-00-00-ho5sj.azure.mongodb.net:27017,cluster0-shard-00-01-ho5sj.azure.mongodb.net:27017,cluster0-shard-00-02-ho5sj.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client[Authdb]
    return db
   
#----------------------------儲存使用者的股票--------------------------
def write_user_stock_fountion(stock, bs, price):  
    db=constructor()
    collect = db['mystock']
    collect.insert({"stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })
    
#----------------------------殺掉使用者的股票--------------------------
def delete_user_stock_fountion(stock):  
    db=constructor()
    collect = db['mystock']
    collect.remove({"stock": stock})
    

#----------------------------抓取使用者的股票--------------------------
def show_user_stock_fountion():  
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"data": 'care_stock'}))

    return cel

#----------------------------抓暫存的股票名稱--------------------------
def cache_temporary_stock(uid):  
    db=constructor()
    collect = db['member']
    cel=list(collect.find({"uid": uid}))

    return cel[0]['temporary_stock']

#----------------------------存取暫存的股票名稱--------------------------
def update_temporary_stock(uid,stock):
    db=constructor()
    collect = db['member']
    collect.update({ "uid": uid }, {'$set': {'temporary_stock':stock}})



