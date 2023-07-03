from datetime import datetime, timedelta
from flask import Flask, render_template, request, make_response, Response,redirect
import subprocess
import psutil
import pygame
from gtts import gTTS
import os
import logging
LOGNAME = '/home/zextor/hs_front/front.log'
#filename=LOGNAME,
logging.basicConfig(filename=LOGNAME,level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

COOKIE_NAME = '00198005090'
COOKIE_PASS = 'homeservice'

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

# 사용자 이름 및 암호 목록
users = {
    "stevia06": "",
}

def check_auth(username, password):
    idcheck = username in users
    passcheck = users[username] == password
    return idcheck and passcheck


@app.route('/')
def index():
    cookie_value = request.cookies.get(COOKIE_NAME)
    print(f"COOKIE:{cookie_value}")
    print(request.remote_addr)
    
    if cookie_value != COOKIE_PASS:
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            logging.error('try login {},{}'.format(auth.username, auth.password))
            return authenticate()

    html = render_template('index.html')
    response = make_response(html)
    expires = datetime.now() + timedelta(days=30)
    response.set_cookie(COOKIE_NAME, COOKIE_PASS, expires=expires)
    return response


    #return render_template('index.html')

@app.route('/percent')
def percent():
    f = psutil.cpu_percent(interval=1)
    return str(f)


@app.route('/temp')
def temp():
    res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    f = float(res.replace("temp=", "").replace("'C\n", ""))
    return str(f)


@app.route('/result', methods=['POST'])
def result():
    #mac_address = "AC:67:84:0C:52:BD"
    #cmd = "bluetoothctl connect {}".format(mac_address)
    #result = subprocess.check_output(cmd, shell=True)
    result = subprocess.check_output(["/home/zextor/connect.sh","connect","AC:67:84:0C:52:BD"], shell=True).decode("utf-8")
    
    logging.info(result)
    text1 = request.form['text']
    logging.info(text1)
    tts = gTTS(text=text1, lang='ko', slow=False)
    #tts.speed = 0.5
    tts.save('/home/zextor/hs_front/test.mp3')

    if  os.path.exists('/home/zextor/hs_front/test.mp3'):
        #result = subprocess.run(["/usr/bin/ffplay","-nodisp","-autoexit","/home/zextor/hs_front/test.mp3"])
        result = subprocess.run(["/usr/bin/play","/home/zextor/hs_front/test.mp3"])

        logging.info('FFPLAY return {}'.format(result))
        #r = pygame.init()
        #logging.info('pygame.init ret {}'.format(r))

        '''init_result = pygame.get_init()
        logging.info(pygame.get_error())

        for index, value in enumerate(init_result):
            logging.info('{},{}'.format(index, value))
            if value == 0:
                module_name = pygame.get_error()
                logging.info(f"Module at index {index} failed to initialize. Error message: {module_name}")

'''
        #r = pygame.mixer.music.load('/home/zextor/hs_front/test.mp3')
        #logging.info('pygame.mixer.music.load ret {}'.format(r))

        #pygame.mixer.music.set_volume(1)
        #r = pygame.mixer.music.play()
        #logging.info('pygame.mixer.music.play ret {}'.format(r))

        #while pygame.mixer.music.get_busy():
        #    pass

        os.remove('/home/zextor/hs_front/test.mp3')
    #return render_template('result.html')
    return redirect('/')


if __name__ == '__main__':
    logging.info('Front Begin')
    app.run(host='0.0.0.0', port=8003, debug=False)