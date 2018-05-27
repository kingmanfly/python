import pymysql
#创建链接数据库
config = {'host':'127.0.0.1',#默认127.0.0.1
        'port':3306,#默认即为3306
        'user':'root',
        'passwd':'root',
        'database':'mypydb',
        'charset':'utf8'#默认即为utf8
        }
# conn = pymysql.connect(host="127.0.0.1",user="root", passwd="root",charset='utf8')
# conn.query("create database mypydb")
conn1 = pymysql.connect(**config)
# conn1.query("create table mytb(title char(20) not null, keywd char(30))")

cursor = conn1.cursor()
cursor.execute("select * from mytb;")
# cursor.execute("insert into mytb (title,keywd) VALUES ('aaa','bbb');")
conn1.query("insert into mytb(title,keywd) VALUES('eee','fff')")

conn1.commit()
cursor.close()
conn1.close()