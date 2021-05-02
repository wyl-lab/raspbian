#coding=utf8

import cv2

import cv2.cv as cv

import requests

import json

import picamera

import os


camera=picamera.PiCamera()

camera.capture("/home/pi/face/faceOfPeople/2018_11_21_12_12--4.jpg")

filename='/home/pi/face/faceOfPeople/2018_11_21_12_12--4.jpg'


url = 'https://api-cn.faceplusplus.com/facepp/v3/search'

payload = {
            'api_key': 'UNgzAecWqPTIdxNy5j1-dMYpg-8m00IN',

            'api_secret': 'VW7E-usdLrCFuUmSKp8CifV4WqKSQ4ix',
            
            'faceset_token':'a209adf78ed90604b45826073f7e3adc',
            
            }

files = {'image_file':open('/home/pi/face/faceOfPeople/2018_11_21_12_12--4.jpg', 'rb')}

r = requests.post(url,files=files,data=payload)

data=json.loads(r.text)

print(r.text)


if os.path.exists(filename):#判断文件是否存在
    
    os.remove(filename)#移除目录下的文件

if data["results"][0]["face_token"] == 'a209adf78ed90604b45826073f7e3adc' and data["results"][0]["confidence"]>=data["thresholds"]["1e-5"]:
    
    print('\n主人')

else:
    
    print('\n闯入者')