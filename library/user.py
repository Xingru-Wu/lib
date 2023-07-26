import connect

db = connect.conn()


# 定义读者类型
class User:
    # 图书查询
    def search(self, bno, cate, title, press, ymin, ymax, author, pmin, pmax):
        try:
            cursor = db.cursor()  # 使用cursor方法创建一个游标对象cursor
            sq = "select bno,category,title,press,year,author,price,total,stock from lib.book where 1=1 "
            if bno != '':
                sq = sq + " and bno='%s'" % bno
            if cate != '':
                sq = sq + " and category='%s'" % cate
            if title != '':
                sq = sq + " and title='%s'" % title
            if press != '':
                sq = sq + " and press='%s'" % press
            if ymin != '':
                ymin = int(ymin)
                sq = sq + " and year>=%d" % ymin
            if ymax != '':
                ymax = int(ymax)
                sq = sq + " and year<=%d" % ymax
            if author != '':
                sq = " and author=%d" % author
            if pmin != '':
                pmin = float(pmin)
                sq = sq + " and price>=%f" % pmin
            if pmax != '':
                pmax = float(pmax)
                sq = sq + " and price<=%f" % pmax
            sq = sq + ";"
            cursor.execute(sq)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(e)

    def rerange(self, arrange2, arrange1, result):
        if len(result) == 0:
            pass
        else:
            if arrange2 == '升序':
                if arrange1 == '书号':
                    result = sorted(result, key=lambda tup: tup[0])
                elif arrange1 == '类型':
                    result = sorted(result, key=lambda tup: tup[1])
                elif arrange1 == '书名':
                    result = sorted(result, key=lambda tup: tup[2])
                elif arrange1 == '出版社':
                    result = sorted(result, key=lambda tup: tup[3])
                elif arrange1 == '年份':
                    result = sorted(result, key=lambda tup: tup[4])
                elif arrange1 == '作者':
                    result = sorted(result, key=lambda tup: tup[5])
                elif arrange1 == '价格':
                    result = sorted(result, key=lambda tup: tup[6])
                elif arrange1 == '总藏书量':
                    result = sorted(result, key=lambda tup: tup[7])
                elif arrange1 == '库存':
                    result = sorted(result, key=lambda tup: tup[8])
            else:
                if arrange1 == '书号':
                    result = sorted(result, key=lambda tup: tup[0], reverse=True)
                elif arrange1 == '类型':
                    result = sorted(result, key=lambda tup: tup[1], reverse=True)
                elif arrange1 == '书名':
                    result = sorted(result, key=lambda tup: tup[2], reverse=True)
                elif arrange1 == '出版社':
                    result = sorted(result, key=lambda tup: tup[3], reverse=True)
                elif arrange1 == '年份':
                    result = sorted(result, key=lambda tup: tup[4], reverse=True)
                elif arrange1 == '作者':
                    result = sorted(result, key=lambda tup: tup[5], reverse=True)
                elif arrange1 == '价格':
                    result = sorted(result, key=lambda tup: tup[6], reverse=True)
                elif arrange1 == '总藏书量':
                    result = sorted(result, key=lambda tup: tup[7], reverse=True)
                elif arrange1 == '库存':
                    result = sorted(result, key=lambda tup: tup[8], reverse=True)
            return result

# w = User()
# re = w.search('123', '', '', '', '', '', '', '', '')
# print(type(re))
