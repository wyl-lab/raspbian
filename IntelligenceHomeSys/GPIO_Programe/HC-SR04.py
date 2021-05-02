#导入 GPIO库
import RPi.GPIO as GPIO
import time
  
#设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)

#定义 GPIO 引脚
GPIO_TRIGGER = 2
GPIO_ECHO = 3
  
#设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
  
def distance():
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)
  
    # 持续 10 us 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
  
    time0 = time.time()
    time1 = time.time()
  
    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        time0 = time.time()
  
    # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        time1 = time.time()
  
    # 计算超声波的往返时间 = 时刻_1 - 时刻_0
    #print(type(time_elapsed))#float
    time_elapsed = time1 - time0
    
    # 声波的速度为 343m/s， 转化为 34300cm/s。
    distance = (time_elapsed /58.0)
    
    #print(type(distance))#float
    #print("The reslut is  ",distance)
    return distance

def Compare_data(dist,list1):
    list1.append(dist)
    print(list1)

if __name__ == '__main__':
    list1 = []
    try:
        dist = distance()
        print("Measured Distance = {:.2f} cm".format(dist))
        Compare_data(dist,list1)
        time.sleep(5)
  
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    
    GPIO.cleanup()
