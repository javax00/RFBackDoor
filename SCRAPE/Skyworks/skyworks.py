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
import math
import os

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def wToDbm(num):
	f = 10*math.log10(float(num))+30
	s = str(f).split('.')

	return float(s[0]+'.'+s[1][:2])

links = [[2, 4, 'https://www.skyworksinc.com/Product-Specification?family=Amplifiers&categories=4G/LTE%20Power%20Amplifiers'],
		[2, 4, 'https://www.skyworksinc.com/Product-Specification?family=Amplifiers&categories=3G/CDMA/TDSCDMA/WCDMA%20Power%20Amplifiers'],
		[2, 4, 'https://www.skyworksinc.com/Product-Specification?family=Amplifiers&categories=2G/GSM/GPRS/EDGE%20Power%20Amplifiers'],
		[2, 4, 'https://www.skyworksinc.com/Product-Specification?family=Amplifiers&categories=Multimode%20Multiband%20(MMMB)%20Power%20Amplifiers'],
		[2, 4, 'https://www.skyworksinc.com/Product-Specification?family=Amplifiers&categories=Bluetooth%20Power%20Amplifiers'],
		[2, 4, 'https://www.skyworksinc.com/Product-Specification?family=Amplifiers&categories=Gain%20Block%20(General%20Purpose)%20Amplifiers'],
		[2, 112, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=Wi-Fi%20Connectivity%20Amplifiers;Wi-Fi%20Connectivity%20Amplifiers;2.5%20GHz%20Low%20Noise%20Amplifiers%20for%20Wi-Fi%20Connectivity;2.5%20GHz%20Power%20Amplifiers%20for%20Wi-Fi%20Connectivity;5%20GHz%20Low%20Noise%20Amplifiers%20for%20Wi-Fi%20Connectivity;5%20GHz%20Power%20Amplifiers%20for%20Wi-Fi%20Connectivity;Dual-Band%20Power%20Amplifiers%20for%20Wi-Fi%20Connectivity'],
		[2, 4, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=BDS/GPS/GNSS%20Power%20Amplifiers;BDS/GPS/GNSS%20Power%20Amplifiers'],
		[2, 50, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=Low%20Noise%20Amplifiers;Low%20Noise%20Amplifiers'],
		[2, 4, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=CATV%20Amplifiers;CATV%20Amplifiers;12v%20Line%20Amplifiers%20for%20HFC;24v%20Line%20Amplifiers%20for%20HFC;75%20Ohm%20Gain%20Blocks%20for%20HFC;Amplifiers%20for%20Set-top%20Box;CATV%20Driver%20Amplifier;FTTx/RFoG%20RF%20Amplifiers%20for%20HFC;Hybrid%20Line%20Amplifier%20Modules%20for%20HFC;Low-Noise%20Amplifier%20for%20Set-top%20Box;Upstream%20Amplifiers%20for%20HFC'],
		[2, 90, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=Variable%20Gain%20Amplifiers%20(VGAs);Variable%20Gain%20Amplifiers%20(VGAs)'],
		[2, 4, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=Wireless%20Infrastructure%20/%20Small%20Cell%20Power%20Amplifiers;Wireless%20Infrastructure%20/%20Small%20Cell%20Power%20Amplifiers;Wireless%20Infrastructure%20/%20Small%20Cell%20Power%20Amplifiers;High%20Efficiency%20Linearizable%20Small%20Cell%20Power%20Amplifiers;High%20Linearity%20Small%20Cell%20Power%20Amplifiers;Small%20Cell%20Gain%20Blocks;WiMAX%20Power%20Amplifiers;High-efficiency%20Small%20Cell%20Power%20Amps%20for%205G'],
		[2, 4, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=Amplifiers%20for%20Smart%20Energy-Connected%20Home%20and%20Automation%20802.15.4,%20ISM%20and%20ZigBee®;Amplifiers%20for%20Smart%20Energy-Connected%20Home%20and%20Automation%20802.15.4,%20ISM%20and%20ZigBee®'],
		[2, 4, 'https://www.skyworksinc.com/Product%20Specification?family=Amplifiers&categories=High-efficiency%20Small%20Cell%20Power%20Amps%20for%205G'],
		[4, 26, 'https://www.skyworksinc.com/Product%20Specification?family=Attenuators&categories=Digital%20Attenuators;Digital%20Attenuators'],
		[4, 93, 'https://www.skyworksinc.com/Product%20Specification?family=Attenuators&categories=Voltage%20Variable%20Attenuators;Voltage%20Variable%20Attenuators;0.7%20-%205.0%20GHz%20Plastic%20Packaged%20Voltage%20Variable%20Attenuators%20-%20PIN%20Diode-Based;DC-6%20GHz%20Plastic%20Packaged%20Voltage%20Variable%20Attenuators%20-%20FET-Based'],
		[4, 8, 'https://www.skyworksinc.com/Product%20Specification?family=Attenuators&categories=ATN3580%20Fixed%20Attenuator%20Pads'],
		[4, 8, 'https://www.skyworksinc.com/Product%20Specification?family=Attenuators&categories=ATN3590%20Fixed%20Attenuator%20Pads'],
		[10, 16, 'https://www.skyworksinc.com/Product%20Specification?family=Circulators%20and%20Isolators&categories=Circulators%20and%20Isolators%20for%20Wireless%20Infrastructure%20Applications;Circulators%20and%20Isolators%20for%20Wireless%20Infrastructure%20Applications'],
		[10, 16, 'https://www.skyworksinc.com/Product%20Specification?family=Circulators%20and%20Isolators&categories=Circulators%20and%20Isolators%20for%20Radar%20Applications;Circulators%20and%20Isolators%20for%20Radar%20Applications'],
		[26, 60, 'https://www.skyworksinc.com/Products/Timing/Ultra-Series-Crystal-Oscillators-XO'],
		[26, 60, 'https://www.skyworksinc.com/Products/Timing/Low-Jitter-Crystal-Oscillators-XO'],
		[26, 60, 'https://www.skyworksinc.com/Products/Timing/General-Purpose-Oscillators-XO'],
		[26, 60, 'https://www.skyworksinc.com/Products/Timing/Ultra-Series-Voltage-Controlled-Crystal-Oscillators-VCXO'],
		[26, 60, 'https://www.skyworksinc.com/Products/Timing/Low-Jitter-Voltage-Controlled-Crystal-Oscillators-VCXO'],
		[26, 60, 'https://www.skyworksinc.com/Products/Timing/General-Purpose-Voltage-Controlled-Crystal-Oscillators-VCXO'],
		[37, 78, 'https://www.skyworksinc.com/Products/Timing/RF-Synthesizers'],
		[33, 70, 'https://www.skyworksinc.com/en/Product-Specification?family=Diodes&categories=Plastic%20Surface%20Mount%20(SMT)%20Limiter%20Diodes'],
		[33, 70, 'https://www.skyworksinc.com/en/Product-Specification?family=Diodes&categories=Limiter%20Modules'],
		[33, 70, 'https://www.skyworksinc.com/en/Product-Specification?family=Diodes&categories=Limiter%20Diode%20Chips'],
		[33, 70, 'https://www.skyworksinc.com/en/Product-Specification?family=Diodes&categories=High%20Reliability%20Limiter%20Diodes'],
		[9, 15, 'https://www.skyworksinc.com/Product%20Specification?family=RF%20Passives&categories=MIS%20Silicon%20Chip%20Capacitors;MIS%20Silicon%20Chip%20Capacitors'],
		[11, 20, 'https://www.skyworksinc.com/Product%20Specification?family=Switches&categories=Smart%20Coupler;Smart%20Coupler']]

# links = [[37, 78, 'https://www.skyworksinc.com/Products/Timing/RF-Synthesizers']]

header = {'Description': 'Description',
			'Package': 'Package',
			'Package (mm)': 'Package',
			'Frequency (MHz)': 'Frequency (max)',
			'Typical PAE (%)': 'PAE',
			'Typical Linear LTE Power': 'Power',
			'(dBm)': 'Power (dBm)',
			'Typical Imax (mA)': 'Current (max)',
			'Typical Gain (dB)': 'Gain (max)',
			'Supply Voltage (V)': 'Voltage (max)',
			'Typical Output Power (dbm) GSM/EDGE': 'Output Power',
			'Output Power (dBm)': 'Output Power',
			'Gain (dB)': 'Gain (max)',
			'Frequency Range (GHz)': 'Frequency (min)', # (break up into min and max)
			'Test Frequency (GHz)': 'Frequency (max)',
			'Gain Typ (dB)': 'Gain (max)',
			'OIP3 (dBm)': 'IP3',
			'P1 dB (dBm)': 'P1dB (dBm)',
			'Quiescent Current Typ (mA)': 'Current (max)',
			'Noise Figure Typ (dB)': 'Quiescent Drain Current',
			'Power Added Efficiency (%)': 'PAE',
			'VCC (V)': 'Voltage (max)',
			'Typ POUT (dBm)': 'Output Power',
			'VDD (V)': 'Drain Voltage (max)',
			'OP1 dB (dBm)': 'P1dB (dBm)',
			'Supply Current Typ (mA)': 'Current (max)',
			'Frequency (GHz)': 'Frequency (max)',
			'Frequency (GHz) Min': 'Frequency (min)',
			'Frequency (GHz) Max': 'Frequency (max)',
			'Linear Output Power (dBm)': 'Output Power',
			'Test Frequency (MHz)': 'Frequency (max)',
			'IP1 dB (dBm)': 'P1dB (dBm)',
			'NF (dB)': 'Noise Figure',
			'Frequency Range': 'Frequency (min)', # (break up into min and max)
			'Control Bits/ Interface Parallel/Serial': 'Control Bits',
			'LSB Attenuation (dB)': 'Attenuation (max)',
			'Attenuation Range (dB)': 'Attenuation Range',
			'Typ IL (dB)': 'Insertion loss (max)',
			'Typ IIP3 (dBm)': 'IP3',
			'Typ IP1 dB (dBm)': 'P1dB (dBm)',
			'Insertion Loss at Min Control (dB) Max': 'Insertion loss (max)',
			'Attenuation Range at Max Control': 'Attenuation Range',
			'Input IP3 (dBm) Min': 'IP3',
			'Control Input Range': 'Control Voltage (min)', # (break up into min and max)
			'Control Input Range1': 'Control Voltage (min)', # (break up into min and max)
			'Control Input Range2': 'Control Voltage (max)', # (break up into min and max)
			'Nominal Attenuation (dB)': 'Attenuation (max)',
			'_Return Loss_ 01-12 GHz (dB)': 'Return Loss',
			'_Return Loss_ 01-265 GHz (dB)': 'Return Loss',
			'_Return Loss_ 01-40 GHz (dB)': 'Return Loss',
			'_Return Loss_ DC-12 GHz (dB)': 'Return Loss',
			'_Return Loss_ 12-26 GHz (dB)': 'Return Loss',
			'_Return Loss_ 26-33 GHz (dB)': 'Return Loss',
			'_Return Loss_ 33-40 GHz (dB)': 'Return Loss',
			'Band': 'Frequency Band',
			'Insertion Loss (dB)': 'Insertion loss (max)',
			'Isolation/ Return Loss (dB)': 'Return Loss',
			'Case Size (Inch/mm)': 'Package',
			'Isolation (dB)': 'Isolation',
			'Return Loss (dB)': 'Return Loss',
			'Max Power (W) F/R': 'Peak Power (min)', # (convert to correct units)
			'Frequency Range (MHz)': 'Frequency (min)', # (break up into min and max)
			'Phase Jitter (ps RMS)': 'Phase Stability',
			'Temperature Range (°C)': 'Temperature Range',
			'Package Size (mm)': 'Package',
			'Frequency Min': 'Frequency (min)',
			'Frequency Max': 'Frequency (max)',
			'Temperature Range Min (°C)': 'Temperature Range', # JOIN
			'Temperature Range Max (°C)': 'Temperature Range', # JOIN
			'Package Type': 'Package',
			'RF Test Frequency (GHz)': 'Frequency (max)',
			'Typical Insertion Loss (dB) Pin = 0 dBm': 'Insertion loss (max)',
			'Maximum Saturated Power (Watts)': 'Saturated Power (Psat)',
			'Typical Return Loss (dB) Pin = 0 dBm': 'Return Loss',
			'Typical Flat Leakage Power (dBm)': 'Flat Leakage',
			'Capacitance Value (pF) ±20%': 'Capacitance (max)',
			'Size (mils)': 'Package',
			'Description (Absorptive/ Reflective)': 'Description',
			'Tx Low-band Insertion Loss (dB) 07-10 GHz': 'Insertion loss (max)',
			'Tx Low-band Insertion Loss (dB) 1-2 GHz': 'Insertion loss (max)',
			'Tx Low-band Insertion Loss (dB) 2-3 GHz': 'Insertion loss (max)',
			'Typical Directivity': 'Directivity',
			'Typical Coupling': 'Coupling',
			'Control Logic': 'Control Type'}

manufacturer = 88

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Skyworks_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])

append_list_as_row(filepathHeader, fHeader)
#########
#########
options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

global driver
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(5)
#########

final = []
for link in links:
	fDatas = []
	try:
		driver.find_element(By.CLASS_NAME, 'cookies_con').find_element(By.TAG_NAME, 'button').click()
	except Exception:
		pass

	driver.get(link[2])
	driver.execute_script("document.body.style.zoom='25%'")
	time.sleep(2)
	try:
		driver.execute_script("document.getElementById('skyworksProductFamilyGrid').style.height = '999999px';")
	except Exception:
		pass
	time.sleep(2)


	specs = [] 
	allSpecs = driver.find_elements(By.CLASS_NAME, 'ag-header-cell-text')
	for x in allSpecs:
		specs.append(x.text)

	pdfs = []
	urls = []
	prods = []
	title = driver.find_elements(By.CLASS_NAME, 'product-title')
	for x in title:
		try:
			pdfs.append(x.find_element(By.CLASS_NAME, 'document-link').get_attribute('href'))
		except Exception:
			pdfs.append('')

		try:
			urls.append(x.find_element(By.CLASS_NAME, 'link-title').get_attribute('href'))
		except Exception:
			urls.append('')

		try:
			prods.append(x.find_element(By.CLASS_NAME, 'link-title').get_attribute('href').split('/')[-1])
		except Exception:
			prods.append('')

	datas = []
	dataCon = driver.find_element(By.CLASS_NAME, 'ag-center-cols-container')
	rows = dataCon.find_elements(By.CLASS_NAME, 'ag-row-position-absolute')
	for row in rows:
		cell = row.find_elements(By.CLASS_NAME, 'ag-cell')
		temp = []
		for x in cell:
			temp.append(x.text)
		datas.append(temp)

	i = 0
	for data in datas:
		con = {}
		con['pdf'] = pdfs[i]
		con['url'] = urls[i]
		con['Product'] = prods[i]
		for b in range(len(data)):
			con[specs[b+1]] = data[b]
		fDatas.append(con)
		i+=1

	for data in fDatas:
		print('['+str(links.index(link)+1)+'/'+str(len(links))+'] - '+str(fDatas.index(data)+1)+'/'+str(len(fDatas)))
		fList = []

		# Frequency (MHz)
		# 'Frequency Min': 'Frequency (min)'
		# 'Frequency Max': 'Frequency (max)'
		if 'Frequency (MHz)' in data and str(data['Frequency (MHz)']) != '':
			try:
				tmp = data['Frequency (MHz)'].split('-')
				temp1 = tmp[0]
				temp2 = tmp[1]
			except Exception:
				pass

			del data['Frequency (MHz)']
			data['Frequency Min'] = str(temp1)
			data['Frequency Max'] = str(temp2)

		# Frequency Range (GHz)
		# 'Frequency (GHz) Min': 'Frequency (min)'
		# 'Frequency (GHz) Max': 'Frequency (max)'
		if 'Frequency Range (GHz)' in data and str(data['Frequency Range (GHz)']) != '':
			if '<br>' in str(data['Frequency Range (GHz)']):
				dt = data['Frequency Range (GHz)'].split('<br>')[0]
			else:
				dt = data['Frequency Range (GHz)']

			try:
				tmp = dt.split('–')
				temp1 = tmp[0]
				temp2 = tmp[1]
			except Exception as e:
				tmp = dt.split('-')
				temp1 = tmp[0]
				temp2 = tmp[1]
			del data['Frequency Range (GHz)']
			data['Frequency (GHz) Min'] = str(temp1)
			data['Frequency (GHz) Max'] = str(temp2)

		# Frequency Range
		# 'Frequency Min': 'Frequency (min)'
		# 'Frequency Max': 'Frequency (max)'
		if 'Frequency Range' in data and str(data['Frequency Range']) != '':
			try:
				tmp = data['Frequency Range'].split('-')
				temp1 = tmp[0]
				temp2 = tmp[1]
			except Exception:
				pass

			del data['Frequency Range']
			data['Frequency Min'] = str(temp1)
			data['Frequency Max'] = str(temp2)


		# Frequency Range (MHz)
		# 'Frequency Min': 'Frequency (min)'
		# 'Frequency Max': 'Frequency (max)'
		if 'Frequency Range (MHz)' in data and str(data['Frequency Range (MHz)']) != '':
			try:
				tmp = data['Frequency Range (MHz)'].split('to')
				temp1 = tmp[0]
				temp2 = tmp[1]
			except Exception:
				pass

			del data['Frequency Range (MHz)']
			data['Frequency Min'] = str(temp1)
			data['Frequency Max'] = str(temp2)

		# Control Input Range
		# 'Control Input Range1': 'Control Voltage (min)'
		# 'Control Input Range2': 'Control Voltage (max)'
		if 'Control Input Range' in data and str(data['Control Input Range']) != '':
			try:
				tmp = data['Control Input Range'].split('-')
				temp1 = tmp[0]
				temp2 = tmp[1].replace('V', '')
			except Exception:
				pass

			del data['Control Input Range']
			data['Control Input Range1'] = str(temp1)
			data['Control Input Range2'] = str(temp2)

		# Temperature Range
		if 'Temperature Range Min (°C)' in data and 'Temperature Range Max (°C)' in data:
			temp1 = data['Temperature Range Min (°C)']
			temp2 = data['Temperature Range Max (°C)']
			del data['Temperature Range Min (°C)']
			del data['Temperature Range Max (°C)']
			data['Temperature Range (°C)'] = str(temp1)+' - '+str(temp2)

		# Max Power (W) F/R # TO DBM, FIRST NUMBER
		if 'Max Power (W) F/R' in data and str(data['Max Power (W) F/R']) != '':
			if '/' in str(data['Max Power (W) F/R']):
				data['Max Power (W) F/R'] = wToDbm(str(data['Max Power (W) F/R']).split('/')[0])
			else:
				data['Max Power (W) F/R'] = wToDbm(str(data['Max Power (W) F/R']))

		try:
			driver.get(data['url'])
			img = driver.find_element(By.CLASS_NAME, 'diagram_page_slider').find_element(By.TAG_NAME, 'img').get_attribute('src')
			if '.gif' in img:
				img = ''
		except Exception as e:
			img = ''

		fList.append(manufacturer)
		fList.append(link[0])
		fList.append(link[1])
		fList.append(data['Product'])
		fList.append(img)
		fList.append(data['pdf'])
		fList.append(data['url'])

		for y in fHeader[7:]:
			chk = ''
			for d in data:
				try:
					if header[d] == y:
						if d == 'Frequency Range (GHz)' or d == 'Test Frequency (GHz)' or d == 'Frequency (GHz)' or d == 'Frequency (GHz) Min' or d == 'Frequency (GHz) Max' or d == 'RF Test Frequency (GHz)':
							chk = str(int(float(data[d])*1000))
						else:
							if '—' == str(data[d]):
								chk = ''
							else:
								chk = str(data[d]).replace('<br>', '\n')
						break
				except Exception:
					pass
			fList.append(chk)

		final.append(fList)
		append_list_as_row(filepathHeader, fList)

driver.quit()














