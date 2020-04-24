#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 19:24:43 2018

@author: Mooncat
"""
import matplotlib
matplotlib.use('Agg')
import datetime
from imgurpython import ImgurClient
client_id = 'd5f8a4196a81f65'
client_secret = 'e81f8633b829bf064dbd0052be6818772580ba03'
album_id = 'mrstock'
access_token = 'd5e3a3f386b3a6f1b5f273dc44f3f3ce98e74973'
refresh_token = '48ec43eaae4edd30908b55992e390223d90de7fe'

###############################################################################
#                              股票機器人 繪圖專區                            #
###############################################################################

def showImgur(fileName):
        # 連接imgur
        client= ImgurClient(client_id, client_secret, access_token, refresh_token)
    
        # 先打好連接需要的參數
        config = {
            # 'album': album_id, # 相簿名稱
            'name': fileName, # 圖片名稱
            'title': fileName, # 圖片標題
            'description': str(datetime.date.today()) # 備註，這邊打日期時間
            }
        
        # 開始上傳檔案
        try:
            print("[log:INFO]Uploading image... ")
            imgurl = client.upload_from_path(fileName+'.png', config=config, anon=False)['link']
            #string to dict
            print("[log:INFO]Done upload. ")
        except :
            # 如果失敗回傳"失敗"這張圖
            imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
            print("[log:ERROR]Unable upload ! ")
            
        
        return imgurl