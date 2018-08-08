try:
	h,w=eval(input("请输入身高（米）和体重（公斤）：\n【用逗号隔开】\n"))
except ZeroDivisionError:
	print("输入错误")
except :
	print("输入格式错误")
else:
	bmi = w / (h**2)
	if bmi < 18.5 :
		print("国际BMI：偏瘦\n国内BMI：偏瘦\n")
	elif bmi< 24 :
		print("国际BMI：正常\n国内BMI：正常\n")
	elif bmi< 25 :
		print("国际BMI：正常\n国内BMI：偏胖\n")
	elif bmi< 28 :
		print("国际BMI：偏胖\n国内BMI：偏胖\n")
	elif bmi< 30 :
		print("国际BMI：偏胖\n国内BMI：肥胖\n")
	else :
		print("国际BMI：肥胖\n国内BMI：肥胖\n")
	print("BMI为：{}".format(bmi))
finally:
	print("\n5秒后自动关闭\n")
	import time
	time.sleep(5)
	