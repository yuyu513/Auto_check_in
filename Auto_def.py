import time
import json
import requests
import urllib.request as req
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Auto_Account import Username, Password, bot_token, chat_id, api_key

def send(text):
	url = 'https://api.telegram.org/{}/{}'.format(bot_token, 'sendMessage')
	data = {'chat_id': chat_id, 'text': text,}
	res = requests.post(url,data)

def open_data_api():
	# 臺北市政府行政機關辦公日曆表
	url = 'https://quality.data.gov.tw/dq_download_json.php?nid=145708&md5_url=1a7506b007086d03afe37570ac7f52e4'
	with req.urlopen(url) as res:
		input_data = json.loads(res.read().decode())
	now_time = datetime.today().date()
	print('▶', now_time)
	filter_data = [x for x in input_data if datetime.strptime(x['date'], '%Y/%m/%d').date() == now_time]
	if (len(filter_data) > 0):
		if (filter_data[0]['isHoliday'] == '是'):
			return False  #休假日/補假
		return True 
def holiday_correction():
	while(open_data_api() == False):
		t = time.localtime()
		text = time.strftime("▶%H:%M:%S ", t)
		Hour = int(time.strftime("%H", t))
		Min = int(time.strftime("%M", t))
		Sec = int(time.strftime("%S", t))
		print(text, '\n☪time.sleep ' + str(24-Hour) + 'h ' + str(-Min) + 'm ' + str(-Sec) + 's')
		time.sleep(60*60*24*1-Sec-60*Min-60*60*Hour)
def time_correction():
	holiday_correction()
	t = time.localtime()
	text = time.strftime("%H:%M:%S ", t)
	Hour = int(time.strftime("%H", t))
	Min = int(time.strftime("%M", t))
	Sec = int(time.strftime("%S", t))
	global first
	first = False
	if (Hour < 8) & (Hour >= 0):
		print('▶', text, '\n☪time.sleep ' + str(8-Hour) + 'h ' + str(-Min) + 'm ' + str(3-Sec) + 's')
		time.sleep((3-Sec)-60*Min+3600*(8-Hour))
	elif (Hour >= 8) & (Hour <= 17):
		if (Hour == 17) & (Min >= 30):
			print('▶', text, '\n☪time.sleep ' + str(32-Hour) + 'h ' + str(-Min) + 'm ' + str(3-Sec) + 's')
			time.sleep((3-Sec)-60*Min+3600*(32-Hour))
		else:
			print('▶', text, '\n☪time.sleep ' + str(17.5-Hour) + 'h ' + str(-Min) + 'm ' + str(3-Sec) + 's')
			time.sleep((3-Sec)-60*Min+3600*(17.5-Hour))
			first = True
	elif (Hour > 17) & (Hour <24):
		print('▶', text, '\n☪time.sleep ' + str(32-Hour) + 'h ' + str(-Min) + 'm ' + str(3-Sec) + 's')
		time.sleep((3-Sec)-60*Min+3600*(32-Hour))
	else:
		print('❌Time Correction IF Error!')
	
def verification_code(xpath, textbox):
	img  = 'verification_code.png'
	web.find_element(By.XPATH, (xpath)).screenshot(img)
	file = {'file': open(img, 'rb')}
	payload = {'key': api_key,}
	response = requests.post('http://2captcha.com/in.php', files = file, params = payload) 

	if response.ok and response.text.find('OK') > -1:
		captcha_id = response.text.split('|')[1]
		for i in range(20):
			response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
			if response.text.find('CAPCHA_NOT_READY') > -1: 
			  print('✓Verification code time.sleep 3s')
			  time.sleep(3)
			elif response.text.find('OK') > -1:
			  captcha_text = response.text.split('|')[1].upper()
		if response.text.find('CAPCHA_NOT_READY') > -1:
			print('❌Verification Code 20 Error!')
		for i in range(20):
			response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
			if response.text.find('CAPCHA_NOT_READY') > -1: 
			  print('✓Verification code time.sleep 3s')
			  time.sleep(3)
			elif response.text.find('OK') > -1:
			  captcha_text = response.text.split('|')[1].upper()
		if response.text.find('CAPCHA_NOT_READY') > -1:
			print('❌Verification Code 40 Error!')
			send('Verification Code 40 Error!')
	else:
	  send('Verification Code Error!')
	  print('❌Verification Code Error!')
	
	web.find_element(By.NAME,textbox).send_keys(captcha_text)
	text = "✓Code: " + captcha_text
	print(text)
def login():
	global web
	web = webdriver.Chrome()
	#web.get('http://hreip1.ntust.edu.tw/EIP/Login/LoginNtust.resource.aspx')
	web.get('https://stuinfosys.ntust.edu.tw/Authenticate/SSOAccount/Index/Attendance')
	web.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/form/div[2]/div[1]/input").send_keys(Username)
	web.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/form/div[2]/div[2]/input").send_keys(Password)
	verification_code("/html/body/div/div/div/div/div/div/form/div[2]/div[3]/img", "VerifyCode")
	login = web.find_element(By.XPATH,"/html/body/div/div/div/div/div/div/form/div[3]/input[1]")
	login.click()
	time.sleep(3)
	web.get("https://hreip1.ntust.edu.tw/EIP/humanly/data_transfer/hum_wkrecord_online.aspx")
def check_in(now):
	login()
	verification_code("/html/body/form/div[3]/div[1]/table[2]/tbody/tr[2]/td/img", "ctl00$ContentPlaceHolder1$TextBox_Code")
	t = time.localtime()
	text = time.strftime("%H:%M:%S ", t)
	if now == "check_in":
		web.find_element(By.NAME,"ctl00$ContentPlaceHolder1$Button_humwr_amst_hum_wkrecord").click()
		text += "\n♡check in finished"
	else:
		web.find_element(By.NAME, "ctl00$ContentPlaceHolder1$Button_humwr_pmet_hum_wkrecord").click()
		text += "\n♡check out finished"
	print('▶', text)

def check(now):
	login()
	if now == "check_in":
		xpath = "/html/body/form/div[3]/div[1]/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]"
		now = '08'
	else:
		xpath = "/html/body/form/div[3]/div[1]/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]"
		now = '17'
	t = time.localtime()
	check_time = web.find_element(By.XPATH, xpath).text
	if (check_time[11:13] == now):
		text = "♡checked " + time.strftime("%H:%M:%S ", t) + check_time
		send(text)
		print(text)
	else:
		send('Time Error!')
		print('❌Time Error!')