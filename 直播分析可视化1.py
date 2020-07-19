# -*- coding: utf-8 -*-
"""
Created on Tue May 26 18:34:46 2020

@author: YangYongbin
"""

import requests
import re
import threading
from queue import Queue
import time
import sys
import os
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


import wordcloud

################################################################################### 需要自动爬取页码范围 

#每页 120 条数据 
PageNum=1


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
urlqueue=Queue()# url队列
rnmutex = threading.Lock()# 创建互斥锁
nnmutex = threading.Lock()
olmutex = threading.Lock()
c2namemutex = threading.Lock()
Lrn_list=[]# 房间名
Lnn_list=[]# 主播名
Lol_list=[]# 热度
Lc2name_list=[]# 分类




def PageNumb():
  
    url='https://www.douyu.com/gapi/rkc/directory/0_0/1'
    r=requests.get(url,headers=headers,timeout=10)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    html=r.text
    reg=re.compile('pgcnt":.*?}')
    pgcnt=re.findall(reg,html)
    pg=str(pgcnt[0])
    num=int(pg[7:-1])
    return num

  



def getHtml(url):
    for i in range(5):
        try:
            r=requests.get(url,headers=headers,timeout=10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
            break
        except:
            print("网络异常！\n尝试重新获取地址 第",i+1,'次 [共5次]')
def textjx(text):
    
    '''
    {"rid":2947432,"rn":"呆妹：好久不见~甚是想念~","uid":85761008,"nn":"呆妹儿小霸王",
    "cid1":1,"cid2":270,"cid3":516,"iv":0,"av":"avatar_v3/201812/da64dbdef534fee78999fe589fe3438f",
    "ol":2765548,"url":"/92000","c2url":"/directory/game/jdqs","c2name":"绝地求生",
    "icdata":{"306":{"url":"","w":0,"h":0},"836":{"url":"","w":0,"h":0},
    "600":{"url":"","w":0,"h":0}},"dot":2106,"subrt":0,"topid":0,"oaid":0,"bid":0,"gldid":0,
    "rs1":"https://rpic.douyucdn.cn/asrpic/200526/2947432_1844.png/dy2",
    "rs16":"https://rpic.douyucdn.cn/asrpic/200526/2947432_1844.png/dy1",
    "utag":[],"rpos":0,"rgrpt":1,"rkic":"","rt":2106,"ot":0,"clis":2,"chanid":0,
    "icv1":[[{"id":836,"url":"https://sta-op.douyucdn.cn/dy-listicon/f118481a9050754749ca8e7567d06deb.png",
    "score":1000,"w":0,"h":0}],
    [{"id":600,"url":"https://sta-op.douyucdn.cn/dy-listicon/a7e875662904c14638c619590a558214.png",
    "score":90,"w":0,"h":0}],[],
    [{"id":306,"url":"https://sta-op.douyucdn.cn/dy-listicon/47b24dcfe308b9630f17e3c70faea1ba.png",
    "score":502,"w":0,"h":0}]],"ioa":1,"od":"绝地年度最佳主播"},
    '''
    
    # 房间名
    rern=re.compile('"rn":".*?"')
    rn_list=re.findall(rern,text)     
    # 主播名
    renn=re.compile('"nn":".*?"')
    nn_list=re.findall(renn,text)     
    # 热度
    reol=re.compile('"ol":.*?"')
    ol_list=re.findall(reol,text)    
    # 分类
    rec2name=re.compile('"c2name":".*?"')
    c2name_list=re.findall(rec2name,text)
    for l in rn_list:
        if rnmutex.acquire(1): 
            Lrn_list.append(str(l)[6:-1])
        rnmutex.release()
        
    for l in nn_list:
        if nnmutex.acquire(1): 
            Lnn_list.append(str(l)[6:-1])
        nnmutex.release()
        
    for l in ol_list:
        if olmutex.acquire(1): 
            Lol_list.append(str(l)[5:-2])
        olmutex.release()
    
    for l in c2name_list:
        if c2namemutex.acquire(1): 
            Lc2name_list.append(str(l)[10:-1])
        c2namemutex.release()
# 生产者生成url队列
def producer():
    for i in range(PageNum):
        url = 'https://www.douyu.com/gapi/rkc/directory/0_0/' + str(i+1)
        
        urlqueue.put(url)
        
        
    # 输出队列测试
    # while not urlqueue.empty():
    #     print (urlqueue.get()) 
# 消费者消耗url队列
def consumer():
    threads=[]              #线程列表
    for i in range(PageNum):
        url=urlqueue.get()
        t = threading.Thread(target=jojo,args=(url,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join(PageNum)
        
# 爬取数据与数据清洗
def jojo(url):
    text=getHtml(url)
    textjx(text)
def mkfile():
    host_data = open("temp.csv", "w+",encoding='utf_8_sig')
    host_data.write("房间名称\t房间类别\t主播名称\t房间热度\n")
    if len(Lrn_list)==len(Lnn_list)==len(Lol_list)==len(Lc2name_list):
        pass
    else:
        print('error')
        time.sleep(10)
        sys.exit(0)
    for i in range(len(Lrn_list)):
        host_data.write(str(Lrn_list[i]) + "\t" + str(Lc2name_list[i]) + "\t" + str(Lnn_list[i]) + "\t" + str(Lol_list[i]) + "\n")
    host_data.close()
    df = pd.read_csv("temp.csv", encoding='utf_8_sig',delimiter="\t")    
    df.to_csv("C:\\Users\\asus-pc\\Desktop\\可视化\\data.csv",encoding="utf_8_sig")
    os.remove('temp.csv')
    
def show():
    df=pd.read_csv("C:\\Users\\asus-pc\\Desktop\\可视化\\data.csv")#读取数据
    #统计直播数最多的主题(房间类别）data.csv
    names=df["主播名称"].value_counts()
    
    heat=df["房间热度"].value_counts()
    
    rclass=df["房间类别"].value_counts()
    # sorted_df = unsorted_df.sort_values(by='col1')
    # print(df.sort_values(by=['房间热度'],ascending=False))
    #排序 by=['房间热度'] 依据热度  ascending=False 是否升序
    # print(type(names))
    # print(names)
    # print(df.loc[1:3])


    

 




    plt.title("直播间数与房间类别") #统计图标题
    plt.rcParams['figure.figsize']=(6.0,4.0)#设置图的尺寸
    plt.rcParams['figure.dpi']=200 #设置分辨率
    # 设置图的字体
    font={
        ##'family' : 'SimHei',
        'weight':'bold',
        'size':'4'
        }

    plt.rc('font',**font)

    plt.ylabel('房间数量') 
    plt.xlabel('直播分类')  
    plt.bar(rclass.index[0:10],rclass.values[0:10],color='aquamarine')
    ##plt.savefig("统计图.png")
    plt.savefig("C:\\Users\\asus-pc\\Desktop\\可视化\\统计图.png")
    plt.show()
    
    
    
def wordc():


    
    
    
    # # 直播分类词云
    wordc = wordcloud.WordCloud(width=1500,height=1000,background_color='white'
                                ,font_path='msyh.ttc')
    wordc.generate(str(Lc2name_list))
    ##wordc.to_file('词云.png')
    wordc.to_file('C:\\Users\\asus-pc\\Desktop\\可视化\\词云.png')
    plt.imshow(wordc, interpolation='bilinear')
    plt.axis("off")
        
    
    
    

def main():
    global PageNum
    PageNum=PageNumb()
    producer()
    consumer()
    mkfile()
    show()
    wordc()
    
    
    
    
    # 测试
    # print(Lrn_list[1])
    # print(Lnn_list[1])    
    # print(Lol_list[1])
    # print(Lc2name_list[1])
    
    # print('\n数据统计：')
    # print('房间名',len(Lrn_list),'条\n主播名',len(Lnn_list),'条\n热度',len(Lol_list),'条\n分类',len(Lc2name_list),'条')
    # print('\n\n#######################################\n##                结束                ##\n#######################################')        
if __name__ == '__main__':
    main()




