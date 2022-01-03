'''
Descripttion: 
version: 
Author: LiQiang
Date: 2022-01-03 10:07:08
LastEditTime: 2022-01-03 10:51:56
'''
from flask import Flask, Response, render_template
from cam.base_camera import BaseCamera
from cam.url_stream import LoadStreams
import cv2

app = Flask(__name__)


class Camera(BaseCamera):
    @staticmethod
    def frames():
        # 此处为自己的视频流url 格式 "rtsp://%s:%s@%s//Streaming/Channels/%d" % (name, pwd, ip, channel)
        # 例如
        # source = 'rtsp://admin:123456@192.168.1.64//Streaming/Channels/101'
        source = '0'
        dataset = LoadStreams(source)
        for im0s in dataset:
            im0 = im0s[0].copy()
            frame = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
            result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            yield cv2.imencode('.jpg', result)[1].tobytes()


@app.route('/url')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(genWeb(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def genWeb(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    #    Run locally
    # app.run(debug=True, host='127.0.0.1', port=5000)
    # Run on the server
    app.run(debug=True, host='0.0.0.0', port=5000)
