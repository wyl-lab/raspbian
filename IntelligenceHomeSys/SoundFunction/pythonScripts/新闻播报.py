#coding=utf-8
import datetime
import time
import smtplib
import requests
import random
import socket
import bs4
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
from lxml import html
import json
from aip import AipSpeech

def get_content(url):
        header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control' : 'max-age=0',
    'Connection' : 'keep-alive',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        timeout = random.choice(range(80, 180))
        while True:
            try:
                rep = requests.get(url,headers = header,timeout = timeout)
                rep.encoding = 'utf-8'
                break
            except socket.timeout as e:
                print( '3:', e)
                time.sleep(random.choice(range(8,15)))
            except socket.error as e:
                print( '4:', e)
                time.sleep(random.choice(range(20, 60)))
        return rep.text


def get_weather(url,data):
        air_list = []
        weather_list = []
        #weather_status = []
        soup = BeautifulSoup(data,'lxml')
        div = soup.find('div',{'class' : 'forecast clearfix'})

        air_quality = div.find('strong',class_='level_2').string    #空气质量
        date = div.find('a',href='https://tianqi.moji.com/today/china/shandong/penglai').string
        wind_direction = div.find('em').string   #风向
        wind_grade = div.find('b').string           #风速
        ul = div.find('ul',{'class' : 'clearfix'})

        ##  天气情况抽取  ##
        a = []
        li = ul.find_all('li')
        j=0
        #return li
        for i in li:
            j+=1
            if j==2:
                a = i
                a = str(a).replace('\n','').replace('\t','').replace(' ','').replace("</li>","").replace('\r','')
                a = a.replace('<li><span>','').replace('<imgalt=','').replace('src="https://h5tq.moji.com/tianqi/assets/images/weather/','')
                a = a.replace('.png/></span>','').replace('.png"/></span>','').replace('"','').replace('\t','')
                #print(a)
                
                for x in range(100,-1,-1):
                    #print("w{0}".format(x))
                    a = a.replace(("w{0}".format(x)),'')

        if(len(a)==2):
            a = a[0:1]
        if(len(a)==4):
            a = a[0:2]

        for day in li:
            #if not isinstance(day,bs4.element.Tag): 
                #date = day.find('a',href='https://tianqi.moji.com/today/china/shandong/penglai').string
            weather_list.append(day.string)
            if not isinstance(day,bs4.element.Tag):
                wind_direction = day.find('em').string
                wind_grade = day.find('b').string
                    
        Tempreture = weather_list[2]
        air_quality =air_quality.replace("\n","").replace(' ','')
        #air_quality = str(air_quality).replace('\n','').replace(' ','')
        #print("'data' {0} 'Tempreture' {1}，air_quality {2}\n,'wind_grade' {3},'wind_direction' {4}".format(date,Tempreture,air_quality,wind_grade,wind_direction))
        i = datetime.datetime.now()
        month = i.month
        day = i.day
        hour = i.hour
        if(hour<12):
                date = "上午"
        elif hour<16:
                date = "下午"
        elif hour<20:
                date = "傍晚"
        elif hour<24:
                date = "晚上"
        else:
                date = "凌晨"

        life_list = get_life(url)
    
        result = "今天"+date+"的天气情况:"+a+Tempreture+"，"+wind_direction+wind_grade+"，"+"空气质量 "+air_quality
        result += "生活小助手在此提醒您当前环境"
        print(result)
        result += life_list[0]
        for i in range(1,len(life_list)):
                if i%2==0:
                        result += "，"
                result += "".join(life_list[i])
        return result
        #return (" 今天{}的天气情况: {}，{}，{}{}，空气质量 {}".format(date,a,Tempreture,wind_direction,wind_grade,air_quality))


def get_life(url):
    life_list = []
    page = requests.Session().get(url)
    tree = html.fromstring(page.text)
    result = tree.xpath('//div[@class="live_index_grid"]//dd/text()')
    result1 = tree.xpath('//div[@class="live_index_grid"]//dt/text()')
    for i in range(10):
            if(i==2 or i==9):
                    continue
        
            if(i==5):
                    life_list.append(result1[i])
                    life_list.append("紫外线")
                    continue
            #带不带伞
            if(i==6):
                    life_list.append("可以")
                    life_list.append(result1[i])
                    continue
            life_list.append(result1[i])
            life_list.append(result[i])
    print(life_list)
    return life_list


def soup_Life(life_list):
    tplt = "{0:^10}\t{1:{4}^10}\t{2:^10}\t{3:^10}"
    print("Soup_Life")
    print(tuple(life_list))

    #life_list = str(life_list).replace("(","").replace("'",'').replace(')','').replace(",","").replace("[","").replace("]","")
    print(life_list)
    count = 0
    left_Life =[]
    right_Life = []
    All_life =[]
    for i in life_list:
            count += 1
            if((count%2)==0):
                    right_Life.append(i)
            else:
                    left_Life.append(i)
    left_Life = str(left_Life).replace("(","").replace("[",'').replace(')','').replace(']','')
    right_Life = str(right_Life).replace("(","").replace("[",'').replace(')','').replace(']','')
   
    print(left_Life+"  left_Life END ")
    print(right_Life+"  right_Life END ")
    return left_Life,right_Life


def send_email():
        '''
        sender = input('From: ')
        password = input('password: ')
        smtp_server = input('SMTP_Server: ')'''
        ##     FROM    ##
        sender = 'wyl1346788525@163.com'
        sent_host = 'smtp.163.com'
        sent_user = 'wyl1346788525@163.com'
        sent_pass = 'cxlgWYL!@'

        ##     TO     ##
        receivers = ['1346788525@qq.com','2436632009@qq.com','wyl1346788525@yeah.net','1412983603@qq.com','wyl1346788525@163.com','wyl1346788525@sohu.com']

        #message = MIMEText("亲爱的,我现在来播报今天的蓬莱天气。\n(嗯...其实现在还只能看不能播)如下所示：\n 时 间| 天气情况 | 温 度 | 风 向 | 风 速 | 空气质量\n'{0}\n".format(result),'plain','utf-8')
        message = MIMEText("尊敬的主人，接下来由我来为您播报蓬莱的天气情况 :\n{}\n{}".format(result,life_list),'plain','utf-8')
        #精简版播报
        #message = MIMEText("尊敬的主人，接下来由我来为您播报蓬莱的天气情况 :\n{}".format(result),'plain','utf-8')
       
        ##   JUST USE TO DISPLAY   ##
        Subject = "智能家居-今日天气播报!"
        headerDefine_From = 'wyl1346788525@163.com' # 注意 utf-8 以及 headerDefine_From 写自己，
        headerDefine_To = '主人'
        
        message['From'] = Header(headerDefine_From) # 否则被当做垃圾邮件处理，导致发送失败
        message['To'] = Header(headerDefine_To,'utf-8')
        message['Subject'] = Header(Subject,'utf-8')   #标题
        try:
            server = smtplib.SMTP()
            #server = smtplib.SMTP(sent_host,25)
            print("SMTP complete")

            server.connect(sent_host,25)
            print("connect complete")
            
            server.set_debuglevel(1)
            server.login(sent_user,sent_pass)
            print("login complete")

            #for i in range(len(receivers)-5):
                #server.sendmail(sender,receivers[i],message.as_string())
            server.sendmail(sender,receivers[0],message.as_string())
            print("邮件发送成功")
            server.quit()

        except smtplib.SMTPException:
            print("Error:发生未知错误，无法发送邮件!")

def implementCrawler():
        result =[]
        url = 'http://tianqi.moji.com/weather/china/shandong/penglai'
        data = get_content(url)
        #life_list = get_life(url)
        #print("a is {}".format(soup_Life(life_list)))

        result = get_weather(url,data)
        result = str(result).replace("\\r","").replace('\t','').replace('\r','').replace("\\n","")
        print("result is \n{}".format(result))
        return result
        #send_email()

def context():
        """ 你的 APPID AK SK """
        APP_ID = '24025146'
        API_KEY = '0Wv3AGwPg5Y4Sa8GzB09qTGw'
        SECRET_KEY = 'Lk3oDN6Y7GGBZWB4BpNM7OpbOGSNvkeV'

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        cuid = 'raspberry'
        content = implementCrawler()

        result  = client.synthesis(content, 'zh', 1, {
                'spd': 4,
                'pit': 6,
                'vol': 8,
                'per': 110,
         })

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
                print("\n准备生成MP3音频格式文件")
                with open('audio1.mp3', 'wb') as f:
                        f.write(result)
                print("音频文件生成完毕")
        else:
                print(type(result))
                json_data = json.dumps(result)
                print("Json对象",json_data)
                print ("Python 原始数据：", repr(result),'\n')
        # 将 JSON 对象转换为 Python 字典
        pyDicts = json.loads(json_data)
        print ("pyDicts['err_no']: ", pyDicts['err_no'])
        print ("pyDicts['err_msg']: ", pyDicts['

if __name__  == '__main__':
        print("热点新闻播报功能待开发中.....")
	


