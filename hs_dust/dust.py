import requests
import json
import pprint
import RPi.GPIO as GPIO
import time
import logging
#import logging.handlers
from datetime import datetime, timedelta
LOGNAME='/home/zextor/hs_dust/dust.log'
#filename=LOGNAME
logging.basicConfig(filename=LOGNAME,level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

MISE_RED    = 19
MISE_YELLOW = 13
MISE_GREEN  = 26

CHO_RED     = 9
CHO_YELLOW  = 10
CHO_GREEN   = 11

GPIO.setup(MISE_RED,GPIO.OUT)
GPIO.setup(MISE_YELLOW,GPIO.OUT)
GPIO.setup(MISE_GREEN,GPIO.OUT)
GPIO.setup(CHO_RED,GPIO.OUT)
GPIO.setup(CHO_YELLOW,GPIO.OUT)
GPIO.setup(CHO_GREEN,GPIO.OUT)

PMR = GPIO.PWM(MISE_RED,    100)
PMY = GPIO.PWM(MISE_YELLOW, 100)
PMG = GPIO.PWM(MISE_GREEN,  100)

CMR = GPIO.PWM(CHO_RED,    100)
CMY = GPIO.PWM(CHO_YELLOW, 100)
CMG = GPIO.PWM(CHO_GREEN,  100)

PMR.start(0)
PMY.start(0)
PMG.start(0)

CMR.start(0)
CMY.start(0)
CMG.start(0)

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
params ={'serviceKey' : '', 'returnType' : 'json', 'numOfRows' : '100', 'pageNo' : '1', 'stationName' : '광교동', 'dataTerm' : 'DAILY', 'ver' : '1.0' }
                
# '2023042018'
# (낮음) 0, (보통) 1, (높음) 2, (매우높음) 3

# 공공 데이터 포털, 카카오로그인
# 일일한도 500회, 5분마다 한번 , 60x5
# https://www.data.go.kr/iim/dor/selectMyOfferReqstList.do
# 측정소 수지, 광교동, 기흥

Current10 = None
Current25 = None

Current10V = None
Current25V = None

def allergy(v):
    logging.info('Allery {}'.format(v))
    CMR.ChangeDutyCycle(0)
    CMY.ChangeDutyCycle(0)
    CMG.ChangeDutyCycle(0)
    if v == 3 :
        CMR.ChangeDutyCycle(10)
    elif v == 2:
        CMY.ChangeDutyCycle(30)
    else:
        CMG.ChangeDutyCycle(100)


def pm10(pm10Value):
    global Current10
    global Current10V
    PMR.ChangeDutyCycle(0)
    PMY.ChangeDutyCycle(0)
    PMG.ChangeDutyCycle(0)

    if pm10Value > 100:
        PMR.ChangeDutyCycle(10)
        Current10 = PMR
        Current10V = 10
    elif pm10Value > 50:
        PMY.ChangeDutyCycle(30)
        Current10 = PMY
        Current10V = 30
    else:
        PMG.ChangeDutyCycle(100)
        Current10 = PMG
        Current10V = 100


def pm25(pm25Value):
    global Current25
    global Current25V
    CMR.ChangeDutyCycle(0)
    CMY.ChangeDutyCycle(0)
    CMG.ChangeDutyCycle(0)

    if pm25Value > 50:
        CMR.ChangeDutyCycle(10)
        Current25 = CMR
        Current25V = 10
    elif pm25Value > 25:
        CMY.ChangeDutyCycle(30)
        Current25 = CMY
        Current25V = 30
    else:
        CMG.ChangeDutyCycle(100)
        Current25 = CMG
        Current25V = 100


if __name__ == '__main__':
#def Check():
    logging.info("Dust Begin")
                
    while True:
        try:
            while True:
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    #print(data)
                    try:
                        #print(data)
                        pm10Value = int(data['response']['body']['items'][0]['pm10Value'])
                        pm25Value = int(data['response']['body']['items'][0]['pm25Value'])
                        dataTime = data['response']['body']['items'][0]['dataTime']
                        
                        logging.info(f"{dataTime} PM10:{pm10Value}, PM2.5:{pm25Value}")
                        #pm10Value=0     
                        #pm25Value=0
                        pm10(pm10Value)
                        pm25(pm25Value)
                    except Exception as e:
                        logging.error(e)
                        time.sleep(300)
                        continue
                '''
                print("ALLERGY")
                url2 = 'https://apis.data.go.kr/1360000/HealthWthrIdxServiceV3/getOakPollenRiskIdxV3'
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d18")
                params2 = {'serviceKey':'','numOfRows':'10','pageNo':'1','dataType':'json','areaNo':'4146557000','time': yesterday }
                #print(params2)
                response2 = requests.get(url2, params=params2)
                
                #print(response2.status_code)
                if response2.status_code == 200:
                    #print("200")
                    data = response2.json()
                    try:
                        Today = int(data['response']['body']['items']['item'][0]['tomorrow'])
                        allergy(Today)
                    except Exception as e:
                        print(e)
                        time.sleep(5)
                        continue
                '''
                #time.sleep(60)
                start_time = time.time()  # 현재 시간 기록

                while True:

                    #logging.info('BEGIN LOOP')

                    for V in range(Current10V,1,-1):
                        Current10.ChangeDutyCycle(V)
                        #logging.info('10 DOWN {}'.format(V))
                        time.sleep(1/Current10V)

                    for V in range(1, Current10V):
                        Current10.ChangeDutyCycle(V)
                        #logging.info('10 UP {}'.format(V))
                        time.sleep(1/Current10V)

                    for V in range(Current25V,1,-1):
                        Current25.ChangeDutyCycle(V)
                        #logging.info('25 DOWN {}'.format(V))
                        time.sleep(1/Current25V)
                    for V in range(1, Current25V):
                        Current25.ChangeDutyCycle(V)
                        #logging.info('25 UP {}'.format(V))
                        time.sleep(1/Current25V)


                    current_time = time.time()  # 현재 시간 갱신
                    elapsed_time = current_time - start_time  # 경과 시간 계산

                    if elapsed_time >= 300:  # 60초가 경과하면 종료
                        #logging.info('1 MIN OUT')
                        break
        
        except Exception as e:
            logging.error(e)
            time.sleep(300)
            pass
