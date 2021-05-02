# encoding:utf-8
import requests 
import json

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=0Wv3AGwPg5Y4Sa8GzB09qTGw&client_secret=Lk3oDN6Y7GGBZWB4BpNM7OpbOGSNvkeV'
response = requests.get(host)
if response:
    result = response.json()
    print(result)
    json_data = json.dumps(result)
    print('\n',"Json对象",json_data)
    print ('\n',"Python 原始数据：", repr(result),'\n')

    # 将 JSON 对象转换为 Python 字典
    pyDicts = json.loads(json_data)
    
    print ("['access_token']: ", pyDicts['access_token'])
    print ("['refresh_token']: ", pyDicts['refresh_token'])
    print ("['session_key']: ", pyDicts['session_key'])
