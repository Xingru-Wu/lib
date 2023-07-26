import pymysql   #导入模块
def conn():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         database='lib',
                         charset='utf8')
    return db



