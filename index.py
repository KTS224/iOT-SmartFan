from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO

import requests
import json
from pprint import pprint
from datetime import datetime

app = Flask(__name__)

import time
# 노란색 LED, 빨간색 LED, PIR 센서의 GPIO 핀 번호 설정
led_R = 20
led_Y = 21
sensor = 4
# 불필요한 warning 제거, GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# LED의 GPIO 핀(led_R, led_Y)을 출력으로 설정하고 PIR 센서의 GPIO 핀(sensor)을 입력으로 설정
GPIO.setup(led_R, GPIO.OUT)
GPIO.setup(led_Y, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)
print("PIR Ready ....")
time.sleep(5)

try:
    while True:
    # PIR 센서는 사람의 움직임을 감지한 경우 3.3V(high 신호,1)을 출력하므로 PIR 센서의 GPIO 핀(sensor)은 3.3V(high 신호,1)을 입력받음
        if GPIO.input(sensor) == 1:
            GPIO.output(led_Y, 1) # 노란색 LED 켬
            GPIO.output(led_R, 0) # 빨간색 LED 끔
            print("Motion Detected !")
            time.sleep(0.2)
            # PIR 센서는 사람의 움직임을 감지하지 못한 경우 0V(low 신호,0)을 출력하므로 PIR 센서의 GPIO 핀(sensor)은 0V(low 신호,0)을 입력받음
        if GPIO.input(sensor) == 0:
            GPIO.output(led_R, 1) # 빨간색 LED 켬
            GPIO.output(led_Y, 0) # 노란색 LED 끔
            print("Motion Not Detected !")
            time.sleep(0.2)
except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()


@app.route("/")
def home():
    # 사람이 있는지 없는지 감지
    #
    # 
	return render_template("index.html")

@app.route("/refresh")
def refresh():
    try:
        now = datetime.now()
        return {'Now': now}
        
        return "ok"
        
    except expression as identifier:
        return "fail"
	
 
 # 지울예정...
@app.route("/get/temperature")
def get_temperature():
	try:
		now = datetime.now()
		date = now.strftime('%Y%m%d')
		hour = str(now.hour)
		isSuccess = False
		if int(hour) < 10:
			hour = "0" + hour + "00"
		else:
			hour = hour + "00"

		while isSuccess == False:
			
			url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
			params ={'serviceKey' : 'DBbxKUDjM9DmJ02j387cMw72prjqtuZ7HKUOyYw+YribvhKzCPgz/ME8haN6A1JQBYasuv3ayYmeL6DJvWYvVg==',
			'pageNo' : '1',
			'numOfRows' : '10',
			'dataType' : 'JSON',
			'base_date' : date,
			'base_time' : hour,
			'nx' : '55',
			'ny' : '127' }
			
			response = requests.get(url, params=params)
			if (response.status_code >= 200) or (response.status_code < 300):
				r_dict = json.loads(response.text) 
				r_resultcode = r_dict["response"]["header"]['resultCode']
				
				#pprint(r_dict)
				
				if r_resultcode == '00': # success
					r_item = r_dict["response"]["body"]["items"]["item"]
					
					for item in r_item:
						if(item.get("category") == "T1H"): #temperature
							result = item
							
							#print("===================================================")
							#print("Forecast date (YYMMDD): " + result['baseDate'])
							#print("Forecast time (hhmm): " + result['baseTime'])
							#print("Temperature (C): " + str(result['obsrValue']))
							#print("===================================================")
							return {'Date':result['baseDate'], 'Time':result['baseTime'], 'Temperature':result['obsrValue']}
					
					isSuccess = True
				else:
					print("time coordinate... erorrCode:", r_resultcode)
					
					hour = str(int(hour)-100)
					
					if int(hour) < 0:
						date = str(int(date)-1)
						hour = '2400'
						
					
					if len(hour) <= 3:
						hour = '0' + hour
		return "ok"
	except expression as identifier:
		return "fail"
		
@app.route("/get/windspeed")
def get_windspeed():
	try:
		now = datetime.now()
		date = now.strftime('%Y%m%d')
		hour = str(now.hour)
		if int(hour) < 10:
			hour = "0" + hour + "00"
		else:
			hour = hour + "00"
				
		isSuccess = False

		while isSuccess == False:
			
			
			url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
			params ={'serviceKey' : 'DBbxKUDjM9DmJ02j387cMw72prjqtuZ7HKUOyYw+YribvhKzCPgz/ME8haN6A1JQBYasuv3ayYmeL6DJvWYvVg==',
			'pageNo' : '1',
			'numOfRows' : '10',
			'dataType' : 'JSON',
			'base_date' : date,
			'base_time' : hour,
			'nx' : '55',
			'ny' : '127' }
			
			response = requests.get(url, params=params)
			if (response.status_code >= 200) or (response.status_code < 300):
				r_dict = json.loads(response.text) 
				r_resultcode = r_dict["response"]["header"]['resultCode']
				
				#pprint(r_dict)
				
				if r_resultcode == '00': # success
					r_item = r_dict["response"]["body"]["items"]["item"]

					for item in r_item:
						if(item.get("category") == "WSD"): #windspeed
							result = item
							
							#print("===================================================")
							#print("Forecast date (YYMMDD): " + result['baseDate'])
							#print("Forecast time (hhmm): " + result['baseTime'])
							#print("Wind speed (m/s): " + str(result['obsrValue']))
							#print("===================================================")
							return {'Date':result['baseDate'], 'Time':result['baseTime'], 'windspeed':result['obsrValue']}
							break
						
					isSuccess = True
				else:
					print("time coordinate... erorrCode:", r_resultcode)
					hour = str(int(hour)-100)
					
					if int(hour) < 0:
						date = str(int(date)-1)
						hour = '2400'
					
					if len(hour) <= 3:
						hour = '0' + hour
		return "ok"
	except expression as identifier:
		return "fail"
		
if __name__ == "__main__":
	app.run(host="0.0.0.0")