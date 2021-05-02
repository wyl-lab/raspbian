
# -*- coding:utf-8 -*-
#!/usr/bin/python
# coding=utf-8
import sys

if __name__  == '__main__':
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
    try:        
        with open('result.txt','r') as f:
            fileContent= f.read()
            #print(fileContent)
        if("天气" in fileContent):
            print("天气程序调取")
            
    finally:
        if f:
            f.close()

    
        

    
    
        
   
