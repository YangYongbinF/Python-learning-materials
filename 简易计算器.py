import time
start=time.perf_counter()
s=input("请输入算式：")
if s.count("+")==1:
	c=s.split("+")
	s1=c[0]
	s2=c[1]
	d=eval(s1)+eval(s2)
	print("\n结果为：{}\n".format(d))
elif s.count("-")==1:
	c=s.split("-")
	s1=c[0]
	s2=c[1]
	d=eval(s1)-eval(s2)
	print("\n结果为：{}\n".format(d))
elif s.count("*")==1:
	c=s.split("*")
	s1=c[0]
	s2=c[1]
	d=eval(s1)*eval(s2)
	print("\n结果为：{}\n".format(d))
elif s.count("/")==1:
	c=s.split("/")
	s1=c[0]
	s2=c[1]
	d=eval(s1)/eval(s2)
	print("\n结果为：{}\n".format(d))
else :
	print("输入格式有误")
ex=eval(input("————按任意 数字键 后按 回车 退出————\n"))
if ex>0:
	stop=time.perf_counter()
	stime=stop-start
	print("\n\n\n=================\n==3秒后自动关闭==\n=================")
	print("程序运行时间:",stime,"秒")
	time.sleep(3)