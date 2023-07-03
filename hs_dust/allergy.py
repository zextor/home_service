import requests
import json
import pprint
from datetime import datetime, timedelta
import time


def Check():
    
    while True:
        try:
            while True:

                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d18")
                
                # '2023042018'
                # (낮음) 0, (보통) 1, (높음) 2, (매우높음) 3
                url = 'https://apis.data.go.kr/1360000/HealthWthrIdxServiceV3/getOakPollenRiskIdxV3'
                params = {'serviceKey':'','numOfRows':'10','pageNo':'1','dataType':'json','areaNo':'4146557000','time': yesterday }

                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    #print(data)
                    try:
                        Today = int(data['response']['body']['items']['item'][0]['tomorrow'])
                        Tomorrow = int(data['response']['body']['items']['item'][0]['dayaftertomorrow'])
                        NextTomorrow = int(data['response']['body']['items']['item'][0]['twodaysaftertomorrow'])
                        print(f"Today {Today} Tomorrow {Tomorrow} Glpy {NextTomorrow}")

                    except Exception as e:
                        print(e)
                        time.sleep(5)
                        continue
                
                time.sleep(5)
        
        except Exception as e:
            print(e)
            time.sleep(5)
            pass

Check()
