from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from TimeCharyUI import Ui_Dialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mtick

df=pd.read_excel('Panel_data.xlsx',sheet_name='INT',engine='openpyxl',usecols='B,H,I')
dic_INT=df.set_index('PANELID').T.to_dict('list')
all_loss_code=[]
all_grade=[]
for grade,loss_code in dic_INT.values():
    all_loss_code.append(loss_code)
    all_grade.append(grade)
all_loss_code=[code for code in list(set(all_loss_code)) if str(code)!='nan']
all_grade=[g for g in list(set(all_grade)) if str(g)!='nan']
class MainWindow(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(['ALL']+sorted(all_loss_code))
        self.ui.comboBox_2.addItems(['ALL']+sorted(all_grade))
        self.ui.pushButton.clicked.connect(self.click_Callback)
    def click_Callback(self):
        global dic_INT
        df=pd.read_excel('Panel_data.xlsx',sheet_name='EDCX',engine='openpyxl',usecols='A,B,C')
        # ID:製造日期
        dic_EDCX=df.set_index('GLASS_ID').T.to_dict('list')
        bar_dic1={}
        for (k,v) in dic_EDCX.items():
            try:
                if v[1][0]=="S":
                    bar_dic1[str(v[0])[4:10]]+=2
                elif v[1][0]=="L":
                    bar_dic1[str(v[0])[4:10]]+=18
                elif v[1][0]=="J":
                    bar_dic1[str(v[0])[4:10]]+=24
                elif v[1][0]=="F":
                    bar_dic1[str(v[0])[4:10]]+=36
                elif v[1][0]=="V":
                    bar_dic1[str(v[0])[4:10]]+=8
                else:
                    bar_dic1[str(v[0])[4:10]]+=6
            except:
                if v[1][0]=="S":
                    bar_dic1[str(v[0])[4:10]]=2
                elif v[1][0]=="L":
                    bar_dic1[str(v[0])[4:10]]=18
                elif v[1][0]=="J":
                    bar_dic1[str(v[0])[4:10]]=24
                elif v[1][0]=="F":
                    bar_dic1[str(v[0])[4:10]]=36
                elif v[1][0]=="V":
                    bar_dic1[str(v[0])[4:10]]=8
                else:
                    bar_dic1[str(v[0])[4:10]]=6
        width=0.35
        bar_dic2={}
        line_dic={}
        fig, ax = plt.subplots()
        for k in list(bar_dic1.keys()):
            bar_dic2[k]=0
            line_dic[k]=0
        for (k,v) in dic_INT.items():
            p_id=k
            p_id=p_id[:-2]+'01'
            time=dic_EDCX[p_id][0]
            time=str(time)[4:10]
            bar_dic2[time]+=1
            if self.ui.comboBox.currentText()=="ALL" and self.ui.comboBox_2.currentText()=="ALL":
                if v[0] not in ['LB','LK','OK','LA']:
                    line_dic[time]+=1
            elif self.ui.comboBox.currentText()=="ALL" and self.ui.comboBox_2.currentText()!="ALL":
                if v[0]==self.ui.comboBox_2.currentText():
                    line_dic[time]+=1
            elif self.ui.comboBox.currentText()!="ALL" and self.ui.comboBox_2.currentText()=="ALL":
                if v[1]==self.ui.comboBox.currentText():
                    line_dic[time]+=1
            else:
                if v[1]==self.ui.comboBox.currentText() and v[0]==self.ui.comboBox_2.currentText():
                    line_dic[time]+=1
        for k,v in line_dic.items():
            if line_dic[k]==0 or bar_dic2[k]==0:
                continue
            else:
                line_dic[k]=line_dic[k]/bar_dic2[k]*100
        ax.bar(np.arange(len(bar_dic1))-width/2,list(bar_dic1.values()),width,label="Prod",color='b')
        ax.bar(np.arange(len(bar_dic2))+width/2,list(bar_dic2.values()),width,label="Light",color='g')
        ax.set_xticks(np.arange(len(bar_dic2)))
        ax.set_xticklabels(list(bar_dic2.keys()), rotation='vertical')
        ax.set_ylabel("Panel Nums",color='tab:blue')

        ax2 = ax.twinx()
        ax2.plot(np.arange(len(line_dic)),list(line_dic.values()),color='r')
        ax2.set_ylabel("Loss Rate",color='tab:red')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
        plt.ylim([0,max(list(line_dic.values()))+0.5])
        ax.legend()
        fig.tight_layout()
        plt.show()

        
if __name__=='__main__':
    app=QApplication(sys.argv)
    mainwindow=MainWindow()
    mainwindow.show()
    
    sys.exit(app.exec_())
