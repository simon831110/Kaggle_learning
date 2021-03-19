from crawler import DatasetCrawler,get_cookies
import time

def crawl(dic):
    ID_types={'TFT':'PANELID',
          'ALL':'PANELID',
          'CF':'PANELID_CF'}
    IE_headers={
            'Accept':'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
            'Host':'intrpt',
            'Cookie':'ASPSESSIONIDSASSBDTT=HJHNLMHBEPPKJOJDHKOOLGJL',
            'Referer':'http://intrpt/EDC/EDC_Query_Dataset.asp?wFab=L6',
            'Accept-Encoding':'gzip, deflate',
            'Content-Length':'235',
            'Cache-Control':'no-cache',
            'Connection':'Keep-Alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept-Language':'en-US, en; q=0.8, zh-Hant-TW; q=0.5, zh-Hant; q=0.2',
           }
    IE_data={
            'Facility':'L6',
            'qryBy':'time',
            'subEntity':dic['Sub'],
            'CDATE_F':dic['from_date'],
            'CDATE_T':dic['to_date'],
            'fromHr':dic['from_Hour'],
            'fromMut':dic['from_Min'],
            'toHr':dic['to_Hour'],
            'toMut':dic['to_Min'],    
            'grpKind':'time',
            'EDCItem':dic['EDCITEM'],
            'EQPID':dic['line'],
            'wFab':'L6'
            }
    chrome_headers={
        'Host': 'intrpt',
        'Connection': 'keep-alive',
        'Content-Length': '779',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://intrpt',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'Referer': 'http://intrpt/WEB/INT/LCD/INTQuery/INTQuery.aspx?fab=LCD_6_INT',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    chrome_datas={
        "FABNUM": "6",
        "ReportID": dic["INT_cls"],
        "qby": "ID",
        "PRODSIZE": "",
        "IDType": ID_types[dic['sub_third']],
        "OPERATION": dic['spot'],
        "TESTCOUNT": "A",
        "LCMTESTCOUNT": "A",
        "FAB": "LCD_6_INT"
    }
    IEcrawler=DatasetCrawler("http://intrpt/EDC/EDC_Query_Dataset.asp?wFab=L6",
                         IE_headers,
                         IE_data,
                         dic
                         )
    IEdatas=IEcrawler.IE_crawl()
    IEcrawler.write_excel()
    time_start=time.time()
    h=get_cookies()
    print("抓Cookies時間為",time.time()-time_start)
    chrome_datas["txtID"]=IEdatas
    chrome_headers['Authorization']='Bearer '+h['value']
    chrome_headers['Cookie']=h['name']+'='+h['value']
    CHROMEcrawler=DatasetCrawler("http://intrpt/WEB/INT/LCD/INTQuery/INTQuery_Import.ashx",
                         chrome_headers,
                         chrome_datas
                         )
    time_start=time.time()
    CHROMEcrawler.chrome_crawl()
    CHROMEcrawler.write_excel()
    chrome_datas["ReportID"]="PIVOT"
    chrome_datas["TESTCOUNT"]="F"
    Analysis_crawler=DatasetCrawler("http://intrpt/WEB/INT/LCD/INTQuery/INTQuery_Pivot.ashx",
                         chrome_headers,
                         chrome_datas
                         )
    time_start=time.time()
    Analysis_crawler.chrome_analysis_crawl()
    print("Chrome不良分析時間為",time.time()-time_start)
def INT_crawl(dic):
    ID_types={'TFT':'PANELID',
          'ALL':'PANELID',
          'CF':'PANELID_CF'}
    chrome_headers={
        'Host': 'intrpt',
        'Connection': 'keep-alive',
        'Content-Length': '779',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://intrpt',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'Referer': 'http://intrpt/WEB/INT/LCD/INTQuery/INTQuery.aspx?fab=LCD_6_INT',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    chrome_datas={
        "FABNUM": "6",
        "ReportID": dic["INT_cls"],
        "qby": "ID",
        "PRODSIZE": "",
        "IDType": ID_types[dic['pnl_cls']],
        "OPERATION": dic['spot'],
        "TESTCOUNT": "A",
        "LCMTESTCOUNT": "A",
        "FAB": "LCD_6_INT"
    }
    h=get_cookies()
    
    chrome_datas["txtID"]=dic['txtID']
    chrome_headers['Authorization']='Bearer '+h['value']
    chrome_headers['Cookie']=h['name']+'='+h['value']
    CHROMEcrawler=DatasetCrawler("http://intrpt/WEB/INT/LCD/INTQuery/INTQuery_Import.ashx",
                         chrome_headers,
                         chrome_datas
                         )
    CHROMEcrawler.write_excel()
    CHROMEcrawler.chrome_crawl()
    CHROMEcrawler.write_excel()

    chrome_datas["ReportID"]="PIVOT"
    chrome_datas["TESTCOUNT"]="F"
    Analysis_crawler=DatasetCrawler("http://intrpt/WEB/INT/LCD/INTQuery/INTQuery_Pivot.ashx",
                         chrome_headers,
                         chrome_datas
                         )
    time_start=time.time()
    Analysis_crawler.chrome_analysis_crawl()
    print("Chrome不良分析時間為",time.time()-time_start)
