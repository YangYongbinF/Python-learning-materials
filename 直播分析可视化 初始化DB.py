import sqlite3


conn = sqlite3.connect('DB.db')
print('数据库创建成功！\n')
cursor = conn.cursor()


cursor.execute('''
                CREATE TABLE RNAME
                (ID INT PRIMARY KEY  NOT NULL );
						 ''')
cursor.execute('''
                CREATE TABLE NAME
                (ID INT PRIMARY KEY  NOT NULL );
						 ''')
cursor.execute('''
                CREATE TABLE HOT
                (ID INT PRIMARY KEY  NOT NULL );
						 ''')
cursor.execute('''
                CREATE TABLE CLASS
                (ID INT PRIMARY KEY  NOT NULL );
						 ''')
print('表创建成功！\n')



# 该方法提交当前的事务。
conn.commit()

# 该方法关闭数据库连接。
conn.close()


print('数据库初始化完成!\n\n\n')