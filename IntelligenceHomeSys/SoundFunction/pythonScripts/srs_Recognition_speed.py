# -*- coding:utf-8 -*-
#!/usr/bin/python
# coding=utf-8
import sys
import json
import base64
import time

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
timer = time.perf_counter

""" 你的 APPID AK SK """
APP_ID = '24025146'
API_KEY = '0Wv3AGwPg5Y4Sa8GzB09qTGw'
SECRET_KEY = 'Lk3oDN6Y7GGBZWB4BpNM7OpbOGSNvkeV'

# 需要识别的文件
AUDIO_FILE= './voice/test.pcm'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
CUID = 'raspbian'
# 采样率
RATE = 16000  # 固定值
# 极速版 打开注释的话请填写自己申请的appkey appSecret ，并在网页中开通极速版（开通后可能会收费）
DEV_PID = 80001
ASR_URL = 'http://vop.baidu.com/pro_api'
SCOPE = 'brain_enhanced_asr'  # 有此scope表示有极速版能力，没有请在网页里开通极速版

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'

class DemoError(Exception):
    pass

def fetch_token():
    params = {
              'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode( 'utf-8') # 编码
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str =  result_str.decode() # 解码
    result = json.loads(result_str) # 是将json格式数据转换为python字典类型

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def speechRecognition_Speed():
    token = fetch_token()
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data) #  base64 编码后，数据会增大 1/3
    speech = str(speech, 'utf-8') # 转换为字符串
    params = {'dev_pid': DEV_PID,
             #"lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    # 是将一个Python数据类型列表进行json格式的编码解析
    post_data = json.dumps(params, sort_keys=False) 
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read() # 存储请求结果
        print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = str(result_str, 'utf-8')
    print(result_str)
    #将 JSON 对象转换为 Python 字典
    content = json.loads(result_str)
    #解析提取出所需的文本内容
    #print ("content['err_msg']: ", content['err_msg'])
    usefulData = (content['result'])[0]
    return usefulData


if __name__  == '__main__':
    sr_result = speechRecognition_Speed()
    """
    #提取'你好管家'用于后续的输入
    sr_result = 
    #else 直接进行语音输入
    语音指令
    1、天气怎么样
    2、开启/关闭 人脸识别
    3、热点新闻
    4、开关灯
    5、
    """
    if("天气" in sr_result):
        print("天气程序调取")
    
        
    with open("/home/pi/IntelligenceHomeSys/SoundFunction/result.txt","w") as of:
        of.write(sr_result)

        
