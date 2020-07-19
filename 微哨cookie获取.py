from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import csv
cookieslist=[]
namelist=[]
sexlist=[]
classlist=[]
codelist=[]
passwdlist=[]
def load():
	sexclist=[]
	with open('c.csv','r') as csvfile:
		f0 = csv.reader(csvfile, quotechar='|')
		for row in f0:
			namelist.append(row[0])
	with open('c.csv','r') as csvfile:
		f1 = csv.reader(csvfile, quotechar='|')
		for row in f1:
			sexclist.append(row[1])
	with open('c.csv','r') as csvfile:
		f2 = csv.reader(csvfile, quotechar='|')
		for row in f2:
			classlist.append(row[2])
	with open('c.csv','r') as csvfile:
		f3 = csv.reader(csvfile, quotechar='|')
		for row in f3:
			codelist.append(row[3])
	with open('c.csv','r') as csvfile:
		f4 = csv.reader(csvfile, quotechar='|')
		for row in f4:
			passwdlist.append(row[4])
	for s in sexclist:
		if str(s)=="男":
			sexlist.append("boy")
		elif str(s)=="女":
			sexlist.append("girl")
def cook(code,passwd):
	url="http://web.weishao.com.cn/login"
	sel = webdriver.Chrome()  
	sel.get(url)  
	time.sleep(1)
	sel.find_element_by_xpath('''//*[@id="react-select-2--value"]/div[2]/input''').send_keys('四川轻化工大学',Keys.ENTER)
	sel.find_element_by_xpath('''//*[@id="username"]''').send_keys(code)
	sel.find_element_by_xpath('''//*[@id="password"]''').send_keys(passwd)
	sel.find_element_by_xpath('''//*[@id="content"]/div/div[3]/div/div[1]/div[1]/div[3]/form/div[4]/button''').click()
	cookie=sel.get_cookies()
	co=[]
	for item in cookie:
		temp=item["name"]+"="+item["value"]
		co.append(temp)
	cookies = ';'.join(co)
	cookieslist.append(cookies)
	time.sleep(5)
	sel.quit()
def wcsv():
	rows=[]
	headers = "name,sex,class,code,cookie\n"
	f=open('ws.csv','a')
	f.write(headers)
	for j in range(1,len(namelist)):
		t=namelist[j]+','+sexlist[j-1]+','+classlist[j]+","+codelist[j]+','+cookieslist[j-1]+'\n'
		f.write(t)
	f.close()
def main():
	load()
	for i in range(len(codelist)):
		if i!=0:
			cook(codelist[i],passwdlist[i])
	wcsv()
if __name__ == '__main__':
	main()