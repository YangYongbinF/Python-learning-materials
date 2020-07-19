# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 19:15:37 2020

@author: YangYongbin
"""

import requests
import re
import threading
from queue import Queue
import time
import sqlite3




headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
urlqueue=Queue()# url队列
mutex = threading.Lock()# 创建互斥锁

PageNum=1
Lrn_list=[]# 房间名
Lnn_list=[]# 主播名
Lol_list=[]# 热度
Lc2name_list=[]# 分类
Lrid_list=[]# 房间ID



def PageNumb():
    url='https://www.douyu.com/gapi/rkc/directory/0_0/1'
    r=requests.get(url,headers=headers,timeout=10)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    html=r.text
    reg=re.compile('pgcnt":.*?}')
    pgcnt=re.findall(reg,html)
    num=int(str(pgcnt[0])[7:-1])
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
    # 房间id
    rerid=re.compile('"rid":.*?,')
    rid_list=re.findall(rerid,text)  
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
    if mutex.acquire(1): 
        for l in rid_list:
            Lrid_list.append(str(l)[6:-1])
        for l in rn_list:
            Lrn_list.append(str(l)[6:-1])
        for l in nn_list:
            Lnn_list.append(str(l)[6:-1])
        for l in ol_list:
            Lol_list.append(str(l)[5:-2])
        for l in c2name_list:
            Lc2name_list.append(str(l)[10:-1])
    mutex.release()
        
# 生产者
def producer():
    for i in range(PageNum):
        url = 'https://www.douyu.com/gapi/rkc/directory/0_0/' + str(i+1)
        urlqueue.put(url)
    # 输出队列测试
    # while not urlqueue.empty():
    #     print (urlqueue.get()) 
        
# 消费者
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
    
def sql():
     # 数据库存在则连接
    conn = sqlite3.connect('DB.db')
    print('数据库连接成功!\n')
    cursor = conn.cursor()
    conn.commit()
# 将id添加到数据库&查重
    for id in Lrid_list:
        id = str(id)
        str1='INSERT OR IGNORE INTO RNAME (ID)  VALUES ('
        str2=');'
        ex = str1+id+str2       
        cursor.execute(ex)   
        str1='INSERT OR IGNORE INTO NAME (ID)  VALUES ('
        str2=');'
        ex = str1+id+str2
        cursor.execute(ex)
        str1='INSERT OR IGNORE INTO HOT (ID)  VALUES ('
        str2=');'
        ex = str1+id+str2
        cursor.execute(ex)
        str1='INSERT OR IGNORE INTO CLASS (ID)  VALUES ('
        str2=');'
        ex = str1+id+str2
        cursor.execute(ex)
    conn.commit()
    print('将id添加到数据库完成！\n')
    # 时间
    nowtime = time.strftime('T%m%d%H%M',time.localtime(time.time())) 
    nt=str(nowtime)
    print('列名：',nt)
    # 房间名RNAME
    # 添加列 列名为当前时间
    str1='ALTER TABLE RNAME ADD COLUMN '
    str2=' char(50);'
    ex=str1+nt+str2
    cursor.execute(ex)
    conn.commit()
    print('RNAME列添加成功！\n')
    # ALTER TABLE RNAME ADD COLUMN T06160944 char(50);
    # 更新数据
    str1="UPDATE RNAME SET "
    str2=" = '"
    str3="' WHERE ID = "
    str4=";"
    for i in range(len(Lrid_list)):
        Ll=str(Lrn_list[i])
        Ll=Ll.replace("'","?")
        ex=str1+nt+str2+Ll+str3+Lrid_list[i]+str4
        cursor.execute(ex)
    conn.commit()
    print('房间名添加',i,'次\n')
    #UPDATE RNAME SET T06160949 = '娱乐主播 今天又是菜鸡的一天' WHERE ID = 8857459;
    # 主播名 NAME 
    # 添加列 列名为当前时间
    str1='ALTER TABLE NAME ADD COLUMN '
    str2=' char(50);'
    ex=str1+nt+str2
    cursor.execute(ex)
    conn.commit()
    print('NAME列添加成功！\n')
    # ALTER TABLE NAME ADD COLUMN T06160944 char(50);    
    # 更新数据
    str1="UPDATE NAME SET "
    str2=" = '"
    str3="' WHERE ID = "
    str4=";"
    for i in range(len(Lrid_list)):
        Ll=str(Lnn_list[i])
        Ll=Ll.replace("'","?")
        ex=str1+nt+str2+Ll+str3+Lrid_list[i]+str4
        cursor.execute(ex)
    conn.commit()
    print('主播名添加',i,'次\n')
    #UPDATE NAME SET T06161002 = '泰泰Kim' WHERE ID = 8027417;
    # 热度   HOT   
    # 添加列 列名为当前时间
    str1='ALTER TABLE HOT ADD COLUMN '
    str2=' INT;'
    ex=str1+nt+str2
    cursor.execute(ex)
    conn.commit()
    print('HOT列添加成功！\n')
    # ALTER TABLE HOT ADD COLUMN T06160944 INT;    
    # 更新数据
    str1="UPDATE HOT SET "
    str2=" = '"
    str3="' WHERE ID = "
    str4=";"
    for i in range(len(Lrid_list)):
        ex=str1+nt+str2+str(Lol_list[i])+str3+Lrid_list[i]+str4
        cursor.execute(ex)
    conn.commit()
    print('热度添加',i,'次\n')
    #UPDATE HOT SET T06161009 = '302334' WHERE ID = 5051242;
    # 分类 CLASS
    # 添加列 列名为当前时间
    str1='ALTER TABLE CLASS ADD COLUMN '
    str2=' char(20);'
    ex=str1+nt+str2
    cursor.execute(ex)
    conn.commit()
    print('CLASS列添加成功！\n')
    # ALTER TABLE CLASS ADD COLUMN T06160944 INT;    
    # 更新数据
    str1="UPDATE CLASS SET "
    str2=" = '"
    str3="' WHERE ID = "
    str4=";"
    for i in range(len(Lrid_list)):
        Ll=str(Lc2name_list[i])
        Ll=Ll.replace("'","?")
        ex=str1+nt+str2+Ll+str3+Lrid_list[i]+str4
        cursor.execute(ex)
    conn.commit()
    print('分类',i,'次\n')
    # UPDATE CLASS SET T06161012 = '颜值' WHERE ID = 2880941;
    # 关闭数据库连接
    conn.close()


def push():
    ttt=time.strftime('%m月%d日 %H时%M分',time.localtime(time.time()))

    txt='房间名'+str(len(Lrn_list))+'条III主播名'+str(len(Lnn_list))+'条III热度'+str(len(Lol_list))+'条III分类'+str(len(Lc2name_list))+'条III房间号'+str(len(Lrid_list))+'条'

    SCKEY='SCU101893T325ea92d64d0bae1abc1d982f85d34745ee8b5f29ddef'
    api = 'https://sc.ftqq.com/'+SCKEY+'.send'


    data = {"text":ttt+',爬虫运行结束！',
                "desp":txt
                }
    req = requests.post(api,data = data)



def main():
    push()
    global PageNum
    PageNum=PageNumb()
    producer()
    consumer()
    sql()
    push()

    
if __name__ == '__main__':
    main()












    