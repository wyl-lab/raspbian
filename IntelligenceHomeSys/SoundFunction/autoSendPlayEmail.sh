#!/bin/bash

# crawler and send
<<<<<<< HEAD
python3 /home/pi/IntelligenceHomeSys/SoundFunction/环境-语音播报.py
=======
python3 /home/pi/IntelligenceHomeSys/SoundFunction/pythonScripts/环境-语音播报.py
>>>>>>> sound

#play local
omxplayer -p -o hdmi /home/pi/IntelligenceHomeSys/SoundFunction/syntheticVoice.mp3

read -p "autoSendPlayEmail.sh has finished!" 

#exit 0

# crontab -e 定时任务

# 00 7 * * * /home/pi/IntelligenceHomeSys/SoundFunction/autoSend&PlayEmail.sh
# 30 16 * * * /home/pi/IntelligenceHomeSys/SoundFunction/autoSend&PlayEmail.sh
<<<<<<< HEAD
=======


>>>>>>> sound
