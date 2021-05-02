'''
setConnectionTimeoutInMillis	建立连接的超时时间（单位：毫秒
setSocketTimeoutInMillis	通过打开的连接传输数据的超时时间（单位：毫秒）
参数	类型	    描述	                              是否必须
tex	    String	合成的文本，使用UTF-8编码，
                请注意文本长度必须小于1024字节	            是
                
cuid	String	用户唯一标识，用来区分用户，
                填写机器 MAC 地址或 IMEI 码，长度为60以内	否

spd	    String	语速，取值0-9，默认为5中语速	            否

pit	    String	音调，取值0-9，默认为5中语调	            否

vol	    String	音量，取值0-15，默认为5中音量	            否

per	    String	发音人选择, 0为女声，1为男声，
                3为情感合成-度逍遥，	
                4为情感合成-度丫丫，默认为普通女            否
'''
import json
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '24025146'
API_KEY = '0Wv3AGwPg5Y4Sa8GzB09qTGw'
SECRET_KEY = 'Lk3oDN6Y7GGBZWB4BpNM7OpbOGSNvkeV'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

content = "Tempreture 9° / 16° 天气情况: 阵雨 温   度 : 9° / 16° 风   向 : 东北风 风   速 : 3-4级 空气质量: 52良！";

cuid = 'raspberry'

result  = client.synthesis(content, 'zh', 1, {
   
    'spd': 4,
    'pit': 6,
    'vol': 8,
    'per': 110,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    print("\n准备生成MP3音频格式文件")
    with open('/home/pi/IntelligenceHomeSys/SoundFunction/audio1.mp3', 'wb') as f:
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
    print ("pyDicts['err_msg']: ", pyDicts['err_msg'])
    
'''
错误码	含义
500	不支持的输入
501	输入参数不正确
502	token验证失败
503	合成后端错误
'''    

