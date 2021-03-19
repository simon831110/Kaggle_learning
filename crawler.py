import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time


def get_cookies():
    dic={}
    options = Options()
    options.add_argument('--headless')

    chrome = webdriver.Chrome('./chromedriver',options=options)
    chrome.get("http://intrpt/WEB/INT/LCD/INTQuery/INTQuery.aspx?fab=LCD_6_INT")
    
    WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.ID, 'sidebar')))
    cookies=chrome.get_cookies()
    chrome.quit()
    return cookies[0]

cls_dic={
    "TFT":"T",
    "CF":"F"
    }
writer = pd.ExcelWriter('./Panel_data.xlsx')
class DatasetCrawler():
    def __init__(self,url,headers,input_data,dic=None):
        self.url=url
        self.headers=headers
        self.input_data=input_data
        self.dic=dic
        self.output={}
        self.output["IE_state"]="f"
        self.output["IE_num"]=0
        self.output["Chrome_state"]="f"
        self.output["Chrome_num"]=0
    def IE_crawl(self):
        time_start=time.time()
        data=requests.post(self.url,data=self.input_data,headers=self.headers)
        if data.ok:
            self.output["IE_state"]="s"
        else:
            self.output["IE_state"]="f"
        print("IE POST時間為",time.time()-time_start)
        time_start=time.time()
        url_code=str(data.text)
        i=1
        #ID:[玻璃類別,生產時間]
        ID_dic={}
        while True:
            longg=len("GridAddText Grid1 , "+str(i)+" , 1 , ")
            ID_start=url_code.find("GridAddText Grid1 , "+str(i)+" , 1 , ")
            Time_start=url_code.find("GridAddText Grid1 , "+str(i)+" , 2 , ",ID_start)
            Class_start=url_code.find("GridAddText Grid1 , "+str(i)+" , 4 , ",Time_start)
            # 找不到資料
            if ID_start==-1 or Class_start==-1 or Time_start==-1:
                break
            if self.dic['sub_second']=='01' or self.dic['sub_second']=='02' or self.dic['sub_second']=='03' or self.dic['sub_second']=='04':
                number_start=url_code.find('edcArr = Split("',Class_start)
                i+=1
                if int(url_code[number_start+16])==int(self.dic['sub_second']):
                    if self.dic['sub_third']=="ALL" or cls_dic[self.dic['sub_third']]==url_code[ID_start+longg+1]:
                        ID_dic[url_code[ID_start+longg+1:ID_start+longg+13]]=[]
                        ID_dic[url_code[ID_start+longg+1:ID_start+longg+13]].append(url_code[Class_start+longg+3:Class_start+longg+7])
                        ID_dic[url_code[ID_start+longg+1:ID_start+longg+13]].append(url_code[Time_start+longg+1:Time_start+longg+15])
            else:
                if self.dic['sub_third']=="ALL" or cls_dic[self.dic['sub_third']]==url_code[ID_start+longg+1]:
                    ID_dic[url_code[ID_start+longg+1:ID_start+longg+13]]=[]
                    ID_dic[url_code[ID_start+longg+1:ID_start+longg+13]].append(url_code[Class_start+longg+3:Class_start+longg+7])
                    ID_dic[url_code[ID_start+longg+1:ID_start+longg+13]].append(url_code[Time_start+longg+1:Time_start+longg+15])        
                i+=1
        self.output["IE_num"]=len(ID_dic)
        s=""
        df={}
        df["GLASS_ID"]=[]
        df["TRANSDT"]=[]
        df["PFCD"]=[]
        for k,v in ID_dic.items():
            if k[-2:]!='01':
                continue
            else:
                if v[0][0]=='S':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,3):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                elif v[0][0]=='2':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,7):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                elif v[0][0]=='3':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,7):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                elif v[0][0]=='J':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,25):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                elif v[0][0]=='L':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,19):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                elif v[0][0]=='F':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,37):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                elif v[0][0]=='V':
                    df["GLASS_ID"].append(k)
                    df["TRANSDT"].append(v[1])
                    df["PFCD"].append(v[0])
                    for i in range(1,9):
                        s+=str(k[:-2]+str(i).zfill(2)+",")
                else:
                    continue
        df=pd.DataFrame(df)
        df.to_excel(writer,sheet_name="EDCX",index=False)
        print("IE 處理時間為",time.time()-time_start)
        return s
    def chrome_crawl(self):
        time_start=time.time()
        dataset=requests.post(self.url,json=self.input_data,headers=self.headers)
        print("Chrome POST時間: ",time.time()-time_start)
        if dataset.ok:
            time_start=time.time()
            self.output["Chrome_state"]="s"
            dataset_txt=dataset.text
            dataset_txt=dataset_txt.replace("null","None")
            dataset_txt=dataset_txt.replace(" ","")
            dataset_txt=eval(dataset_txt)
            print("轉成json時間: ",time.time()-time_start)
            time_start=time.time()
            results=dataset_txt["result"]
            self.output["Chrome_num"]=len(results)
            print(len(results))
            if len(results)>0:
                df={}
                for k in results[0]:
                    df[k]=[]
                for result in results:
                    for k,v in result.items():
                        df[k].append(v)
                df=pd.DataFrame(df)
                df.to_excel(writer,sheet_name="INT",index=False)
            print("Chrome 寫入xlsx時間: ",time.time()-time_start)
            #print(dataset.text)
        else:
            self.output["Chrome_state"]="f"
    def chrome_analysis_crawl(self):
        dataset=requests.post(self.url,json=self.input_data,headers=self.headers)
        if dataset.ok:
            df={}
            self.output["Chrome_state"]="s"
            dataset_txt=dataset.text
            dataset_txt=dataset_txt.replace("null","None")
            dataset_txt=dataset_txt.replace(" ","")
            dataset_txt=eval(dataset_txt)
            results=dataset_txt["result"]
            self.output["Chrome_num"]=len(results)

            if len(results)>0:
                for k in results[0]:
                    df[k]=[]
                for result in results:
                    for k,v in result.items():
                        df[k].append(v)
                cols=list(df.keys())
                cols.remove('ALL_VALUE')
                cols.remove('LOSS_VALUE')
                cols.remove('LossRate%')
                cols.remove('DefectRate%')
                cols.append('ALL_VALUE')
                cols.append('LossRate%')
                cols.append('DefectRate%')
                df=pd.DataFrame(df)
                df.to_excel(writer,sheet_name="樞紐",index=False,columns=cols)
                writer.save()
            else:
                df=pd.DataFrame()
                df.to_excel(writer,sheet_name="樞紐",index=False)
                writer.save()
        else:
            self.output["Chrome_state"]="f"
    def write_excel(self):
        with open('state.csv', 'a', newline='') as csvfile:
            fieldnames = ['IE_state', 'IE_num', 'Chrome_state','Chrome_num']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(self.output)
