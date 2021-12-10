import os
import time

import cv2
import datetime
import configparser
import csv

import queue

import threading

thread_exit = False
ready = False

q = queue.Queue()


class myThread(threading.Thread):
    def __init__(self, camera_id, img_width, img_height, fps):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.img_width = img_width
        self.img_height = img_height
        self.fps = fps

        self.cap = cv2.VideoCapture(self.camera_id)

        print("摄像头默认帧率:{}".format(self.cap.get(cv2.CAP_PROP_FPS)))
        print("摄像头设置帧率:{}".format(self.fps))
        ret = self.cap.set(5, self.fps)        # 设置视频读取帧率
        print("摄像头设置后帧率:{},{}".format(ret, self.cap.get(cv2.CAP_PROP_FPS)))

        self.cap.set(3, self.img_width)  # 设置视频的宽
        self.cap.set(4, self.img_height)  # 设置视频的高

        print("摄像头默认编解码:{}".format(self.cap.get(cv2.CAP_PROP_FOURCC)))
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.cap.set(6, fourcc)  # 设置解码格式
        print("摄像头设置后编解码:{}".format(self.cap.get(cv2.CAP_PROP_FOURCC)))

        self.img_width = int(self.cap.get(
            cv2.CAP_PROP_FRAME_WIDTH))  # 重新获取最大的分辨率宽
        self.img_height = int(self.cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT))  # 重新获取最大的分辨率高
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)
                       )                # 获取支持的fps

    def run(self):
        global thread_exit
        global ready
        global q

        frame_count = 0
        str_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        f = open(str_time + '.csv', 'w', encoding='utf-8', newline='')
        header = ['Frame', 'DateTime']
        writer = csv.writer(f)
        writer.writerow(header)
        while not thread_exit:
            ret, frame = self.cap.read()
            if ret:

                print(self.cap.get(cv2.CAP_PROP_POS_MSEC))

                font = cv2.FONT_HERSHEY_SIMPLEX
                text = 'Width: ' + str(self.img_width) + \
                    ' Height:' + str(self.img_height)

                datet = str(datetime.datetime.now())
                str_date = datet.replace('.', ' ')  # .分隔会导致csv文件格式显示不对,需要格式处理
                # datet = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')[:-3] # .分隔会导致csv文件格式显示不对需要格式处理
                frame = cv2.putText(frame, text, (10, 50), font, 0.5,
                                    (0, 255, 255), 2, cv2.LINE_AA)
                frame = cv2.putText(frame, datet, (10, 100), font, 1,
                                    (0, 255, 255), 2, cv2.LINE_AA)
                my_list = [frame_count, str_date]
                writer.writerow(my_list)

                q.put(frame)
                ready = True
                frame_count = frame_count + 1

            else:
                f.close()
                thread_exit = True
                self.cap.release()


def main():
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

    global thread_exit
    global ready
    global q

    thread = myThread(id, width, height,  fps)
    thread.start()

    # 构建视频保存的对象
    # 为保存视频做准备，构建了一个对象，其中10为帧率，自己可按照需要修改
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    str_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    out = cv2.VideoWriter(str_time + ".avi", fourcc,
                          thread.fps, (thread.img_width, thread.img_height))

    interval = 1 / thread.fps   # 毫秒为单位
    print(interval)

    while not thread_exit:
        if ready:
            start = time.time()
            print(start)

            print(q.qsize())
            q_start = time.time()
            frame = q.get()
            q_end = time.time()
            qt = (round(q_end * 1000) - round(q_start * 1000)) / 1000
            print("队列获取数据耗时:{}".format(qt))

            cv2.imshow('Video', frame)

            start_time = time.time()
            out.write(frame)  # 保存视频
            end_time = time.time()
            tt = (round(end_time * 1000) - round(start_time * 1000)) / 1000
            print("写耗时:{}".format(tt))

            end = time.time()
            print(end)

            t = (round(end * 1000) - round(start * 1000)) / 1000
            print(t)
            # if t < interval:
            #     time.sleep(interval-t)

            # time.sleep(0.001)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                thread_exit = True
                out.release()
                cv2.destroyAllWindows()

        else:
            continue

    thread.join()


if __name__ == "__main__":
    main()
