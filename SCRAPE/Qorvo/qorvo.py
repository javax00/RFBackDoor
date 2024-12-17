from datetime import datetime
from bs4 import BeautifulSoup
from csv import writer
import requests
import getpass
import random
import math
import time
import os

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

u = open("/Users/b2y/Work/RFBackDoor/Files/assets/users.txt", "r")
data = u.read()
users = data.split('\n')

s = open("/Users/b2y/Work/RFBackDoor/Files/assets/sites.txt", "r")
data = s.read()
sites = data.split('\n')

def getLinkHeader():
	userIndex = random.choice(users)
	siteIndex = random.choice(sites)

	global headers
	headers = {
		'dnt': '1',
		'upgrade-insecure-requests': '1',
		'User-Agent': userIndex,
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-user': '?1',
		'sec-fetch-dest': 'document',
		'referer': 'https://www.'+siteIndex+'/',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
		'Updgrade-Insecure-Requests': '1',
		'authority': siteIndex,
	}

links = ['https://www.qorvo.com/products/product-list/?categoryID=ca0003',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0021',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0026',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0030',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0037',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0046',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0063',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0071',
		'https://www.qorvo.com/products/product-list/?categoryID=ca0172',
		'https://www.qorvo.com/products/wireless-connectivity/low-power-iot',
		'https://www.qorvo.com/products/wireless-connectivity/ultra-wideband']

# links = ['https://www.qorvo.com/products/product-list/?categoryID=ca0003']

cats = [['2.4 GHz Wi-Fi Low Noise Amplifiers', 2, 50],
		['2.4 GHz Wi-Fi Power Amplifiers', 2, 67],
		['3G Mobile Power Amplifiers', 2, 67],
		['3G/4G Mobile Power Amplifiers', 2, 67],
		['5 GHz Wi-Fi Power Amplifiers', 2, 67],
		['Analog Variable Gain Amplifiers', 2, 90],
		['CATV Amplifiers', 2, 4],
		['CATV Hybrid Amplifiers', 2, 4],
		['Digital Variable Gain Amplifiers', 2, 90],
		['Distributed Amplifiers', 2, 4],
		['Driver Amplifiers', 2, 31],
		['Gain Block Amplifiers', 2, 4],
		['General Purpose Mobile Power Amplifiers', 2, 67],
		['High Frequency Amplifiers', 2, 4],
		['Infrastructure Power Amplifier Modules', 2, 67],
		['Low Noise Amplifiers', 2, 50],
		['Low Noise Amplifiers with Bypass', 2, 50],
		['Low Phase Noise Amplifiers', 2, 52],
		['Mobile PA Modules', 2, 4],
		['Power Amplifiers', 2, 67],
		['Spatium Amplifiers', 2, 4],
		['Switch LNA Modules', 2, 50],
		['Transimpedance Amplifiers', 2, 4],
		['Low Noise Amplifiers', 2, 50],
		['Low Noise Amplifiers', 2, 50],
		['2.4 GHz Wi-Fi Low Noise Amplifiers', 2, 50],
		['CATV Hybrid Amplifiers', 2, 4],
		['Infrastructure Power Amplifier Modules', 2, 67],
		['Mobile PA Modules', 2, 67],
		['Power Amplifiers', 2, 67],
		['Switch LNA Modules', 2, 50],
		['2.4 GHz Wi-Fi Low Noise Amplifiers', 2, 50],
		['Digital Step Attenuators', 4, 26],
		['Fixed Attenuators', 4, 8],
		['Temperature Compensating Attenuators', 4, 8],
		['Voltage Controlled Attenuators', 4, 93],
		['Fixed Attenuators', 4, 8],
		['Duplexers', 15, 32],
		['Antennaplexers', 16, 120],
		['Diplexers', 16, 28],
		['GPS Filters', 16, 44],
		['RF Filters', 16, 120],
		['Wi-Fi Filters', 16, 113],
		['Diplexers', 16, 28],
		['Wi-Fi Filters', 16, 113],
		['Diplexers', 16, 28],
		['Wi-Fi Filters', 16, 113],
		['Downconverters', 23, 30],
		['Integrated Synthesizers with Mixers', 23, 56],
		['Mixers', 23, 56],
		['Modulators', 23, 86],
		['Upconverters', 23, 86],
		['Multiplexers', 24, 57],
		['Multipliers (Active)', 25, 58],
		['Multipliers (Passive)', 25, 58],
		['Phase Shifters', 29, 66],
		['Limiters', 33, 70],
		['Limiters', 33, 70],
		['Wi-Fi Switches', 36, 76],
		['Antenna Switch Modules', 36, 7],
		['Discrete Switches', 36, 76],
		['Diversity Switches', 36, 76],
		['High Power GaN Switches', 36, 76],
		['Wi-Fi Switches', 36, 76],
		['Wi-Fi Switches', 36, 76],
		['GaAs pHEMTs', 38, 74],
		['GaN HEMTs', 38, 74],
		['Ultra-Wideband Transceiver Modules', 39, 80],
		['Ultra-Wideband Transceivers', 39, 80]]

header = {'Attenuation Range dB': 'Attenuation Range',
			'Bandwidth GHz': 'Bandwidth',
			'Channels': 'Channel',
			'Bits': 'Control Bits',
			'Current mA': 'Current (max)',
			'11b/g Current mA': 'Current (max)',
			'11ac Current mA': 'Current (max)',
			'11n Current mA': 'Current (max)',
			'11g/n Current mA': 'Current (max)',
			'11a/n Current mA': 'Current (max)',
			'Description': 'Description',
			'Vd V': 'Drain Voltage (max)',
			'Standards': 'Features',
			'Bands': 'Features',
			'Type': 'Features',
			'Functionality': 'Features',
			'Standards / Bands': 'Features',
			'Frequency Max MHz': 'Frequency (max)',
			'Frequency Max GHz': 'Frequency (max)',
			'Frequency Min MHz': 'Frequency (min)',
			'Frequency Min GHz': 'Frequency (min)',
			'Gain dB': 'Gain (max)',
			'Gain @ 0 dB Atten dB': 'Gain (max)',
			'Power Gain dB': 'Gain (max)',
			'Small Signal Gain dB': 'Gain (max)',
			'Vg V': 'Gate Voltage (max)',
			'Insertion Loss dB': 'Insertion loss (max)',
			'IIP3 dBm': 'IP3',
			'OIP3 dBm': 'IP3',
			'NF dB': 'Noise Figure',
			'11b/g Pout dBm': 'Output Power',
			'11ac Pout dBm': 'Output Power',
			'11n Pout dBm': 'Output Power',
			'Pout dBm': 'Output Power',
			'2.4GHz 11g/n Pout dBm': 'Output Power',
			'5GHz 11a/n Pout dBm': 'Output Power',
			'Power dBm': 'Output Power',
			'Pout W': 'Output Power',
			'Differential Output Vpp mV': 'Output Voltage (max)',
			'OP1dB dBm': 'P1dB (dBm)',
			'Package Type': 'Package',
			'Package mm': 'Package',
			'Phase Noise dBc/Hz': 'Phase Noise (max)',
			'2.4GHz Rx Gain dB': 'Rx Gain',
			'5GHz Rx Gain dB': 'Rx Gain',
			'Psat dBm': 'Saturated Power (Psat)',
			'Psat W': 'Saturated Power (Psat)',
			'2.4GHz Tx Gain dB': 'Tx Gain',
			'5GHz Tx Gain dB': 'Tx Gain',
			'Voltage V': 'Voltage (max)',
			'Vcc V': 'Voltage (max)'}

manufacturer = 79

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Qorvo_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])

append_list_as_row(filepathHeader, fHeader)
#########

getLinkHeader()
session = requests.Session()
for link in links:
	print(link)
	response = session.get(link, headers=headers)
	soup = BeautifulSoup(response.text, features='lxml')

	tbls = soup.find_all("div", {"class": "pst-open"})
	for tbl in tbls:
		tblHeader = tbl.find("h3", {"class": "pst-header-title"}).text.replace(' '+tbl.find("span", {"class": "pst-header-amount"}).text, '')

		tr = tbl.find_all("tr")
		ths = tr[0].find_all("th")
		finalHeader = []
		for th in ths:
			hdr = th.text.strip().replace('\n', '')
			finalHeader.append(hdr)

		c, sc = '', ''
		for cat in cats:
			if tblHeader == cat[0]:
				c = cat[1]
				sc = cat[2]

		if c != '':
			for trtd in tr[1:]:
				fList = []
				# TEMP = []
				# TEMP.extend(['', '', '', '', '', '', ''])
				fList.append(manufacturer)
				fList.append(c)
				fList.append(sc)

				finalBody = []
				for td in trtd.find_all("td"):
					finalBody.append(td.text.strip())
				print(finalBody[0])

				fList.append(finalBody[0])

				##
				getLinkHeader()
				session1 = requests.Session()
				response1 = session1.get('https://www.qorvo.com'+trtd.find_all("td")[0].find("a", {"class": "pst-part-ref-name"})['href'], headers=headers)
				soup1 = BeautifulSoup(response1.text, features='lxml')

				img = soup1.find("div", {"class": "product-info"}).find("img")['src']
				if img != '':
					fList.append('https://www.qorvo.com'+img)
				else:
					fList.append('')
				##

				try:
					fList.append('https://www.qorvo.com'+trtd.find_all("td")[0].find("a", {"class": "pst-part-ref-pdf"})['href'])
				except Exception:
					fList.append('')

				fList.append('https://www.qorvo.com'+trtd.find_all("td")[0].find("a", {"class": "pst-part-ref-name"})['href'])

				for y in fHeader[7:]:
					chk = ''
					for i in finalHeader:
						try:
							if y == header[i]:
								chk = i
						except Exception:
							pass
					if chk != '':
						if chk == 'Psat W':
							if finalBody[finalHeader.index(chk)] != '':
								r = 10*math.log10(float(finalBody[finalHeader.index(chk)]))+30
								fList.append("{:.2f}".format(float(r)))
							else:
								fList.append('')
						elif chk == 'Pout W':
							if finalBody[finalHeader.index(chk)] != '':
								r = 10*math.log10(float(finalBody[finalHeader.index(chk)]))+30
								fList.append("{:.2f}".format(float(r)))
							else:
								fList.append('')
						elif chk == 'Frequency Max GHz':
							r = finalBody[finalHeader.index(chk)]
							if r == 'DC':
								fList.append(r)
							elif r == '':
								fList.append(r)
							elif ', ' in r:
								fList.append("{:.2f}".format(float(r.split(', ')[1])/1000))
							else:
								fList.append("{:.2f}".format(float(r)/1000))
						elif chk == 'Frequency Min GHz':
							r = finalBody[finalHeader.index(chk)]
							if r == 'DC':
								fList.append(r)
							elif r == '':
								fList.append(r)
							elif ', ' in r:
								fList.append("{:.2f}".format(float(r.split(', ')[1])/1000))
							else:
								fList.append("{:.2f}".format(float(r)/1000))
						else:
							fList.append(finalBody[finalHeader.index(chk)])
						# TEMP.append(chk)
					else:
						# TEMP.append('')
						fList.append('')
				# append_list_as_row(filepathHeader, TEMP)
				append_list_as_row(filepathHeader, fList)

		print('~')
	time.sleep(3)

# print('~')
# for x in dups:
# 	print(x)



