from Auto_def import time_correction, check_in, check, send

def main(now):
	check_in(now)
	print('☪time.sleep 1 quater')
	time.sleep(900)
	check(now)
	if(now == "check_in"):
		print('☪time.sleep 9.25 h')
		time.sleep(3600*9.25)
	else:
		print('☪time.sleep 14.25 h')
		time.sleep(3600*14.25)

try:
	time_correction()
	if(first):
		main("check_out")
		
	while True:
		main("check_in")
		main("check_out")
		holiday_correction()
except:
	print('❌CMD Error!')
	send('CMD Error!')