from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from state import *
import sys
import os
from PyQt5.QtGui import *

class MainWindow(QWidget):
    def __init__(self,dic):
        super().__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)

        if dic["IE_state"]=='s':
            self.ui.label_4.setText("成功")
            self.ui.label_4.setPalette(pe)
        self.ui.label_10.setText(str(dic["IE_num"]))
        if dic["Chrome_state"]=='s':
            self.ui.label_5.setText("成功")
            self.ui.label_5.setPalette(pe)
        self.ui.label_12.setText(str(dic["Chrome_num"]))
        if(os.path.isfile('./Panel_data.xlsx')):
            self.ui.label_6.setText("成功")
            self.ui.label_6.setPalette(pe)

        os.remove('./state.csv')


def main(dic):
    app=QApplication(sys.argv)
    mainwindow=MainWindow(dic)
    mainwindow.show()
    
    sys.exit(app.exec_())
