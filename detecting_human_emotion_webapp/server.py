from flask import Flask, render_template, Response, jsonify, request
from .camera import VideoCamera

app = Flask(__name__)

video_camera = None
global_frame = None


@app.route('/')
def index():
    return render_template('video_recorder.html')


@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera
    if video_camera is None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        print("recording started")
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")


def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #     print(global_frame)
        #     # yield (b'--frame\r\n'
        #     #        b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)