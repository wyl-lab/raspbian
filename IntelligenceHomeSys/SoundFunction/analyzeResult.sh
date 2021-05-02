#!/bin/bash

#提取'你好管家'用于后续的输入
#预设的语音指令
    #1、天气怎么样	#你好，管家外面天气怎么样啊。
    #2、开启/关闭人脸识别	#你好，管家我在家呢，把人脸检测关了吧。
    #3、热点新闻	#你好，管家我想听一下今天的新闻。
    #4、开关灯	#你好，管家把灯关了吧我要睡觉了。
    #5、室内环境	#你好，管家屋里现在的环境咋样啊。

#sudo chmod 777 /home/pi/IntelligenceHomeSys/SoundFunction/result.txt
#file = $(/home/pi/IntelligenceHomeSys/SoundFunction/result.txt)

if grep "天气" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt
then
    # python3 /home/pi/IntelligenceHomeSys/SoundFunction/pythonScripts/环境-语音播报.py
    python3 /home/pi/IntelligenceHomeSys/SoundFunction/pythonScripts/环境-室内外-语音播报及预警.py
fi

## 室内环境
if grep "环境" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
    if grep "屋" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
	echo "反馈室内环境"

    fi
fi


## 开关 灯功能
if grep "灯" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
    if grep "开" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
	echo "开灯操作"
	python3 /home/pi/IntelligenceHomeSys/SoundFunction/pythonScripts/语音控制引脚开灯关灯.py
    fi

    if grep "关" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
	echo "关灯操作"
    fi
fi


## 开关 人脸检测识别功能
if grep "人脸" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
    if grep "开" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
	echo "打开人脸检测"
    fi
    if grep "关" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
	echo "关闭人脸检测"
    fi
fi


## 热点新闻
if grep "新闻" /home/pi/IntelligenceHomeSys/SoundFunction/result.txt;then
    python3 /home/pi/IntelligenceHomeSys/SoundFunction/pythonScripts/新闻播报.py
fi



