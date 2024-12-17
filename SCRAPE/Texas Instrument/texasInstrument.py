from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
from csv import writer
import pandas as pd
import pycountry
import requests
import getpass
import gspread
import pytz
import time
import json
import os

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

links = [[2, 4, 'https://www.ti.com/amplifier-circuit/fully-differential/products.html'],
		[2, 90, 'https://www.ti.com/amplifier-circuit/pga-vga/products.html'],
		[2, 31, 'https://www.ti.com/amplifier-circuit/special-function/line-drivers/products.html'],
		[2, 67, 'https://www.ti.com/rf-microwave/rf-amplifiers/products.html'],
		[2, 128, 'https://www.ti.com/rf-microwave/rf-amplifiers/rf-fda/products.html'],
		[2, 4, 'https://www.ti.com/rf-microwave/rf-amplifiers/rf-gain-block/products.html'],
		[2, 90, 'https://www.ti.com/rf-microwave/rf-amplifiers/rf-vga/products.html'],
		[23, 30, 'https://www.ti.com/rf-microwave/mixers-modulators/downconverting-mixer/products.html'],
		[23, 30, 'https://www.ti.com/rf-microwave/mixers-modulators/iq-demodulator/products.html'],
		[23, 86, 'https://www.ti.com/rf-microwave/mixers-modulators/iq-modulator/products.html'],
		[26, 60, 'https://www.ti.com/clocks-timing/oscillators/products.html'],
		[30, 65, 'https://www.ti.com/rf-microwave/rf-plls-synthesizers/products.html'],
		[31, 68, 'https://www.ti.com/rf-microwave/rf-power-detectors/products.html'],
		[37, 78, 'https://www.ti.com/rf-microwave/rf-plls-synthesizers/products.html'],
		[39, 72, 'https://www.ti.com/rf-microwave/transceivers-transmitters-receivers/wideband-receivers/products.html'],
		[39, 80, 'https://www.ti.com/rf-microwave/transceivers-transmitters-receivers/rf-sampling-transceivers/products.html'],
		[39, 129, 'https://www.ti.com/rf-microwave/transceivers-transmitters-receivers/wideband-transmitters/products.html']]

# links = [[2, 4, 'https://www.ti.com/amplifier-circuit/fully-differential/products.html']]

header = {'p480': 'Number of Channels',
			'p1261min': 'Voltage (min)',
			'p1261max': 'Voltage (max)',
			'p512': 'Bandwidth',
			'p22typ': 'Slew rate',
			'p89': 'Description',
			'p1typ': 'Current (max)',
			'p1192': 'Temperature Range',
			'p2954': 'Description',
			'p233typ': 'Current (max)',
			'p1184': 'Harmonic Level (max)',
			'p3229': 'Description',
			'p358max': 'Voltage (max)',
			'p358min': 'Voltage (min)',
			'p554max': 'Gain (max)',
			'p1811': 'Package',
			'p2192': 'Features',
			'p62min': 'Frequency (min)',
			'p62max': 'Frequency (max)',
			'p554min': 'Gain (min)',
			'p1185': 'Harmonic Level (max)',
			'p1241': 'Description',
			'p1496': 'Current (max)',
			'p554typ': 'Gain (max)',
			'p2977': 'Impedance',
			'p988typ': 'Noise Figure',
			'p2976typ': 'IP3',
			'p1011typ': 'P1dB (dBm)',
			'p3137': 'Attenuation Step Size',
			'p2505min': 'RF Frequency (min)',
			'p2505max': 'RF Frequency (max)',
			'p3004min': 'IF Frequency (min)',
			'p3004max': 'IF Frequency (max)',
			'p3005typ': 'Conversion Gain',
			'p1515typ': 'IP3',
			'p1987typ': 'IP3',
			'p3003typ': 'P1dB (dBm)',
			'p3008typ': 'LO Power (max)',
			'p3006min': 'LO Frequency (min)',
			'p3006max': 'LO Frequency (max)',
			'p989typ': 'Power',
			'p0typ': 'Voltage (max)',
			'p1507typ': 'Frequency (max)',
			'p1396typ': 'Voltage (max)',
			'p1127typ': 'Phase Noise (max)',
			'p1009typ': 'Carrier Rejection',
			'p1010typ': 'Sideband Rejection',
			'p1099': 'Frequency (max)',
			'p116': 'Description',
			'p1480': 'Package',
			'p3141': 'Stability',
			'p0': 'Voltage (max)',
			'p870': 'Phase Stability',
			'p1099min': 'Frequency (min)',
			'p1099max': 'Frequency (max)',
			'p2409': 'Phase Noise (max)',
			'p0min': 'Voltage (min)',
			'p0max': 'Voltage (max)',
			'p613': 'Current (max)',
			'p846typ': 'Dynamic Range',
			'p1028': 'Number of Channels',
			'p84': 'Resolution Bits',
			'p157max': 'Sample Rate',
			'p300': 'Bandwidth',
			'p873typ': 'SFDR',
			'p1047max': 'Control Voltage (max)',
			'p1047min': 'Control Voltage (min)',
			'p1046max': 'Voltage (max)',
			'p1046min': 'Voltage (min)',
			'p3290': 'Data Rate (input/output)',
			'p596': 'Sample Rate',
			'p1345': 'Number of Channels',
			'p468': 'Description'}

manufacturer = 94

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Texas_Instrument_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])

append_list_as_row(filepathHeader, fHeader)
#########

specs = []
datas = []
for link in links:
	#########
	options = Options()
	# options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-gpu')
	options.add_argument("--start-maximized")
	options.add_argument('--disable-infobars')
	options.add_argument("--disable-extensions")

	global driver
	capabilities = DesiredCapabilities.CHROME
	capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
	driver = webdriver.Chrome(options=options, desired_capabilities=capabilities, service=Service(ChromeDriverManager().install()))
	driver.implicitly_wait(3)
	#########

	print(str(links.index(link)+1)+'-'+str(len(links)))

	driver.get(link[2])
	# driver.fullscreen_window()
	time.sleep(5)

	logs_raw = driver.get_log("performance")
	logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

	def log_filter(log_):
		return (
			# is an actual response
			log_["method"] == "Network.responseReceived"
			# and json
			and "json" in log_["params"]["response"]["mimeType"]
		)

	temp1 = ''
	datas = ''
	for log in filter(log_filter, logs):
		temp1 = ''
		lp = 0
		while lp == 0:
			try:
				request_id = log["params"]["requestId"]
				jsn = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
				if 'ParametricResults' in str(jsn['body']):
					temp1 = json.loads(jsn['body'])['ParametricResults']
				lp = 1
			except Exception as e:
				print('ERROR: Trying again. '+str(e))
				time.sleep(5)
				lp = 0

		if temp1 != '':
			datas = temp1

	scrl = 0
	while scrl == 0:
		try:
			if 'hidden' in str(driver.find_element(By.CLASS_NAME, 'load-more').get_attribute("outerHTML")):
				scrl = 1
			else:
				driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CLASS_NAME, 'load-more'))
				time.sleep(2)
				driver.execute_script("arguments[0].click();", driver.find_element(By.CLASS_NAME, 'load-more').find_element(By.TAG_NAME, 'button'))
				time.sleep(3)
				scrl = 0
		except Exception as e:
			print(str(e))
			scrl = 1

	for data in datas:
		print(str(datas.index(data)+1)+'/'+str(len(datas))+' - '+data['o1'])

		driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.ID, data['o1']))
		driver.execute_script("arguments[0].click();", driver.find_element(By.ID, data['o1']))
		time.sleep(1)

		try:
			img = driver.find_element(By.ID, 'rstid_'+data['o1']).find_element(By.TAG_NAME, 'img').get_attribute('src').replace(':singlesmall','')
		except Exception as e:
			if data['o10'] == '':
				img = ''
			else:
				img = 'https://www.ti.com/ds_dgm/images/'+data['o10']
		driver.execute_script("arguments[0].click();", driver.find_element(By.ID, data['o1']))

		fList = [manufacturer, link[0], link[1], data['o1'], img, 'https://www.ti.com/lit/gpn/'+data['o1'], 'https://www.ti.com/product/'+data['o1']]
		# print(data)
		for y in fHeader[7:]:
			chk = ''
			for d in data:
				try:
					if header[d] == y:
						if type(data[d]) == dict:
							con = ''
							for mp in data[d]:
								con += data[d][mp]['l']+'\n'
							if d in header:
								chk = con
						else:
							if d in header:
								chk = data[d]
				except Exception as e:
					pass
			fList.append(chk)
		append_list_as_row(filepathHeader, fList)

driver.quit()























