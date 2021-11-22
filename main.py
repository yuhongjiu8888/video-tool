import os

import cv2
import datetime
import configparser
import csv

# 默认设置
id = 0
width = 640
height = 480
fps = 30

status = os.path.exists("config.ini")
if status == True:
    config = configparser.ConfigParser()
    config.read("config.ini")

    config.sections()
    config.options("camera")
    id = config.getint("camera", "id")
    width = config.getint("camera", "width")
    height = config.getint("camera", "height")
    fps = config.getint("camera", "fps")
    print("配置文件中读取配置")

cap = cv2.VideoCapture(id)
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, width)
cap.set(4, height)

#构建视频保存的对象
fourcc = cv2.VideoWriter_fourcc('M','P','4','2')  #为保存视频做准备，构建了一个对象，其中10为帧率，自己可按照需要修改


str_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

out = cv2.VideoWriter(str_time+".avi", fourcc, fps, (width, height))

f = open(str_time+'.csv', 'w', encoding='utf-8', newline='')
header = ['Frame', 'DateTime']
writer = csv.writer(f)
writer.writerow(header)

frame_count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:

       font = cv2.FONT_HERSHEY_SIMPLEX
       text = 'Width: '+ str(cap.get(3)) + ' Height:' + str(cap.get(4))

       datet = str(datetime.datetime.now())
       str_date = datet.replace('.', ' ')  # .分隔会导致csv文件格式显示不对,需要格式处理
       # datet = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')[:-3] # .分隔会导致csv文件格式显示不对需要格式处理
       frame = cv2.putText(frame, text, (10, 50), font, 0.5,
                           (0, 255, 255), 2, cv2.LINE_AA)
       frame = cv2.putText(frame, datet, (10, 100), font, 1,
                           (0, 255, 255), 2, cv2.LINE_AA)

       my_list = [frame_count, str_date]

       writer.writerow(my_list)

       f.flush()

       cv2.imshow('frame', frame) #显示视频
       out.write(frame) #保存视频

       frame_count = frame_count+1
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break
    else:
        break

cap.release()
f.close()
cv2.destroyAllWindows()
