import requests
import re
from bs4 import BeautifulSoup
import threading




key=[]

def gethtml(url):
	for i in range(8):
		try:
			headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
			r=requests.get(url, headers=headers,timeout=5)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
			break
		except:
			print('网络连接错误  尝试重新连接[共8次] 第',i+1,'次\n')
        
        

     
def gettag(html,name,urlhead):
    soup = BeautifulSoup(html,'html.parser')
    taglist=soup.find_all('h3',string=re.compile(name))
    rhref='href=.+html'
    rehref=re.compile(rhref)
    urllist=[]
    if len(taglist)>0:
            for i in taglist:
               
                i=str(i)
                href=re.findall(rehref,i) 
                href=str(href)
                url=urlhead+href[8:-2]
                urllist.append(url)
    return urllist

def urlre(urlnew):
     rurlhead='https://.+/'
     reurlhead=re.compile(rurlhead)
     urlhead=re.findall(reurlhead,urlnew)
     
     rurl='https://.+page='
     reurl=re.compile(rurl)
     url=re.findall(reurl,urlnew)
     urlhead=str(urlhead)
     url=str(url)
     urlhead=urlhead[2:-2]
     url=url[2:-2]
     return urlhead,url
     

def start(i,url,urlhead,name):
	print('正在检索第',i+1,'页')         
	url=url+str(i+1)
	html_doc=gethtml(url)
	urllist=gettag(html_doc,name,urlhead)
	print(len(urllist)*'*')
	for i in urllist:
		print(i)
		key.append(i)
     
     
     
def main():
    name=input('输入关键词：')
    lim=eval(input('输入检索范围[1-100]：'))
    urlnew='https://cl*****&page=2'
     
    urlhead,url=urlre(urlnew)
    for i in range(lim):
        t= threading.Thread(target=start(i,url,urlhead,name))
        t.start()


          

    f=open('urllist.txt','w+')
    for i in key:
        i=i+'\n'
        f.write(i)
    f.close()




if __name__ == '__main__':
	main()

