#TextProBarV1.py
import time
scale = 100
print("------开始执行------")
start=time.perf_counter()
for i in range (scale + 1) :
	a = '*' * i
	b = '.' * (scale - i)
	c = (i/scale)*100
	print("\r\r{:^3.0f}%[{}->{}]".format(c,a,b),end=" ")
	time.sleep(0.01)
stop=time.perf_counter()
print("\n------执行结果------")
sj=-start+stop
print("运行时间：{:|^20.5f}".format(sj))
time.sleep(3)