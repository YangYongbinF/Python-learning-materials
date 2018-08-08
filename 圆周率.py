import time
start=time.perf_counter()
n=10000
p=0
for i in range(n):
	p=(1/pow(16,i))*(4/(8*i+1)-2/(8*i+4)-1/(8*i+5)-1/(8*i+6))+p
print("圆周率约为：{}".format(p))
stop=time.perf_counter()
print("计算用时：{:.3f}秒\n5秒后自动退出".format(stop-start))
time.sleep(5)
