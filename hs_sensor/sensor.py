import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import tm1637
import logging
LOGNAME = '/home/zextor/hs_sensor/sensor.log'
#filename=LOGNAME,
logging.basicConfig(filename=LOGNAME,level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

GPIO.setmode(GPIO.BCM) 

DATA_PIN = 17
DIO = 27
CLK = 22

GPIO.setup(DIO,GPIO.OUT)
GPIO.setup(CLK,GPIO.OUT) 

tm = tm1637.TM1637(clk=CLK,dio=DIO)
tm.brightness(1)
sensor = Adafruit_DHT.DHT22

#D = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110, 0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]

D=[ 0b00111111,
    0b00110000,
    0b01011011,
    0b01111001,
    0b01110100,
    0b01101101,
    0b01101111,
    0b00111000,
    0b01111111,
    0b01111101]

# D3 D2 D1 D6 D5 D4
# list[ 1 2, 3, 4, 5,6 ]
def DP(Temp,Hum):
    
    Temp = int(Temp)
    T1 = int(Temp/10)
    T2 = int(Temp%10)
   
    Hum = int(Hum)
    H1 = int(Hum/10)
    H2 = int(Hum%10)

    #logging.info('{} {}'.format(Temp,Hum))

    CURSOR = 0
    if SIGNALS:
        CURSOR = 1

    tm.write([CURSOR,D[H1],D[H2],D[T1],D[T2],0b10001111])


if __name__ == '__main__':
    old_h = 0.0
    old_t = 0.0
    SIGNALS = True
    logging.info('sensor.py Sensor() started')
    while True:
        try:
            h,t = Adafruit_DHT.read_retry(sensor, DATA_PIN)

            if (h is not None) and (t is not None):

                needlog = False

                if old_h != h:
                    old_h = h
                    needlog = True

                if old_t != t:
                    old_t = t
                    needlog = True

                DP(t,h)

                if SIGNALS:
                    SIGNALS = False
                else:
                    SIGNALS = True
                
                if needlog:
                    logging.info("Temp = {0:0.1f}*c Humidity = {1:0.1f}%".format(t,h))

            else:
                logging.error("read error")

            time.sleep(1)

        except Exception as e:
            logging.error(e)
            continue