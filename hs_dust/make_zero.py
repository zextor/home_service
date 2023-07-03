import requests
import json
import pprint
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) 

MISE_RED = 19
MISE_YELLOW = 13
MISE_GREEN = 26

CHO_RED = 9
CHO_YELLOW = 10
CHO_GREEN = 11

GPIO.setup(MISE_RED,GPIO.OUT)
GPIO.setup(MISE_YELLOW,GPIO.OUT)
GPIO.setup(MISE_GREEN,GPIO.OUT)
GPIO.setup(CHO_RED,GPIO.OUT)
GPIO.setup(CHO_YELLOW,GPIO.OUT)
GPIO.setup(CHO_GREEN,GPIO.OUT)

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
params ={'serviceKey' : '', 'returnType' : 'json', 'numOfRows' : '100', 'pageNo' : '1', 'stationName' : '광교동', 'dataTerm' : 'DAILY', 'ver' : '1.0' }

# 공공 데이터 포털, 카카오로그인
# https://www.data.go.kr/iim/dor/selectMyOfferReqstList.do
# 측정소 수지, 광교동, 기흥
def pm10(pm10Value):

    GPIO.output(MISE_RED,0)
    GPIO.output(MISE_YELLOW,0)
    GPIO.output(MISE_GREEN,0)

    if pm10Value > 74:
        GPIO.output(MISE_RED,1)
    elif pm10Value > 49:
        GPIO.output(MISE_YELLOW,1)
    else:
        GPIO.output(MISE_GREEN,1)


def pm25(pm10Value):
    GPIO.output(CHO_RED,0)
    GPIO.output(CHO_YELLOW,0)
    GPIO.output(CHO_GREEN,0)

    if pm10Value > 24:
        GPIO.output(CHO_RED,1)
    elif pm10Value > 19:
        GPIO.output(CHO_YELLOW,1)
    else:
        GPIO.output(CHO_GREEN,1)

def Check():
    
    while True:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            #print(data)
            try:
                pm10Value = int(data['response']['body']['items'][0]['pm10Value'])
                pm25Value = int(data['response']['body']['items'][0]['pm25Value'])
                dataTime = data['response']['body']['items'][0]['dataTime']
                
                print(f"{dataTime} PM10: {pm10Value}, PM2.5: {pm25Value}")
                #pm10Value=0     
                #pm25Value=0
                pm10(pm10Value)
                pm25(pm25Value)
            except Exception as e:
                continue
        
        time.sleep(60)
                

GPIO.output(MISE_RED,0)
GPIO.output(MISE_YELLOW,0)
GPIO.output(MISE_GREEN,0)
GPIO.output(CHO_RED,0)
GPIO.output(CHO_YELLOW,0)
GPIO.output(CHO_GREEN,0)
