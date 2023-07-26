import datetime
import connect

db = connect.conn()


# 定义管理员类型，其中包括图书入库，借书、还书、借书证管理等实例方法
class Admin:
    # 登录~
    def login(self, name, password):
        cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
        sql = "select * from administrator where ano = '%s' and password = '%s'" % (name, password)
        cursor.execute(sql)  # 执行语句
        results = cursor.fetchall()  # 获得所有记录的列表
        if len(results) == 0:  # 判断数组是否为空
            return "false"
        else:
            return "true"

    def query(self, cno):
        cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
        try:
            # 查询用户未还的全部书籍
            sql = '''select book.bno,book.category,book.title,book.press,book.year,book.author,book.price,book.total,stock
                     from book natural join borrow 
                     where borrow.cno = '%s' and return_date is null;''' % cno
            cursor.execute(sql)  # 执行语句
            results = cursor.fetchall()  # 获得所有记录的列表
            return results
        except Exception as e:
            db.rollback()
            print('查询错误！\n')
            return e

    # 借书
    def borrow(self, bno, cno, ano):
        try:
            cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
            sql1 = '''select stock
                      from book
                      where bno = '%s';''' % bno
            cursor.execute(sql1)  # 执行语句
            result = cursor.fetchone()  # 获得单条数据
            if len(result) == 0:
                return '书籍不存在！'
            # 库存不足
            elif result[0] == 0:
                # 从该书未还记录中找到最早借书的日期，加上30天后得到预计最早还书时间
                sql2 = '''select min(borrow_date)
                          from borrow
                          where bno='%s' and return_date is null;''' % bno
                try:
                    cursor.execute(sql2)
                    results = cursor.fetchone()
                    # 无历史借书记录，库存不能为0
                    mr_time = results[0]
                    # 预计还书时间，预计借书日期为30天
                    mr_time = (mr_time + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
                    return str(mr_time)
                except Exception as e:
                    print(e)
            # 库存充足
            else:
                b_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # r_time = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
                sql3 = '''update lib.book
                          set stock=stock-1
                          where bno=%s;'''  # 更新库存
                sql4 = '''insert into lib.borrow
                          values
                          (%s, %s, %s, null, %s);'''  # 插入borrow表数据,还书日期设为null值
                try:
                    cursor.execute(sql4, (bno, cno, b_time, ano))  # 执行语句
                    cursor.execute(sql3, bno)
                    db.commit()
                    return '借书成功！'
                except Exception as e:
                    db.rollback()
                    print(e)
        except Exception as e:
            db.rollback()
            print(e)

    # 还书
    def book_return(self, bno, cno):
        try:
            result = self.query(cno)
            cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
            r_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if len(result) == 0:
                return '该图书未在用户已借书列表内！'
            else:
                # 更新还书时间，若重复借书，则归还最早借出的那本
                sql = '''update lib.borrow as a
                         set a.return_date = %s
                         where a.bno=%s and a.cno=%s and a.return_date is null and a.borrow_date in 
                         (select min from 
                         (select min(borrow_date) as min from lib.borrow as b where b.bno=%s and b.cno=%s and b.return_date is null) as c);'''
                cursor.execute(sql, (r_time, bno, cno, bno, cno))
                # 更新库存
                sql = '''update lib.book
                         set stock=stock+1
                         where bno=%s;'''
                cursor.execute(sql, bno)
                db.commit()
                return '还书成功！'
        except Exception as e:
            db.rollback()
            return e

    # 单本入库~
    def add_one(self, new_bno, new_cate, new_title, new_press, new_year, new_author, new_price, num):
        # 类型转换
        if new_year != '' and new_price != '' and num != '' and new_bno != '' and new_title != '':
            new_year = int(new_year)
            new_price = float(new_price)
            num = int(num)
            cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
            sql = 'SELECT bno,category,title,press,year,author,price FROM lib.book;'
            cursor.execute(sql)
            result = cursor.fetchall()
            flag = 0
            # 判断该书是否已在库中
            for x in result:
                if (new_bno, new_cate, new_title, new_press, new_year, new_author, new_price) == x:
                    flag = 1  # 在库中
                    try:
                        # 更新库存和藏书
                        sql1 = "update lib.book set stock = stock + %d where bno = '%s';" % (num, new_bno)
                        sql2 = "update lib.book set total = total + %d where bno = '%s';" % (num, new_bno)
                        cursor.execute(sql1)
                        cursor.execute(sql2)
                        db.commit()
                        return '库存修改成功!'
                    except Exception as e:
                        db.rollback()
                        return e
                else:
                    pass
            if flag == 0:  # 不在库中
                try:
                    sql = 'insert into book values("%s","%s","%s","%s","%d","%s","%f","%d","%d")' \
                          % (new_bno, new_cate, new_title, new_press, new_year, new_author, new_price, num, num)
                    cursor.execute(sql)
                    db.commit()
                    return '入库成功！'
                except Exception as e:
                    db.rollback()
                    return e

    # 批量入库
    def add_all(self, str):
        if str != '':
            try:
                # 用回车分隔两条记录
                str_tup = str.split(sep="\n")
                for rec in str_tup:
                    if rec != '':
                        rec_list = rec.split(sep=",")
                        # 首尾去掉括号
                        rel = self.add_one(rec_list[0][1:], rec_list[1], rec_list[2], rec_list[3], rec_list[4],
                                         rec_list[5], rec_list[6], rec_list[7][0:-1])
                        # print(rel)
                return 1
            except Exception as e:
                return e

    # 添加卡号
    def add_card(self, new_cno, new_cname, new_dept, new_type):
        if new_cno=='' or new_type=='' or new_dept=='' or new_cname=='':
            return '请完善信息！'
        else:
            new_type = int(new_type)  # 类型转换
            try:
                cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
                sql = "select * from card where cno=%s;" % new_cno
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result) != 0:
                    return "卡号已存在！"
                else:
                    sql = 'insert into lib.card values("%s","%s","%s","%d")' % (new_cno, new_cname, new_dept, new_type)
                    cursor.execute(sql)
                    db.commit()
                    return '添加成功！'
            except Exception as e:
                db.rollback()
                return e

    # 删除卡号~
    def del_card(self, cno, cname, dept, type):
        type = int(type)
        cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
        try:
            results = self.query(cno)
            # 判断借书记录是否为空,不存在未还书时才可删除卡号
            if len(results) == 0:
                sql2 = "select cno from lib.card where cno = '%s' and cname ='%s' and department='%s' and type= %d" % (
                    cno, cname, dept, type)
                cursor.execute(sql2)
                result = cursor.fetchone()
                if len(result) == 0:
                    return "借书证不存在"
                else:
                    sql1 = "delete from borrow where cno='%s'" % cno
                    cursor.execute(sql1)
                    sql = "delete from lib.card where cno='%s'" % cno
                    cursor.execute(sql)
                    db.commit()
                    return "删除成功"
            else:
                return "该账户存在未还书籍，无法删除！"
        except Exception as e:
            db.rollback()
            return e


# 测试
# ad = Admin()
# ad.add_all('''(20200001,history,世界历史,安徽文艺出版社,2009,马健,46.8,30)\n
# (20200030,computer,数据库系统原理教程,清华大学出版社,1998,王珊,18.5,20)\n
# (20201005,Mathematics,概率论与数理统计,高等教育出版社,2010,盛骤,41.8,30)\n
# (20203001,computer,MYSQL必知必会,人民邮电出版社,2009,刘晓霞,39.0,25)\n
# (20200304,music,勋伯格和声学,上海音乐出版社,2007,阿诺德·勋伯格,28.0,15)''')

# a = ad.borrow('123', '1', '1')
# b=ad.book_return('123','1')
# print(b)
