#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import re
import csv
from bs4 import BeautifulSoup

#设置URL固定部分
url= "http://www.cbooo.cn/year?year="
#设置请求头部信息
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/55.0.2883.87 Safari/537.36'
}
#循环抓取列表页信息
for year in range(2009,2019):
    if year == 2009:
        year=str(year)
        a=(url+year)

        r=requests.get(url=a,headers=headers)
        html=r.content
    else:
        year=str(year)
        a=(url+year)
        r=requests.get(url=a,headers=headers)
        html2=r.content
        html = html + html2
    #每次间隔0.5秒
    time.sleep(0.5)
lj=BeautifulSoup(html,'html.parser')

#提取名称、类型、总票房（万）、平均票价、场均人次及国家及地区
result=lj.find_all('td')

mname=[]
title=""
index=1
year=2009
for i in result:
    i=str(i)
    title=re.findall(r'</span>(.*?)</p>',i,re.I|re.M)
    if len(title)>0:
        mname.append(index)
        index=index+1
        mname.append(title[0])
    else:
        info=re.findall(r'<td>(.*?)</td>',i,re.I|re.M)
        mname.append(info[0])

k=0
data=[]
while k<2000:
    year=2009
    year=year+(k//200)
    data.append([mname[k],mname[k+1],mname[k+2],mname[k+3],mname[k+4],mname[k+5],
                 mname[k+6],mname[k+7],year,1])
    k=k+8
#print(data)
print(len(data))#一共250条数据
#将结果存到CSV文件

with open('./data.csv','w') as fout:
    cin= csv.writer(fout,lineterminator='\n')
    for item in data:
        cin.writerow(item)




