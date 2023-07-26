from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import admin
from PySide2.examples.widgets.animation.easing.ui_form import Ui_Form
import user


# 主界面~
class Hello(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/hello.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.admin.clicked.connect(self.jumpad)
        self.ui.user.clicked.connect(self.jumpuser)

    def jumpad(self):
        self.stats = Admin_loggin()
        self.stats.ui.show()
        self.ui.close()

    def jumpuser(self):
        self.stats = user_search()
        self.stats.ui.show()
        self.ui.close()


# 管理员登录~
class Admin_loggin(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/ad_loggin.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.login.clicked.connect(self.login)
        self.ui.back.clicked.connect(self.back)

    def back(self):
        self.stats = Hello()
        self.stats.ui.show()
        self.ui.close()

    def login(self):
        account = self.ui.account.text()
        password = self.ui.password.text()
        a = admin.Admin()
        if (a.login(account, password) == "true"):
            self.stats = admin_select()
            self.stats.ui.show()
            self.ui.close()

        else:
            QMessageBox.critical(self.ui, '密码错误', '用户名或密码错误！')
            self.ui.account.clear()
            self.ui.password.clear()


# 查询~
class user_search(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/user_search.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.sub.clicked.connect(self.sub)
        self.ui.back.clicked.connect(self.back)

    def back(self):
        self.stats = Hello()
        self.stats.ui.show()
        self.ui.close()

    def sub(self):
        bno = self.ui.bno.text()
        cate = self.ui.cate.text()
        title = self.ui.title.text()
        press = self.ui.press.text()
        ymax = self.ui.ymax.text()
        ymin = self.ui.ymin.text()
        author = self.ui.author.text()
        pmax = self.ui.pmax.text()
        pmin = self.ui.pmin.text()
        arrange1 = self.ui.arrange1.currentText()
        arrange2 = self.ui.arrange2.currentText()
        us = user.User()
        # 查询
        result = us.search(bno, cate, title, press, ymin, ymax, author, pmin, pmax)
        # 排序
        result = us.rerange(arrange2, arrange1, result)
        # 输出
        for res in result:
            self.ui.res.append(','.join("%s" % i for i in res))


# 管理员操作选择~
class admin_select(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/admin_select.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.addone.clicked.connect(self.addone)
        self.ui.addall.clicked.connect(self.addall)
        self.ui.br.clicked.connect(self.br)
        self.ui.card.clicked.connect(self.card)
        self.ui.back.clicked.connect(self.back)

    def back(self):
        self.stats = Hello()
        self.stats.ui.show()
        self.ui.close()

    def addone(self):
        self.stats = add_one()
        self.stats.ui.show()
        self.ui.close()

    def addall(self):
        self.stats = add_all()
        self.stats.ui.show()
        self.ui.close()

    def br(self):
        self.stats = br()
        self.stats.ui.show()
        self.ui.close()

    def card(self):
        self.stats = card()
        self.stats.ui.show()
        self.ui.close()


# 加一本~
class add_one(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/add_one.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.subm.clicked.connect(self.add)
        self.ui.back.clicked.connect(self.back)

    def back(self):
        self.stats = admin_select()
        self.stats.ui.show()
        self.ui.close()

    def add(self):
        new_bno = self.ui.bno.text()
        new_cate = self.ui.cate.text()
        new_title = self.ui.title.text()
        new_press = self.ui.press.text()
        new_year = self.ui.year.text()
        new_author = self.ui.author.text()
        new_price = self.ui.price.text()
        num = self.ui.num.text()

        ad = admin.Admin()
        rel = ad.add_one(new_bno, new_cate, new_title, new_press, new_year, new_author, new_price, num)
        if type(rel)==type('str'):
            QMessageBox.information(self.ui, rel, rel)
        else:
            QMessageBox.critical(self.ui, '信息有误！', '信息有误！')


# 加多本~
class add_all(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/add_all.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.sub.clicked.connect(self.sub)
        self.ui.back.clicked.connect(self.back)

    def back(self):
        self.stats = admin_select()
        self.stats.ui.show()
        self.ui.close()

    def sub(self):
        str = self.ui.addall.toPlainText()
        ad = admin.Admin()
        rel = ad.add_all(str)
        if rel == 1:
            QMessageBox.information(self.ui, '入库成功!', '入库成功!')


# 修改借书证（约束条件问题）
class card(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/card.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.sub.clicked.connect(self.sub)
        self.ui.back.clicked.connect(self.back)

    def back(self):
        self.stats = admin_select()
        self.stats.ui.show()
        self.ui.close()

    def sub(self):
        sel = self.ui.ad.currentText()
        new_cno = self.ui.cno.text()
        new_cname = self.ui.cname.text()
        new_dept = self.ui.dept.text()
        new_type = self.ui.type.text()
        ad = admin.Admin()
        if sel == "增加借书证":
            rel = ad.add_card(new_cno, new_cname, new_dept, new_type)
        else:
            rel = ad.del_card(new_cno, new_cname, new_dept, new_type)
        QMessageBox.information(self.ui, rel, rel)


# 借还书
class br(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/borrow&return.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.back.clicked.connect(self.back)
        self.ui.query.clicked.connect(self.query)
        self.ui.br.clicked.connect(self.b_r)

    def back(self):
        self.stats = admin_select()
        self.stats.ui.show()
        self.ui.close()

    def query(self):
        cno = self.ui.cno.text()
        ad = admin.Admin()
        result = ad.query(cno)
        self.ui.book.clear()
        for res in result:
            self.ui.book.append(','.join("%s" % i for i in res))

    def b_r(self):
        sel = self.ui.comboBox.currentText()
        cno = self.ui.cno.text()
        bno = self.ui.bno.text()
        ano = self.ui.ano.text()
        ad = admin.Admin()
        if sel == '借书':
            result1 = ad.borrow(bno, cno, ano)
            if result1 == '书籍不存在！':
                QMessageBox.critical(self.ui, '书籍不存在！', '书籍不存在！')
            elif result1 == '借书成功！':
                QMessageBox.information(self.ui, '借书成功！', '借书成功！')
            # 日期字符串的转化
            else:
                QMessageBox.critical(self.ui, '库存不足', '最近还书日期：' + str(result1))
        else:
            result2 = ad.book_return(bno, cno)
            QMessageBox.information(self.ui, result2, result2)


