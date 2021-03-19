from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from tabs import Ui_Dialog as tabs_Ui
from crawler_main import crawl,INT_crawl


EDCITEM={
    '05':'DSP Unit ID',
    '21':'CHB unit No',
    '32':'Unit ID',
    '33':'Unit ID'
    }
class MainWindow(QWidget,tabs_Ui):
    def __init__(self):
        super().__init__()
        self.ui=tabs_Ui()
        self.ui.setupUi(self)
        self.Warning=QMessageBox()
        #tab1
        self.dic={}
        self.ui.checkBox_5.stateChanged.connect(self.check_SubEntity)
        self.ui.checkBox_6.stateChanged.connect(self.check_SubEntity)
        self.ui.checkBox_8.stateChanged.connect(self.check_SubEntity)
        self.ui.checkBox_10.stateChanged.connect(self.check_SubEntity)

        self.ui.checkBox_7.stateChanged.connect(self.tab1_check_INT)
        self.ui.checkBox_9.stateChanged.connect(self.tab1_check_INT)

        self.ui.pushButton_2.clicked.connect(self.tab1_click_Callback)
        #tab2
        self.dic2={}
        self.ui.comboBox_2.addItems(['ALL','TFT','CF'])
        self.ui.pushButton.clicked.connect(self.tab2_click_Callback)
        self.ui.checkBox.stateChanged.connect(self.BigSmall)
        self.ui.checkBox_2.stateChanged.connect(self.BigSmall)
        
        self.ui.checkBox_3.stateChanged.connect(self.tab2_check_INT)
        self.ui.checkBox_4.stateChanged.connect(self.tab2_check_INT)
    #tab1
    def check_SubEntity(self,state):
        '''
        按下前四個checkBox時的連動機制
        '''
        if state == Qt.Checked:
            if self.sender() == self.ui.checkBox_8:
                cls=["ALL","01","02","03","04"]
                PanelCls=["ALL","CF","TFT"]
                self.ui.checkBox_10.setChecked(False) 
                self.ui.checkBox_5.setChecked(False)
                self.ui.checkBox_6.setChecked(False)
                self.ui.comboBox_4.clear()
                self.ui.comboBox_4.addItems(cls)
                self.ui.comboBox_6.clear()
                self.ui.comboBox_6.addItems(PanelCls)
                self.ui.label_7.setText("DSP Unit ID: ")
                self.dic["Sub"]="05"
            elif self.sender() == self.ui.checkBox_10:
                chb_no=["ALL","01","02","03"]
                self.ui.checkBox_6.setChecked(False) 
                self.ui.checkBox_8.setChecked(False)
                self.ui.checkBox_5.setChecked(False)
                self.ui.comboBox_4.clear()
                self.ui.comboBox_4.addItems(chb_no)
                self.ui.comboBox_6.clear()
                self.ui.comboBox_6.addItems(["TFT"])
                self.ui.label_7.setText("Chamber No: ")
                self.dic["Sub"]="21"
            elif self.sender() == self.ui.checkBox_5:
                cls=["ALL","CF","TFT"]
                self.ui.checkBox_8.setChecked(False) 
                self.ui.checkBox_10.setChecked(False)
                self.ui.checkBox_6.setChecked(False)
                self.ui.comboBox_6.clear()
                self.ui.comboBox_6.addItems(cls)
                self.ui.comboBox_4.clear()
                self.ui.comboBox_4.addItems(["ALL"])
                self.dic["Sub"]="32"
            else:
                cls=["ALL","CF","TFT"]
                self.ui.checkBox_8.setChecked(False)
                self.ui.checkBox_10.setChecked(False)
                self.ui.checkBox_5.setChecked(False)
                self.ui.comboBox_6.clear()
                self.ui.comboBox_6.addItems(cls)
                self.ui.comboBox_4.clear()
                self.ui.comboBox_4.addItems(["ALL"])
                self.dic["Sub"]="33"
        else:
            self.ui.label_7.setText("篩選: ")
            self.ui.comboBox_4.clear()
            self.ui.comboBox_6.clear()
    def tab1_check_INT(self,state):
        '''
        按下後2個check Box的連動機制
        '''
        if state == Qt.Checked:
            if self.sender() == self.ui.checkBox_7:
                cls=["2100","2200"]
                self.ui.checkBox_9.setChecked(False)
                self.ui.comboBox_5.clear()
                self.ui.comboBox_5.addItems(cls)
                self.dic["INT_cls"]="INT_PNLHIS_"
            else:
                cls=["3600","4600"]
                self.ui.checkBox_7.setChecked(False)
                self.ui.comboBox_5.clear()
                self.ui.comboBox_5.addItems(cls)
                self.dic["INT_cls"]="INT_LONHIS_"
        else:
            self.ui.comboBox_5.clear()
    def tab1_click_Callback(self):
        #資料未填寫完整
        if self.ui.comboBox_5.currentText()=="" or self.ui.comboBox_4.currentText()=="":
            self.Warning.setIcon(QMessageBox.Critical)
            self.Warning.setText("Error")
            self.Warning.setInformativeText('資料尚未填寫完整!!!')
            self.Warning.setWindowTitle("Error")
            self.Warning.exec_()
        else:
            self.dic['line']='TPAB'+self.ui.comboBox_7.currentText()+'00'
            self.dic['Sub']='TPAB'+self.ui.comboBox_7.currentText()+self.dic['Sub']
            self.dic['from_date']=str(self.ui.dateTimeEdit.dateTime()).split(',')[0][-4:]+'/'+str(self.ui.dateTimeEdit.dateTime()).split(',')[1][1:].zfill(2)+'/'+str(self.ui.dateTimeEdit.dateTime()).split(',')[2][1:].zfill(2)
            self.dic['from_Hour']=str(self.ui.dateTimeEdit.dateTime()).split(',')[3][1:].zfill(2)
            self.dic['from_Min']=str(self.ui.dateTimeEdit.dateTime())[:-1].split(',')[4][1:].zfill(2)
            self.dic['to_date']=str(self.ui.dateTimeEdit_2.dateTime()).split(',')[0][-4:]+'/'+str(self.ui.dateTimeEdit_2.dateTime()).split(',')[1][1:].zfill(2)+'/'+str(self.ui.dateTimeEdit_2.dateTime()).split(',')[2][1:].zfill(2)
            self.dic['to_Hour']=str(self.ui.dateTimeEdit_2.dateTime()).split(',')[3][1:].zfill(2)
            self.dic['to_Min']=str(self.ui.dateTimeEdit_2.dateTime())[:-1].split(',')[4][1:].zfill(2)
            self.dic['EDCITEM']=EDCITEM[self.dic['Sub'][-2:]]
            self.dic['sub_second']=self.ui.comboBox_4.currentText()
            self.dic['sub_third']=self.ui.comboBox_6.currentText()
            self.dic['spot']=self.ui.comboBox_5.currentText()
            print(self.dic)
            self.close()
            crawl(self.dic)
    #tab2
    def BigSmall(self,state):
        # 由無到有(按鍵都沒被按到被按)
        if state == Qt.Checked:
            if self.sender() == self.ui.checkBox:
                panel_num=["2","6","8","12","18","21","24","36"]
                self.ui.comboBox_87.clear()
                self.ui.comboBox_87.addItems(panel_num)
                self.ui.checkBox_2.setChecked(False)
            elif self.sender() == self.ui.checkBox_2:
                self.ui.checkBox.setChecked(False)
                self.ui.comboBox_87.clear()
    def tab2_check_INT(self,state):
        if state == Qt.Checked:
            if self.sender() == self.ui.checkBox_3:
                cls=["2100","2200"]
                self.ui.checkBox_4.setChecked(False)
                self.ui.comboBox_3.clear()
                self.ui.comboBox_3.addItems(cls)
                self.dic2["INT_cls"]="INT_PNLHIS_"
            else:
                cls=["3600","4600"]
                self.ui.checkBox_3.setChecked(False)
                self.ui.comboBox_3.clear()
                self.ui.comboBox_3.addItems(cls)
                self.dic2["INT_cls"]="INT_LONHIS_"
        else:
            self.ui.comboBox_3.clear()
    def tab2_click_Callback(self):
        Panel_IDs=self.ui.textEdit.toPlainText()
        #資料未填寫完整
        if self.ui.comboBox_3.currentText()=="" or (not self.ui.checkBox.isChecked() and not self.ui.checkBox_2.isChecked()) or len(Panel_IDs)<1:
            self.Warning.setIcon(QMessageBox.Critical)
            self.Warning.setText("Error")
            self.Warning.setInformativeText('資料尚未填寫完整!!!')
            self.Warning.setWindowTitle("Error")
            self.Warning.exec_()
        else:
            panel_num=self.ui.comboBox_87.currentText()
            self.dic2['pnl_cls']=self.ui.comboBox_2.currentText()
            self.dic2['spot']=self.ui.comboBox_3.currentText()
            #Panel_IDs=self.ui.textEdit.toPlainText()
            Panel_IDs=Panel_IDs.replace(" ","")
            Panel_IDs=Panel_IDs.split("\n")
            Panel_IDs=[Panel_ID for Panel_ID in Panel_IDs if len(Panel_ID)==12]
            print(Panel_IDs)
            print(len(Panel_IDs))
            s=''
            if len(Panel_IDs)>0 and panel_num!="":
                for p in Panel_IDs:
                    if self.dic2['pnl_cls']=="ALL":
                        for i in range(1,int(panel_num)+1):
                            s+=(p[:-2]+str(i).zfill(2)+',')
                    elif self.dic2['pnl_cls']=="TFT" and p[0]=="T":
                        for i in range(1,int(panel_num)+1):
                            s+=(p[:-2]+str(i).zfill(2)+',')
                    elif self.dic2['pnl_cls']=="CF" and p[0]=="F":
                        for i in range(1,int(panel_num)+1):
                            s+=(p[:-2]+str(i).zfill(2)+',')
                    else:
                        continue
                self.dic2['txtID']=s
                self.close()
                INT_crawl(self.dic2)
            elif len(Panel_IDs)>0 and panel_num=="":
                for p in Panel_IDs:
                    if self.dic2['pnl_cls']=="ALL":
                        s+=(p+',')
                    elif self.dic2['pnl_cls']=="TFT" and p[0]=="T":
                        for i in range(1,int(panel_num)+1):
                            s+=(p+',')
                    elif self.dic2['pnl_cls']=="CF" and p[0]=="F":
                        for i in range(1,int(panel_num)+1):
                            s+=(p+',')
                    else:
                        continue
                self.dic2['txtID']=s
                self.close()
                INT_crawl(self.dic2)
            else:
                self.Warning.setIcon(QMessageBox.Critical)
                self.Warning.setText("Error")
                self.Warning.setInformativeText('ID Box內找不到ID!!!')
                self.Warning.setWindowTitle("Error")
                self.Warning.exec_()
if __name__=='__main__':
    app=QApplication(sys.argv)
    mainwindow=MainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())
