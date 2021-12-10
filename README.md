### video-tool

video-tool是基于python-opencv编写的软件，可以支持打开usb外接摄像头，通过修改config.ini配置文件进行指定摄像头。

**main.py 与 single_thread.py：**都是单线程的读写，在计算机性能较好、录制分辨率、帧率不高的情况下，可以满足录制，否则存在丢帧现象



**single_thread_list.py**: 也是单线程，不同的是将写的数据暂时放入到缓存list中，待关闭摄像头后，一次性写入。如果录制视频2分钟左右，占用内存200M也能满足需要，如果是较长视频不建议采用。



**multi_thread_run.py：**多线程下，读写线程数据分离，解决单线程下存在丢帧的现象。