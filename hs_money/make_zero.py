import RPi.GPIO as GPIO
import tm1637
import time
import pickle
import os

GPIO.setmode(GPIO.BCM) 

GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT) 

# 사용할 GPIO 핀 번호
BTN_RESET = 14
BTN_1000 = 15
BTN_100 = 18
MONEY = 0 
FILENAME = 'money.dat'

# 버튼 핀 입력으로 설정
GPIO.setup(BTN_RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_1000, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_100, GPIO.IN, pull_up_down=GPIO.PUD_UP)

tm = tm1637.TM1637(clk=3,dio=2)

D = [0b00111111, 0b00000110, 0b01011011, 0b01001111, 0b01100110, 0b01101101, 0b01111101, 0b00000111, 0b01111111, 0b01101111]

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

		if AL == 5:
			D3 = 0
		elif AL == 4:
			D3 = D2 = 0
		elif AL == 3:
			D3 = D2 = D1 = 0
		elif AL == 2:
			D6 = D3 = D2 = D1 = 0
		elif AL == 1:
			D5 = D6 = D3 = D2 = D1 = 0
		else:
			pass
	
	if AL > 3:
		num_list = [D1+128,D2,D3,D4,D5,D6]
	else:
		num_list = [D1,D2,D3,D4,D5,D6]

	return num_list

def Display():
    tm.write(ml(MONEY))
    with open(FILENAME, 'wb') as f:
        pickle.dump(MONEY, f)

def Cb_BTN_RESET(channel):
    global MONEY
    MONEY = 0
    Display()


def Cb_BTN_1000(channel):
    global MONEY
    MONEY = MONEY + 1000
    Display()

def Cb_BTN_100(channel):
    global MONEY
    MONEY = MONEY + 100
    Display()

def init_money_data():
    with open(FILENAME, 'wb') as f:
        MONEY = 0
        pickle.dump(MONEY, f)

def money_loop():

    if os.path.isfile(FILENAME):
        print("OK")
    else:
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
            time.sleep(0.1)
                
    except KeyboardInterrupt:
        # 프로그램 종료 시 GPIO 리셋
        GPIO.cleanup()


#while True:
	#tm.write([0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111]) #천만십만일십백
	#tm.write([digits[3]+128,digits[2],digits[1],digits[6],digits[5],digits[4]])

#for i in range(999999):
#	#tm.write([0,0,0,0,0b11111111,0])
#	tm.write(ml(i))
#tm.write([0b01110110,0b01111001,D[2],0b01010000,0b01011100,0b01111000])

tm.write(ml(0))
#user_input = input("pending")