# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import json
import Imgur
import datetime


today = datetime.date.today()

def stockSD(stocknumber):
    url = 'http://invest.wessiorfinance.com/Stock_api/Notation_cal?Stock=' + stocknumber + '.TW&Odate=' + str(datetime.date.today()) + '&Period=3.5&is_log=0&is_adjclose=0'
    # 20191105更新，增加header一起進行請求，否則網站不會給你資料
    header = {      
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Connection': 'keep-alive',
            'cookie': '__cfduid=d504aeae9a440cd7203f85f731467be0f1547526562; _ga=GA1.2.451511484.1547526564; __auc=e97f7be41684fc569db1811e5bb; __gads=ID=4550f45ddfb5ca38:T=1547526565:S=ALNI_Ma5zMgCV0epLrUAeQWgeStOkVYDzQ; _atrk_siteuid=yaRu7petUS8Nw1KD; _fbp=fb.1.1549942898388.585175892; dcard=eyJ0b2tlbiI6IjlWemw1b2hZUlJXOTVRSERmY0lFZUE9PSJ9; dcard.sig=H3nXXxV2G3-Sm2MEWknZ7L1HMnY; G_ENABLED_IDPS=google; _fbc=fb.1.1557714992745.IwAR16gXlGLm6soQA_EwUQRKRrD16b5QtbRVST6xjL2TywLrR0LE-Z9OArkV8; cf_clearance=8adf4067ad2681ea1406260fb2c7f0aa0c17f5bf-1559721181-1800-250; dcsrd=uY8fSKpkzGIiUrEQIsr_RgEK; dcsrd.sig=p922Dw18jIm9oh2PPbp_8GgUWWA; _gid=GA1.2.1192734338.1559721495; __asc=d267ae3a16b26a5482a02c9392b; amplitude_id_bfb03c251442ee56c07f655053aba20fdcard.tw=eyJkZXZpY2VJZCI6ImRiMzQ5MGVhLTc4MmUtNDIwZC1hMjkxLWFhYzk3ODMxMjJkYlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU1OTcyMTQ5NTI3OSwibGFzdEV2ZW50VGltZSI6MTU1OTcyMTQ5NTI3OSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9',
            'Host': 'invest.wessiorfinance.com',
            'Referer': 'http://invest.wessiorfinance.com/notation.html',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    list_req = requests.get(url, headers = header)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson=json.loads(soup.text)
    if len(getjson)>0: # 如果資料不到10筆，表示請求失敗
        time=[]  
        theClose=[]
        TL=[]
        TL1=[]
        TL2=[]
        TL3=[]
        TL4=[]
        # 先把所有要畫圖的資料準備好
        for i in range(1,len(getjson),10):
            time.append(getjson[str(i)]['theDate_O'])
            theClose.append(getjson[str(i)]['theClose'])
            TL.append(getjson[str(i)]['TL'])
            TL1.append(getjson[str(i)]['TL']+getjson[str(i)]['STD']*2)
            TL2.append(getjson[str(i)]['TL']+getjson[str(i)]['STD'])
            TL3.append(getjson[str(i)]['TL']-getjson[str(i)]['STD'])
            TL4.append(getjson[str(i)]['TL']-getjson[str(i)]['STD']*2)
           
        ##################### 繪 圖 #####################
        #把文字設定為中文
        plt.plot(time,TL) # 中央平均線
        plt.plot(time,TL1) # 加兩個標準差
        plt.plot(time,TL2) # 加一個標準差
        plt.plot(time,TL3) # 減一個標準差
        plt.plot(time,TL4) # 減兩個標準差
        plt.plot(time,theClose) # 每日的收盤假
        plt.scatter(getjson[str(len(getjson))]['theDate_O'],getjson[str(len(getjson))]['theClose'], marker = 'o', color = 'r', label='5', s = 15) # 最後一天的股價，因為上面for迴圈是用跳的，可能會跳過最後一個點
        plt.text(getjson[str(len(getjson))]['theDate_O'], getjson[str(len(getjson))]['theClose'], '%s' % getjson[str(len(getjson))]['theDate_O']+' price', fontsize=10 ) # 最後一天的點上方的標籤文字
        plt.xticks(fontsize=5,rotation=90) # 設定x軸標籤
        plt.title('Standard Deviation', fontsize=20)
        plt.xlabel("Time (3.5 year)", fontsize=15)
        plt.ylabel("Price", fontsize=15)
        plt.show()
        plt.savefig('showSD.png')
        plt. close() # 殺掉記憶體中的圖片
        #開始利用imgur幫我們存圖片，以便於等等發送到手機
        return Imgur.showImgur('showSD')
    else:
        # 找不到這個股票也回傳"失敗"這張圖
        return 'https://i.imgur.com/RFmkvQX.jpg' 
    

# 股票搜尋
def searchstock(stocknumber):
    url = 'http://invest.wessiorfinance.com/Stock_api/Notation_cal?Stock=' + stocknumber + '.TW&Odate=' + str(datetime.date.today()) + '&Period=3.5&is_log=0&is_adjclose=0'
    # 20191105更新，增加header一起進行請求，否則網站不會給你資料
    header = {      
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Connection': 'keep-alive',
            'cookie': '__cfduid=d504aeae9a440cd7203f85f731467be0f1547526562; _ga=GA1.2.451511484.1547526564; __auc=e97f7be41684fc569db1811e5bb; __gads=ID=4550f45ddfb5ca38:T=1547526565:S=ALNI_Ma5zMgCV0epLrUAeQWgeStOkVYDzQ; _atrk_siteuid=yaRu7petUS8Nw1KD; _fbp=fb.1.1549942898388.585175892; dcard=eyJ0b2tlbiI6IjlWemw1b2hZUlJXOTVRSERmY0lFZUE9PSJ9; dcard.sig=H3nXXxV2G3-Sm2MEWknZ7L1HMnY; G_ENABLED_IDPS=google; _fbc=fb.1.1557714992745.IwAR16gXlGLm6soQA_EwUQRKRrD16b5QtbRVST6xjL2TywLrR0LE-Z9OArkV8; cf_clearance=8adf4067ad2681ea1406260fb2c7f0aa0c17f5bf-1559721181-1800-250; dcsrd=uY8fSKpkzGIiUrEQIsr_RgEK; dcsrd.sig=p922Dw18jIm9oh2PPbp_8GgUWWA; _gid=GA1.2.1192734338.1559721495; __asc=d267ae3a16b26a5482a02c9392b; amplitude_id_bfb03c251442ee56c07f655053aba20fdcard.tw=eyJkZXZpY2VJZCI6ImRiMzQ5MGVhLTc4MmUtNDIwZC1hMjkxLWFhYzk3ODMxMjJkYlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU1OTcyMTQ5NTI3OSwibGFzdEV2ZW50VGltZSI6MTU1OTcyMTQ5NTI3OSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9',
            'Host': 'invest.wessiorfinance.com',
            'Referer': 'http://invest.wessiorfinance.com/notation.html',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    list_req = requests.get(url, headers = header)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson=json.loads(soup.text)
    if len(getjson)>0:
        time = getjson[str(len(getjson))]['theDate_O']
        print('時間 = ' + time)

        theClose = getjson[str(len(getjson))]['theClose']
        print('收盤價 = ' + str(theClose))

        TL = getjson[str(len(getjson))]['TL']
        print('TL = ' + str(TL))

        STD = getjson[str(len(getjson))]['STD']
        print('STD = ' + str(STD))
    
        low="Boss目前此股太貴不建議買"
        if (TL - STD*2) >= theClose:
            low ="Boss這檔股票可以趕快下單"
        elif (TL - STD) >= theClose:
            low ="Boss這檔股票蠻便宜了"
    
        return('收盤價 = ' + str(theClose) + '\n中間價 = ' + str(TL) + '\n線距 = ' + str(STD) + '\n' + low)
    else:
        return('沒有這個股票')


    
