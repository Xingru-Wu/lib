from PySide2.QtWidgets import QApplication
import gui

# 实例化gui
app = QApplication([])
stats = gui.Hello()
stats.ui.show()
app.exec_()


