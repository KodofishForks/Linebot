# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import mongodb
import re
import time
from bs4 import BeautifulSoup
import requests
import urllib.parse
from pymongo import MongoClient
import json
import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import Imgur
import Standard_Deviation




app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('SqP1GmH6JZjcIoC4OPj/Ksn3afa5ZXjUL3+Y5N6qPZOQlFr5EgIEKmcqtUFWhkyDu/Awpp9sXi39+5guWYPZgwJ7K0Fvg2cHw0lfhzea7cldlXol3LPiPnwFg5/TQMRr2i1WJablrtC6qq2msrZusQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('e7496ab6e73f55906ea3788a3c85ab39')

line_bot_api.push_message('Uaaccc56dd4dc6e92a4ca00f29bad8ac3', TextSendMessage(text='Boss需要幫忙嗎'))

yourID='Uaaccc56dd4dc6e92a4ca00f29bad8ac3'
Authdb='klas9802'
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)    
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id  # 使用者ID
    usespeak = str(event.message.text)

    if re.match('[0-9]{4}[<>][0-9]', usespeak):  # 先判斷是否是使用者要用來存股票的
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4] + '已經儲存成功'))
        return 0

    elif re.match('刪除[0-9]{4}', usespeak):     # 刪除存在資料庫裡面的股票
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0




################################我的股票########################################
    elif re.match('我的股票',usespeak):
        
        get=mongodb.show_user_stock_fountion()
        msg=''
        
        if len(get) >0:
            for i in get:
                msg += i['stock'] + " " + i['bs'] + " " + str(i['price']) +'\n'
            line_bot_api.push_message(uid, TextSendMessage(msg))
            return 0
        else:
            line_bot_api.push_message(uid, TextSendMessage('沒有資料'))
            return 0
        
################################################################################
      
        
################################標準差分析#######################################
    elif re.match('[0-9]{4}',usespeak): # 如果只有給四個數字就判斷是股票查詢
        mongodb.update_temporary_stock(uid,usespeak)
        line_bot_api.push_message(uid, TextSendMessage('Boss請稍等我正在運算中...'))
        url = 'https://histock.tw/stock/'+usespeak+'/%E5%88%A9%E6%BD%A4%E6%AF%94%E7%8E%87'
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content,"html.parser")
        table = soup.find("table", class_="tb-stock tbBasic")
        data_txt = table.text
        line_bot_api.push_message(yourID, TextSendMessage(data_txt+'\n'))                
                    
        # 推撥標準插圖
        imgurl = Standard_Deviation.stockSD(usespeak)
        line_bot_api.push_message(uid, ImageSendMessage(original_content_url=imgurl, preview_image_url=imgurl))
        line_bot_api.push_message(uid, TextSendMessage(Standard_Deviation.searchstock(usespeak)))
        return 0

################################################################################       
    
################################黃金交叉########################################         
                #########################################
                #          當短期5日線突破20日線          #
                #              股本6億~20億              #
                #########################################    
    elif event.message.text == '黃金交叉':
        line_bot_api.push_message(uid, TextSendMessage('Boss請稍等我正在運算中...'))
        elected=''
        url = 'https://tw.screener.finance.yahoo.net/screener/ws?PickID=100205,100533,100534,100535,100536,100537&f=j&764'
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getjson4=json.loads(soup.text)
        for e in getjson4['items']:
            elected += e['symname']+e['symid']+'\n'
        #print(elected)
        
        if elected != '':
            line_bot_api.push_message(yourID, TextSendMessage(text="黃金交叉選股結果：\n"+ elected))
        else:
            line_bot_api.push_message(yourID, TextSendMessage(text="黃金交叉選股，沒有可以買的股票"))
                
################################################################################

################################黃金交叉學生#####################################
                #########################################
                #          當短期5日線突破20日線          #
                #              股本6億~20億              #
                #             價格在20塊以下             # 
                #########################################
    
    elif event.message.text == '學生選股':
        line_bot_api.push_message(uid, TextSendMessage('Boss請稍等我正在運算中...'))
        elected_student=''
        url = 'https://tw.screener.finance.yahoo.net/screener/ws?PickID=100205,100533,100534,100535,100536,100537&f=j&764'
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getjson=json.loads(soup.text)
        for e in getjson['items']:
            if e['close_price'] < '20':
               elected_student += e['symname']+e['symid']+'\n' 
        #print(elected_student)
        if elected_student != '':
            line_bot_api.push_message(yourID, TextSendMessage(text="學生選股結果：\n"+ elected_student))
        else:
            line_bot_api.push_message(yourID, TextSendMessage(text="學生選股，沒有可以買的股票"))
################################################################################


################################################################################
                ##########################################
                #              外資連續買超6天            #
                #               股本2億~20億             # 
                #########################################
                
    elif event.message.text == '籌碼面選股':
        line_bot_api.push_message(uid, TextSendMessage('Boss請稍等我正在運算中...'))
        elected_chip_analysis=''
        url = 'https://tw.screener.finance.yahoo.net/screener/ws?PickID=465,100533,100534,100535,100536,100537&f=j&47'
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getjson2=json.loads(soup.text)
        for e in getjson2['items']:
            elected_chip_analysis += e['symname']+e['symid']+'\n' 
        #print(elected_student)
        if elected_chip_analysis != '':
            line_bot_api.push_message(yourID, TextSendMessage(text="籌碼面選股結果：\n"+ elected_chip_analysis))
        else:
            line_bot_api.push_message(yourID, TextSendMessage(text="籌碼面選股結果：沒有可以選的股票\n"))


################################################################################



################################################################################
    elif event.message.text == '殖利率選股':
        line_bot_api.push_message(uid, TextSendMessage('Boss請稍等我正在運算中...'))
        elected_Dividend_yield=''
        url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=&selectType=&_=1574844091489'
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getjson3=json.loads(soup.text)
        for e in getjson3['data']:
            if e[2] > '6':
                elected_Dividend_yield += e[0]+' '+e[1]+'\n'
        if elected_Dividend_yield != '':
            line_bot_api.push_message(yourID, TextSendMessage(text="殖利率選股結果：\n"+ elected_Dividend_yield))
        else:
            line_bot_api.push_message(yourID, TextSendMessage(text="殖利率選股結果：沒有可以選的股票\n"))            
################################################################################
 

    elif event.message.text == '呼叫小秘書':
        message = TextSendMessage(text='Boss我能幫你甚麼?')

    else:
        message = TextSendMessage(text='')
    line_bot_api.reply_message(event.reply_token, message)



#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)