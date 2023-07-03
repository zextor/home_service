from flask import Flask, render_template, request,redirect
import time
import pygame
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    text1 = request.form['text']
    tts = gTTS(text=text1, lang='ko', slow=False)
    #tts.speed = 0.5
    tts.save('test.mp3')

    if  os.path.exists('test.mp3'):
        pygame.init()
        pygame.mixer.music.load('test.mp3')
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pass

        os.remove('test.mp3')
    #return render_template('result.html')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)
