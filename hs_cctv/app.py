from flask import Flask, render_template, Response, request
from picamera import PiCamera
from io import BytesIO
import time
import subprocess
import threading

'''
print("Camera Initialize")
camera = PiCamera()
camera.resolution = camera.MAX_RESOLUTION #(640, 480)
camera.framerate = 24
camera.vflip = True
camera.hflip = True
print(f"Size {camera.MAX_RESOLUTION}")
'''


print(f"Camera Initialized")
app = Flask(__name__)
print(f"{app} ")


def get_cpu_temp_sub():
    temp = subprocess.check_output(['vcgencmd','measure_temp']).decode()
    return float(temp.split('=')[1].split('\'')[0])


@app.route('/get_cpu_temp')
def get_cpu_temp():
    global boost_until
    boost_until = time.time() + 6
    return str(get_cpu_temp_sub())





@app.route('/')
def index():
    cpu_temp = get_cpu_temp_sub()
    return render_template('index.html',cpu_temp=cpu_temp)

Times = 0

@app.route('/times')
def times():
    print(Times)
    return str(Times)


@app.route('/close_stream')
def close_stream():
    print("CLOSE_STREAM")
    global camera

    if camera != None:
        camera.close()
        camera = None
        print("CAMERA CLOSE, NONE")
    return "OK"


camera = None
lifetime = 0

def CameraChecker():
    global camera
    global lifetime

    while True:
        
        if camera != None:       
            lifetime = lifetime + 1

        
        if lifetime > 60:
            if camera != None:
                camera.close()
                camera = None
                print("CAMERA CLOSE, NONE")
        
        time.sleep(1)
        #print(f"Check Camera LifeTime {lifetime}")

t = threading.Thread(target=CameraChecker)
t.start()

@app.route('/video_feed')
def video_feed():
    print("VIDEO_FEED")
    global camera
    global lifetime

    lifetime = 0
    Times = 0  

    if camera == None:
        print("CAMERA CREATE")
        camera = PiCamera()
        camera.resolution = (1280,961) #(1640,1232) #camera.MAX_RESOLUTION #(640, 480)
        print(f"Size {camera.MAX_RESOLUTION}")
        camera.framerate = 24
        camera.vflip = True
        camera.hflip = True

    def capture():
        global camera
        global Times
        global lifetime

        stream = BytesIO()
        stream.seek(0)
        stream.truncate()
        Times = 0        
            
        for frame in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            print(f"Transfer {stream.getbuffer().nbytes}")
            Times += 1
            ls = str(stream.getbuffer().nbytes)
            lb = ls.encode('utf-8')
            yield(b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: '+ lb +b'\r\n\r\n'+ stream.getvalue() + b'\r\n')
            stream.seek(0)
            stream.truncate()
            lifetime = 0
            

    
    return Response(capture(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.after_request
def after_request(response):
    print("after_request")
    return response

@app.teardown_request
def teardown_request(exception):
    print("teardown_request")

@app.teardown_appcontext
def teardown_appcontext(exception):
    print("teardown_appcontext")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
