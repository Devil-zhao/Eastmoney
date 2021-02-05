#用静态方法抓取静态网页
import scrapy
import pandas as pd

from selenium import webdriver
from lxml import etree
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList
from zh.items import ZhItem

class EastmoneySpider(scrapy.Spider):
    name = 'Eastmoney'
    allowed_domains = ['group.eastmoney.com']
    start_urls = ["http://group.eastmoney.com"]

    def parse(self, response):
        content = response.xpath("//div[@class='mod-center']//div[@class='mod-center-dom']//"
                                 "div[@class='mod-center-right']//"
                                 "div[@class='combin_rank list']//div[@class='info_ul']//"
                                 "div[@class='data']")
        na = list()
        wi = list()
        re = list()
        for c in content:
            name = c.xpath(".//li[@class='w110']//a//text()").getall()
            win = c.xpath(".//li[@class='w70']//text()").getall()
            revenue1 = c.xpath(".//li[@class='w80 red checked']//text()").getall()
            revenue2 = c.xpath(".//li[@class='w70 red checked']//text()").getall()
            url = c.xpath(".//li[@class='w110']//a//@href").getall()
            if len(revenue1) != 0:
                revenue = revenue1
            else:
                revenue = revenue2
            na.append(name)
            wi.append(win)
            re.append(revenue)

        #生成excel表格
        df1 = {'姓名': na[0], '胜率': wi[0], '收益': re[0]}
        sku_df1 = pd.DataFrame(df1)
        sku_df1.to_excel('1日排行.xlsx', index=False)
        df2 = {'姓名': na[1], '胜率': wi[1], '收益': re[1]}
        sku_df2 = pd.DataFrame(df2)
        sku_df2.to_excel('5日排行.xlsx', index=False)
        df3 = {'姓名': na[2], '胜率': wi[2], '收益': re[2]}
        sku_df3 = pd.DataFrame(df3)
        sku_df3.to_excel('20日排行.xlsx', index=False)
        df4 = {'姓名': na[3], '胜率': wi[3], '收益': re[3]}
        sku_df4 = pd.DataFrame(df4)
        sku_df4.to_excel('250日排行.xlsx', index=False)
        df5 = {'姓名': na[4], '胜率': wi[4], '收益': re[4]}
        sku_df5 = pd.DataFrame(df5)
        sku_df5.to_excel('总排行.xlsx', index=False)
        pass

    def parse_item(self,response):
        item = ZhItem()
        yield item