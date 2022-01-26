'''
Descripttion: 
version: 
Author: LiQiang
Date: 2022-01-25 12:47:16
LastEditTime: 2022-01-25 12:48:37
'''
import cv2
import queue
import threading

# 无缓存读取视频流类
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # 帧可用时立即读取帧，只保留最新的帧
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # 删除上一个（未处理的）帧
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

cap = VideoCapture(0)
while True:
  frame = cap.read()
  cv2.imshow("frame", frame)
  if chr(cv2.waitKey(1)&255) == 'q':
    break
