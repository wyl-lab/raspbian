# -*- coding:utf-8 -*-
#!/usr/bin/python
# coding=utf-8
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import datetime
import requests
import random
import socket
import bs4
import time
import json
from bs4 import BeautifulSoup
from email.header import Header
from lxml import html
from aip import AipSpeech
'''
setConnectionTimeoutInMillis	建立连接的超时时间（单位：毫秒
setSocketTimeoutInMillis	通过打开的连接传输数据的超时时间（单位：毫秒）
参数	类型	    描述	                              是否必须
tex	    String	合成的文本，使用UTF-8编码，
                请注意文本长度必须小于1024字节	            是
                
CUID	String	用户唯一标识，用来区分用户，
                填写机器 MAC 地址或 IMEI 码，长度为60以内	否

spd	    String	语速，取值0-9，默认为5中语速	            否

pit	    String	音调，取值0-9，默认为5中语调	            否

vol	    String	音量，取值0-15，默认为5中音量	            否

per	    String	发音人选择, 0为女声，1为男声，
                3为情感合成-度逍遥，	
                4为情感合成-度丫丫，默认为普通女            否
'''

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
        weather_status = []
        li = ul.find_all('li')
        j=0
        #return li
        for i in li:
            j+=1
            if j==2:
                weather_status = i
                weather_status = str(weather_status).replace('\n','').replace('\t','').replace(' ','').replace("</li>","").replace('\r','')
                weather_status = weather_status.replace('<li><span>','').replace('<imgalt=','').replace('src="https://h5tq.moji.com/tianqi/assets/images/weather/','')
                weather_status = weather_status.replace('.png/></span>','').replace('.png"/></span>','').replace('"','').replace('\t','')
                #print(a)
                
                for x in range(100,-1,-1):
                    #print("w{0}".format(x))
                    weather_status = weather_status.replace(("w{0}".format(x)),'')

        if(len(weather_status)==2):
            weather_status = weather_status[0:1]
        if(len(weather_status)==4):
            weather_status = weather_status[0:2]

        for day in li:
            #if not isinstance(day,bs4.element.Tag): 
                #date = day.find('a',href='https://tianqi.moji.com/today/china/shandong/penglai').string
            weather_list.append(day.string)
            if not isinstance(day,bs4.element.Tag):
                wind_direction = day.find('em').string
                wind_grade = day.find('b').string
                    
        Tempreture = weather_list[2] # type:<class 'bs4.element.NavigableString'>
        # 8°/15° => 8 到 15 摄氏度
        Tempreture = Tempreture.replace('°','').replace('/','，到，')+'摄氏度'
        
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
        
        result = date +"好，管家为您播报。\n蓬莱，室外环境情况："+weather_status+"，\n白天到夜间，"+Tempreture+"，\n" + \
                 wind_direction+wind_grade+"，"+"空气质量，"+air_quality+"。\n\n"
        result += "生活小助手在此提醒您当前环境：\n"
        #print(result)
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
            if(i==4 or i==7):
                    continue
            """
            if(i==5):
                    life_list.append(result1[i])
                    life_list.append("紫外线")
                    continue
            #带不带伞
            if(i==6):
                    life_list.append("带雨伞")
                    life_list.append(result1[i])
                    continue
            """
            life_list.append(result[i]+"方面")
            life_list.append(result1[i])
    #print(life_list)
    return life_list

'''
        sender = input('From: ')
        password = input('password: ')
        smtp_server = input('SMTP_Server: ')
        message = MIMEText("亲爱的,我现在来播报今天的蓬莱天气。\n(嗯...其实现在还只能看不能播)如下所示：\n 时 间| 天气情况 | 温 度 | 风 向 | 风 速 | 空气质量\n'{0}\n".format(result),'plain','utf-8')
        message = MIMEText("尊敬的主人，接下来由我来为您播报蓬莱的天气情况 :\n{}\n{}".format(result,life_list),'plain','utf-8')
        #精简版播报
        message = MIMEText("尊敬的主人，接下来由我来为您播报蓬莱的天气情况 :\n{}".format(result),'plain','utf-8')
'''
#收件人、主题、内容、附件名称
def send_email(recipientAddrs, Subject, content, attachmentName):              
        message = email.mime.multipart.MIMEMultipart()
        txt = MIMEText(content, 'plain', 'utf-8')
        message.attach(txt)       
     
        # 添加附件
        part = MIMEApplication(open(attachmentName,'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=attachmentName )
        message.attach(part)

        headerDefine_From = 'wyl1346788525@163.com'
        headerDefine_To = '主人'
        ## 注意: 该段仅用来显示，但要合规，否则当做垃圾邮件处理，导致发送失败！
        message['From'] = Header(headerDefine_From) # 否则被当做垃圾邮件处理
        message['To'] = Header(headerDefine_To, 'utf-8')#实际收件人 server.sendmail(()方法的recipientAddrs
        message['Subject'] = Header(Subject, 'utf-8')   #邮件主题
        # static content
        sender = 'wyl1346788525@163.com'
        sent_host = 'smtp.163.com'
        sent_user = 'wyl1346788525@163.com'
        sent_pass = 'cxlgWYL!@'
        ##  TO   receivers = ['1346788525@qq.com','2436632009@qq.com','wyl1346788525@yeah.net','1412983603@qq.com','wyl1346788525@163.com','wyl1346788525@sohu.com']
        try:
            server = smtplib.SMTP()
            #server = smtplib.SMTP(sent_host,25)
            #print("SMTP complete")
            server.connect(sent_host,25)
            #print("connect complete")
            #server.set_debuglevel(1)
            server.login(sent_user,sent_pass)
            #print("login complete")
            #for i in range(len(receivers)-5):
                #server.sendmail(sender,receivers[i],message.as_string())
            server.sendmail(sender, recipientAddrs, message.as_string())
            print("邮件发送成功")
            server.quit()
        except smtplib.SMTPException:
            print("Error:发生未知错误，无法发送邮件!")

            
#完成爬虫信息的整合
def implementCrawler():
        result =[]
        url = 'http://tianqi.moji.com/weather/china/shandong/penglai'
        data = get_content(url)
        #life_list = get_life(url)
        #print("a is {}".format(soup_Life(life_list)))

        result = get_weather(url,data)
        result = str(result).replace("\\r","").replace('\t','').replace('\r','').replace("\\n","")
        #print("result is \n{}".format(result))
        return result


#用于获取环境信息[室内、室外]:Home Part
def getContent():
        environment_Indoor = "室内温度"+"湿度"
        return environment_Indoor


'''
        功能：用于将implementCrawler方法 与 getContent方法 返回的 文本信息==>音频文件(mp3)
        参数：附件名称
'''
def speechSynthesis(content, attachmentName):
        ## static content      
        APP_ID = '24025146'
        API_KEY = '0Wv3AGwPg5Y4Sa8GzB09qTGw'
        SECRET_KEY = 'Lk3oDN6Y7GGBZWB4BpNM7OpbOGSNvkeV'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        CUID = 'raspbian'
        voiceConfig  = client.synthesis(content, 'zh', 1, {
                'spd': 3,   # 语速，取值0-15，默认为5中语速
                'pit': 5,   # 音调，取值0-15，默认为5中语调
                'vol': 6,   # 音量，取值0-9，默认为5中音量
# 度逍遥（精品）=5003，度小鹿=5118，度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5
                'per': 5118,
         })
        # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
        AUE = 3
        FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
        FORMAT = FORMATS[AUE]

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(voiceConfig, dict):
                #print("\n准备生成MP3音频格式文件")
                with open(attachmentName, 'wb') as f:
                        f.write(voiceConfig)
                print("音频文件生成完毕")
        else:
                #print(type(voiceConfig))
                json_data = json.dumps(voiceConfig)
                #print("Json对象",json_data)
                #print ("Python 原始数据：", repr(voiceConfig),'\n')
                #将 JSON 对象转换为 Python 字典
                pyDicts = json.loads(json_data)
                #print ("pyDicts['err_no']: ", pyDicts['err_no'])
                print ("pyDicts['err_msg']: ", pyDicts['err_msg'])
       


if __name__  == '__main__':
        '''
        错误码	含义
        500	不支持的输入
        501	输入参数不正确
        502	token验证失败
        503	合成后端错误
        '''
        #收件人、主题、内容、附件名称
        recipientAddrs = "1346788525@qq.com"
        Subject = "智能家居-环境情况播报 [ 室内、室外 ] "
        content = implementCrawler()#调用方法获取爬虫信息
        attachmentName = "syntheticVoice.mp3"
        
        speechSynthesis(content, attachmentName) # 语音识别
        send_email(recipientAddrs, Subject, content, attachmentName)
        


