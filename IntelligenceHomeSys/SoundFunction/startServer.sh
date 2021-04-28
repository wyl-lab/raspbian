#!/bin/bash


# flask: turn on local server
. /home/pi//env-flask/bin/activate
cd /home/pi/IntelligenceHomeSys/WebService
flask run


# qingting NAT-DDNS
/bin/bash /usr/local/flynat/manage.sh start
/bin/bash /usr/local/flynat/manage.sh status


# security subsystem
#cd /home/pi/IntelligenceHomeSys/SecuritySubsystem/mjpg-streamer-master/mjpg-streamer-experimental
#./mjpg_streamer -i "./input_raspicam.so -w 240 -h 180 -fps 4" -o "./output_http.so -w ./www"  
#./mjpg_streamer -i "./input_raspicam.so" -o "./output_http.so -w ./www"

