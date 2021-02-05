#动态方法（模拟浏览器Chrome）抓取动态网页
from lxml import etree
import time
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
from selenium import webdriver
#模拟浏览器，获取网页源码
driver = webdriver.Chrome(executable_path='chromedriver')

class Company():
    def __init__(self):
        self.name=""
        self.url=""
        self.url2=""

    def Scrapy_chrome(self):
        url = "http://group.eastmoney.com/mcombin,10001.html"
        driver.get(url)
        time.sleep(3)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        resp_text = driver.page_source
        page_html = etree.HTML(resp_text)
        lis = page_html.xpath("/html/body/div[3]/div/div[2]/div[5]/div[1]/ul")
        #两个列表，分别用来存储公司名称和链接
        product_list = []
        next_list = []

        for li in lis:
            product = li.xpath('.//li[10]/a/text()')[0]
            next_url = li.xpath('.//li[10]/a/@href')[0]
            product_list.append(product)
            next_list.append(next_url)

        #去重
        no_repeat=lambda x,y:x if y in x else x+[y]
        reduce1 = reduce(no_repeat,[[],]+(product_list))
        reduce2 = reduce(no_repeat,[[],]+(next_list))
        self.name = reduce1
        self.url = reduce2

        # 生成company.xlsx
        df = {'公司名称': reduce1, '公司链接': reduce2}
        sku_df1 = pd.DataFrame(df)
        sku_df1.to_excel('company.xlsx', index=False)
        pass
    #模拟浏览器抓取实时数据的链接
    def Scrapy_url(self):
        url2 = []
        for i in self.url:
            driver.get(i)
            time.sleep(3)
            driver.execute_script('window.scrollTo(0,1000)')
            time.sleep(3)
            resp_text = driver.page_source
            page_html = etree.HTML(resp_text)
            lis = page_html.xpath("//*[@id='vvcc']/table/tfoot/tr/td/a/@href")
            if len(lis) == 0:
                lis = page_html.xpath("/html/body/div[1]/div[5]/div[4]/div/div[2]/div[1]/a/@href")
            url2.append(lis[0])
        self.url2 = url2
        pass

    def Scrapy_data(self):
        l=0
        for i in self.url2:
            driver.get(i)
            time.sleep(1)
            driver.execute_script('window.scrollTo(0,1000)')
            time.sleep(1)
            resp1 = driver.page_source
            page1= etree.HTML(resp1)
            value = page1.xpath("//*[@id='jk']/text()")[0]
            if len(value) == 0:
                l += 1
                continue
            open_value = float(value)
            k=page1.xpath("/html/body/div[1]/div[2]/div[4]"
                                           "/div[2]/ul/li[5]/span[2]/text()")
            if len(k) == 0:
                l += 1
                continue
            ti = []
            reve = []
            differ = []
            j=1
            while j<= int(k[0]):
                resp = driver.page_source
                page_html = etree.HTML(resp)
                data = page_html.xpath('/html/body/div[1]/div[2]/div[4]/div[1]')
                for d in data:
                    li = d.xpath('.//tr/td[1]/text()')
                    da = d.xpath('.//tr/td[2]/text()')
                    for x in li:
                        ti.append(x)
                    for x in da:
                        reve.append(x)
                        differ.append(float(x)-open_value)
                next_page = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[4]/div[2]/ul/li[text()='下一页']")
                next_page.click()
                time.sleep(2)
                j+=1
            df2 = {'时间': ti, '成交价': reve, '差值': differ}
            sku_df2 = pd.DataFrame(df2)
            name = self.name[l]+'.xlsx'
            sku_df2.to_excel(name, index=False)
            l+=1
        pass

    #数据可视化
    def visual(self):
        for i in self.name:
            j = i + '.xlsx'
            title = i + '股票涨跌浮动.jpg'
            df = pd.read_excel(j)
            plt.plot(df["时间"], df["差值"], label='时间', linewidth=1, color='r', markersize=20)
            plt.xlabel("时间")
            plt.ylabel('差值')
            plt.title("revenue float")
            plt.legend()
            plt.grid()
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.savefig(title)
            plt.show()

C = Company()
C.Scrapy_chrome()
C.Scrapy_url()
C.Scrapy_data()
C.visual()
driver.quit()