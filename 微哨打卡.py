import requests
import json
import re

namelist=[]
sexlist=[]
clalist=[]
codelist=[]
cookielist=[]

def getlist():
	f=open("ws.csv","r")
	for line in f.readlines():
		line = line.strip()
		lis=line.split(',')
		namelist.append(lis[0])
		sexlist.append(lis[1])
		clalist.append(lis[2])
		codelist.append(lis[3])
		cookielist.append(lis[4])
	f.close()

def post(i):
	name=namelist[i]
	sext=sexlist[i]
	sex='"'+sext+'"'
	if clalist[i]=='1':
		cla="行政组织架构&0/四川轻化工大学&3/计算机学院&1/网络工程&0/网络20171(卓越)&0"
	elif clalist[i]=='2':
		cla="行政组织架构&0/四川轻化工大学&3/计算机学院&1/网络工程&0/网络20172(卓越)&0"
	code=codelist[i]
	Cookie=cookielist[i]
	headers={'Host': 'ncp.suse.edu.cn',
	'Connection': 'keep-alive',
	'Content-Length': '6175',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
	'Content-Type': 'application/json',
	'Accept': '*/*',
	'Origin': 'http://ncp.suse.edu.cn',
	'Referer': 'http://ncp.suse.edu.cn/questionnaire/addanswer?page_from=onpublic&activityid=82&can_repeat=1',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cookie': Cookie
	}
	datao={"sch_code":"suse","stu_code":code,"stu_name":name,"identity":"student","path":"1001,1009,1119,1722,1725","organization":cla,"gender":sex,"activityid":"82","anonymous":0,"canrepeat":1,"repeat_range":1,"question_data":[{"questionid":987,"optionid":"1794","optiontitle":"已返校","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":996,"optionid":"1816","optiontitle":"在校","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":998,"optionid":"1818","optiontitle":"没有出现症状","question_sort":0,"question_type":2,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":999,"optionid":"1825","optiontitle":"否，身体健康 ","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1000,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"36.1","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1001,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"36.3","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1002,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"36.2","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1003,"optionid":"1830","optiontitle":"是","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'}],"totalArr":[{"questionid":987,"optionid":"1794","optiontitle":"已返校","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":988,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":8,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":989,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":7,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":990,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":991,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":4,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":992,"optionid":"","optiontitle":"","question_sort":0,"question_type":2,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":993,"optionid":"","optiontitle":"","question_sort":0,"question_type":2,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":994,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":995,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":996,"optionid":"1816","optiontitle":"在校","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":997,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":4,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":"","answerid":0,"hide":'true',"answered":'false'},{"questionid":998,"optionid":"1818","optiontitle":"没有出现症状","question_sort":0,"question_type":2,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":999,"optionid":"1825","optiontitle":"否，身体健康 ","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1000,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"36.1","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1001,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"36.3","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1002,"optionid":0,"optiontitle":0,"question_sort":0,"question_type":10,"option_sort":0,"range_value":"","content":"36.2","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'},{"questionid":1003,"optionid":"1830","optiontitle":"是","question_sort":0,"question_type":1,"option_sort":0,"range_value":"","content":"","isotheroption":0,"otheroption_content":"","isanswered":'true',"answerid":0,"answered":'true'}],"private_id":0}
	url='http://ncp.suse.edu.cn/api/questionnaire/questionnaire/addMyAnswer'
	data=json.dumps(datao)
	r=requests.post(url=url,headers=headers,data=data,timeout=10)
	text=r.text
	print(namelist[i])
	print(text)



def main():
	getlist()
	ok=0
	error=0
	for j in range(1,len(namelist)):
		post(j)

if __name__ == '__main__':
	main()