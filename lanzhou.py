# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen
import urllib 
import time
import sched
import csv


#input your query and your key
region_name=u'兰州市'
roads=['青兰高速','兴隆山大道','栖云北路','太白东路','G312']
filepath=r"C:\Users\Xin-yi.Song\Desktop\百度API\lanzhou\\" #设置存放路径

#input your own key. Here is xinyi's ak.
ak=r"&ak=x1kbYRksKTuBGRa0EXGgIB55cL6WqNSL"
#参考：ak=r"&ak=5UK6Um2nRBqID8cTTgYblTbGQREW8DtC"

#input step_length(s),data will be collected every step_length
step_length=60

def all_heads(): #此处定义了all_heads函数，用于创建文件并写表头
    for i in range(0,len(roads)):
        road_name=roads[i]
        filename=filepath+region_name+road_name+'.csv'   

        Header = u'道路名称',u'日期',u'时',u'分',u'路况整体评价',u'路况整体描述',u'拥堵路段',u'路段拥堵评价',u'较十分钟前拥堵趋势',u'拥堵距离',u'平均通行速度'
        with open(filename, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(Header)

def all_roads(sc):
    
    start = time.clock()#记录开始时间
    print('开始时间为：',start)    
   
    for i in range(0,len(roads)):
        road_name=roads[i]
        region=urllib.parse.quote(region_name.encode('utf-8'))
        road=urllib.parse.quote(road_name.encode('utf-8'))
        filename=filepath+region_name+road_name+'.csv'
    
        url=r"http://api.map.baidu.com/traffic/v1/road?city=%s&road_name=%s"%(region,road)
        aurl= url + ak 
        res=urlopen(aurl)
        cet=res.read()
        result=json.loads(cet)
    
        date=(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        h=(time.strftime('%H',time.localtime(time.time())))
        m=(time.strftime('%M',time.localtime(time.time())))
    
        x = result
        evaluation_status=x['evaluation']['status']
        evaluation_status_desc=x['evaluation']['status_desc'] 
        if len(x['road_traffic'][0])==1:
            traffic=[x['road_traffic'][0]['road_name'],date,h,m,evaluation_status,evaluation_status_desc]  
        else:
            congestions=x['road_traffic'][0]['congestion_sections']
            for j in range(len(congestions)):
                traffic=[x['road_traffic'][0]['road_name'],date,h,m,evaluation_status,evaluation_status_desc,congestions[j]['section_desc'],congestions[j]['status'],congestions[j]['congestion_trend'],congestions[j]['congestion_distance'],congestions[j]['speed']]
        print(traffic)
        f = csv.writer(open(filename, "a+",newline=''))
        f.writerow(traffic)
    
    end = time.clock()#记录结束时间
    print('结束时间为',end)
    
    cost = end-start#计算程序运行时间，6条路大概占用2秒
    print("程序运行时间为 : %.03f seconds" %(cost)) 
    
    sc.enter(step_length, 1, all_roads, (sc,))

#################主函数开始#########################      
s = sched.scheduler(time.time, time.sleep)

all_heads()#创建文件，并写表头

s.enter(step_length, 1, all_roads, (s,)) # 调用函数，格式为(delay, priority, action, argument)
s.run()        
    





