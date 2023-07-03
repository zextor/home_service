import RPi.GPIO as GPIO
import tm1637
import time
import pickle
import os
import logging

FILENAME = '/home/zextor/hs_money/money.dat'
LOGNAME = '/home/zextor/hs_money/money.log'
# filename=LOGNAME,
logging.basicConfig(filename=LOGNAME,level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

'''
logging.debug('디버그 메시지')
logging.info('인포 메시지')
logging.warning('경고 메시지')
logging.error('에러 메시지')
logging.critical('심각한 에러 메시지')
'''

GPIO.setmode(GPIO.BCM) 

GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT) 

# 사용할 GPIO 핀 번호
BTN_RESET = 14
BTN_1000 = 15
BTN_100 = 18
MONEY = 0 
SIGNALS = True

# 버튼 핀 입력으로 설정
GPIO.setup(BTN_RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_1000, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_100, GPIO.IN, pull_up_down=GPIO.PUD_UP)

tm = tm1637.TM1637(clk=3,dio=2)
tm.brightness(0)


D = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110, 0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]


# D3 D2 D1 D6 D5 D4

def ml(num):
    num_str = str(num)
    AL = len(num_str)

    if AL == 6: 
        D1 = D[int(num_str[2])]
        D2 = D[int(num_str[1])]
        D3 = D[int(num_str[0])]
        D4 = D[int(num_str[5])]
        D5 = D[int(num_str[4])]
        D6 = D[int(num_str[3])]
    else:
        num_str = "0"*(6-AL) + num_str
        D1 = D[int(num_str[2])]
        D2 = D[int(num_str[1])]
        D3 = D[int(num_str[0])]
        D4 = D[int(num_str[5])]
        D5 = D[int(num_str[4])]
        D6 = D[int(num_str[3])]

        CURSOR = 0
        if SIGNALS:
            CURSOR = 8


        if AL == 5:
            D3 = CURSOR
        elif AL == 4:
            D3 = 0
            D2 = CURSOR
        elif AL == 3:
            D3 = D2 = 0
            D1 = CURSOR
        elif AL == 2:
            D1 = D3 = D2 = 0
            D6 = CURSOR
        elif AL == 1:
            D1 = D6 = D3 = D2 = 0
            D5 = CURSOR
        else:
            pass
    
    if AL > 3:
        num_list = [D1+128,D2,D3,D4,D5,D6]
    else:
        num_list = [D1,D2,D3,D4,D5,D6]

    return num_list

def Save():
    with open(FILENAME, 'wb') as f:
        pickle.dump(MONEY, f)

def Display():
    tm.write(ml(MONEY))

def Cb_BTN_RESET(channel):
    global MONEY
    logging.info('Press reset Button, Before {}'.format(MONEY))
    MONEY = 0
    Display()
    Save()


def Cb_BTN_1000(channel):
    global MONEY
    logging.info('Press 1,000 Button, Before {}'.format(MONEY))
    MONEY = MONEY + 1000
    Display()
    Save()

def Cb_BTN_100(channel):
    global MONEY
    logging.info('Press 100 Button, Before {}'.format(MONEY))
    MONEY = MONEY + 100
    Display()
    Save()

'''    
 First = True
 while GPIO.input(BTN_100) == GPIO.LOW:
        MONEY = MONEY + 100
        Display()
        if First:
            time.sleep(1)
            First = False'''
    


def init_money_data():
    global MONEY
    with open(FILENAME, 'wb') as f:
        MONEY = 0
        pickle.dump(MONEY, f)


if __name__ == '__main__':
#def money_loop():
    #global MONEY
    logging.info('Money Thread Start')

    if os.path.isfile(FILENAME):
        logging.info("Money is Exists. OK!")
    else:
        logging.info("Money is not Exists. Initialize OK!")
        with open(FILENAME, 'wb') as f:
            MONEY = 0
            pickle.dump(MONEY, f)

    try:
        # 버튼 핀에 대한 이벤트 감지 설정
        with open(FILENAME, 'rb') as f:
            MONEY = pickle.load(f)

        tm.write(ml(MONEY))

        GPIO.add_event_detect(BTN_RESET, GPIO.FALLING, callback=Cb_BTN_RESET, bouncetime=200)
        GPIO.add_event_detect(BTN_1000, GPIO.FALLING, callback=Cb_BTN_1000, bouncetime=200)
        GPIO.add_event_detect(BTN_100, GPIO.FALLING, callback=Cb_BTN_100, bouncetime=200)

        while True:
            time.sleep(1)
            if SIGNALS:
                SIGNALS = False
            else:
                SIGNALS = True
            Display()

            #print("Money Thread")
                
    except KeyboardInterrupt:
        # 프로그램 종료 시 GPIO 리셋
        GPIO.cleanup()
    except Exception as e:
        logging.critical(e)



#while True:
    #tm.write([0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111]) #천만십만일십백
    #tm.write([digits[3]+128,digits[2],digits[1],digits[6],digits[5],digits[4]])

#for i in range(999999):
#   #tm.write([0,0,0,0,0b11111111,0])
#   tm.write(ml(i))
#tm.write([0b01110110,0b01111001,D[2],0b01010000,0b01011100,0b01111000])

#tm.write(ml(123456))
#user_input = input("pending")


#while True:
#    money_loop()
#    time.sleep(1)