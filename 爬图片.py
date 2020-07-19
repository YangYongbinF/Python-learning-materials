import urllib.request
import re
import requests
import time
import threading
import os
import sys
from queue import Queue

imgurlqueue=Queue(500)
threadLock = threading.Lock()

num=1
errornum=0
listlen=0
urlname=""
threads=[]
testnum=5

# HTML获取
def getHtml(url):
	url=url
	global testnum
	try:
		r=requests.get(url, timeout=10)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		print("获取图片地址列表成功 !\n")
		return r.text

	except:
		print("网络连接异常！\n")
		print("尝试重新获取地址中~")
		if testnum>0:
			testnum=testnum-1
			getHtml(url)
		else:
			print("失败~\n")
			testnum=5
			main()
			return

# HTML解析
def getImg(html):
	global 	listlen
	global imgurlqueue
	global urlname
	print("开始HTML解析。\n")
	reg = 'ess-data=\'.*?\''
	imgre = re.compile(reg)
	imglist = re.findall(imgre, html)
	simglist=str(imglist)
	rreg = 'http.*?.\''
	rimgre = re.compile(rreg)
	rimglist = re.findall(rimgre, simglist)
	listlen=len(rimglist)

	ren = '<h4>.*</h4>'
	rena = re.compile(ren)
	urln = re.findall(rena, html)
	urln=urln[0]
	urlname=urln[4:-10]

	if listlen==0:
		print("\n\n\n**********************")
		print("未得到图片地址")
		print("**********************\n\n\n")
	else:
		print("共",listlen,"个文件！\n")
		print("*****************\n")

	for imgurl in rimglist:
		imgurlqueue.put(imgurl)
	return

# 下载图片
def downloadimg():
	try:
		global urlname
		global listlen
		global num
		global errornum

		imgurl=imgurlqueue.get()
		imgurl=imgurl[:-1]

		n2=imgurl.split('/')
		n2=n2[-1]
		n0=urlname+n2

		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
		request = urllib.request.Request(url=imgurl,headers=headers)
		try:
			f=open(n0,'xb')
			f.close()
			try:
				response = urllib.request.urlopen(request,timeout=30)
				page = response.read()
				f=open(n0,'wb')
				f.write(page)
				f.close()			
			except:
				threadLock.acquire()
				print("共",listlen,"个***第",num,"个：",n0,"\t连接已超时！\n")
				os.remove(n0)
				num+=1
				errornum+=1
				threadLock.release()
				return
			print("共",listlen,"个***第",num,"个：",n0,"\t已爬取成功!\n")
			threadLock.acquire()
			num+=1
			threadLock.release()
		except :
			threadLock.acquire()
			print("共",listlen,"个***第",num,"个：",n0,"\t文件已存在!\n")
			num+=1
			threadLock.release()
	except :
		print("\t下载异常!\n")

# 线程创建
def nthread():
	global listlen
	global threads
	print(listlen,"个线程已成功创建！\n")	
	for i in range(listlen):
		t=threading.Thread(target=downloadimg)
		t.start()
		threads.append(t)


def main():
	htmlurl1=input("[输入 ”0“ 退出]\n输入URL:")
	if htmlurl1=='0':
		time.sleep(2)
		sys.exit(0)
	htmlurl=htmlurl1.replace("htm_mob","htm_data")
	html = getHtml(htmlurl)
	if type(html)!=type('1'):
		return
	listlen=getImg(html)
	nthread()


if __name__ == '__main__':
	while True:
		main()
		for t in threads:
			t.join()
		print('共',listlen,'个，成功下载',num-1-errornum,'个\n')
		num=1
		listlen=0
		urlname=""
		threads=[]
		errornum=0
	