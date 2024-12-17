from prettytable import PrettyTable
from datetime import datetime
from bs4 import BeautifulSoup
from csv import writer
import requests
import getpass
import random
import math
import json
import time
import os
import re

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def remDec(num):
	toStr = str(num).split('.')
	if int(toStr[1]) == 0:
		return toStr[0]
	else:
		return num

def filterList(h, b):
	finalHead = []
	finalBody = []
	temp = []
	for x in h:
		try:
			if header[x] in temp:
				# print('~~~'+str(temp.index(header[x])))
				a = temp.index(header[x])
				finalBody[a] = finalBody[a]+' - '+b[h.index(x)]
			else:
				# print(header[x])
				# print(b[h.index(x)])
				finalHead.append(x)
				finalBody.append(b[h.index(x)])
				temp.append(header[x])
		except Exception as e:
			pass
	return [finalHead, finalBody]

# links = ['amplifiers/amplifiers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=amplifiers']
links = ['amplifiers/amplifiers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=amplifiers',
		'baluns/baluns-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=baluns',
		'bias-tees/bias-tees-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=biastees',
		'couplers/couplers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=couplers',
		'equalizers/equalizers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=equalizers',
		'filters-diplexers/filters-diplexers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=filters',
		'hybrids/hybrids-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=hybrids',
		'iq-mixers/iq-mixers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=iqmixers',
		'mixers/mixers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=mixers',
		'multipliers/multipliers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=multipliers',
		'power-dividers/power-dividers-products.aspx?utm_source=home&utm_medium=icon&utm_campaign=powerdividers',
		'other/other-products.aspx#attenuators',
		'other/other-products.aspx#adapters',
		'other/other-products.aspx#dc-blocks',
		'other/other-products.aspx#Limiters']

header = {'Suppression 3F (dBc)': '3rd Harmonic Suppression (3F)',
		'Accuracy [dB]': 'Accuracy',
		'Amplitude Balance [dB]': 'Amplitude Balance',
		'Amplitude Flatness [dB]': 'Amplitude Flatness',
		'Attenuation [dB]': 'Attenuation (min)',
		'Average Power [W]': 'Average Power',
		'Bias [V/mA]': 'Bias Voltage',
		'Center Frequency [GHz]': 'Center Frequency',
		'Common Mode Rejection (dB)': 'Common Mode Rejection',
		'Conversion Loss [dB]': 'Conversion Loss',
		'Coupling [dB]': 'Coupling',
		'Mean Coupling [dB]': 'Coupling',
		'Current [mA]': 'Current (min)',
		'DC Current [A]': 'Current (min)',
		'Directivity [dB]': 'Directivity',
		'Featured': 'Features',
		'Flat Leakage [dBm]': 'Flat Leakage',
		'Frequency (GHz) High': 'Frequency (max)',
		'Frequency (GHz) Low': 'Frequency (min)',
		'Frequency Band  [GHz] Low': 'Frequency Band',
		'Frequency Band  [GHz] High': 'Frequency Band',
		'Frequency Band [GHz] Low': 'Frequency Band',
		'Frequency Band [GHz] High': 'Frequency Band',
		'Suppression F (dBc)': 'Fundamental Suppression (F)',
		'Small Signal Gain [dB]': 'Gain (min)',
		'Group Delay [ps]': 'Group Delay',
		'IF [GHz] High': 'IF Frequency (max)',
		'IF [MHz] High': 'IF Frequency (max)',
		'IF [GHz] Low': 'IF Frequency (min)',
		'IF [MHz] Low': 'IF Frequency (min)',
		'Image Rejection [dB]': 'Image Rejection',
		'Input [GHz] High': 'Input Frequency (max)',
		'Input [GHz] Low': 'Input Frequency (min)',
		'Input Level [dBm] High': 'Input Power Level (max)',
		'Drive Level [dBm]': 'Input Power Level (min)',
		'Input Level [dBm] Low': 'Input Power Level (min)',
		'Insertion Loss [dB]': 'Insertion loss (min)',
		'Total Insertion Loss as a mode converter [dB]': 'Insertion loss (min)',
		'IIP3 [dBm]': 'IP3',
		'Output IP3 [dBm]': 'IP3',
		'DC Port Isolation [dB]': 'Isolation',
		'Isolation [dB]': 'Isolation',
		'LO Drive [dBm] High': 'LO Power (max)',
		'LO Drive [dBm] Low': 'LO Power (min)',
		'Isolations L-I [dB]': 'LO/IF Isolation',
		'RF/LO [GHz] High': 'LO/RF Frequency (max)',
		'RF/LO [GHz] Low': 'LO/RF Frequency (min)',
		'Isolations L-R [dB]': 'LO/RF Isolation',
		'Pass Band Low [GHz] High': 'Lower Passband Frequency (max)',
		'Pass Band Low [GHz] Low': 'Lower Passband Frequency (min)',
		'Typical Suppression [avg]': 'Fundamental Suppression (F)',
		'Noise Figure [dB]': 'Noise Figure',
		'Output [GHz] High': 'Output Frequency (max)',
		'Output [GHz] Low': 'Output Frequency (min)',
		'Output Level [dBm]': 'Output Power',
		'Output P1dB [dBm]': 'P1dB (dBm)',
		'P1dB [dBm]': 'P1dB (dBm)',
		'High Frequency 1 dB Cutoff [GHz]': 'Passband Frequency (max)',
		'Low Frequency 1 dB Cutoff [GHz]': 'Passband Frequency (min)',
		'3 dB Cutoff Frequency [GHz]': 'Passband Frequency (min)',
		'Cutoff Frequency [GHz]': 'Passband Frequency (min)',
		'Passband Insertion Loss [dB]': 'Passband Insertion Loss',
		'Passband Return Loss [dB]': 'Passband Return Loss',
		'Peak Power, CW [W]': 'Peak Power (min)',
		'Phase Balance [Degrees]': 'Phase Balance',
		'Pick-Off Loss [dB]': 'Pick Off Loss',
		'Return Loss (dB)': 'Return Loss',
		'Return Loss [dB]': 'Return Loss',
		'Rise Time [ps]': 'Rise Time',
		'Rise/Fall Time [ps]': 'Rise Time',
		'Saturated Output Power [dBm]': 'Saturated Power (Psat)',
		'Pass Band High [GHz] High': 'Upper Passband Frequency (max)',
		'Pass Band High [GHz] Low': 'Upper Passband Frequency (min)',
		'DC Voltage [V]': 'Voltage (min)',
		'Voltage [V/V]': 'Voltage (min)',
		'VSWR': 'VSWR (single value or input/output)'}

cats = {'LO Driver Surface Mounts': [2, 31],
		'LO Driver Bare Die/Modules': [2, 31],
		'Gain Blocks Bare Die': [2, 4],
		'Surface Mounts & Bare Die': [5, 9],
		'Test & Measurement': [5, 9],
		'Inverters': [5, 9],
		'Surface Mounts': [6, 12],
		'Test & Measurement': [6, 12],
		'High Directivity Bridge': [11, 20],
		'Stripline Directional': [11, 20],
		'Low Loss High Power': [11, 20],
		'Dual Directional': [11, 20],
		'Pick-Off Tees': [11, 20],
		'Surface Mounts': [16, 35],
		'Bare Die/Modules': [16, 35],
		'Lowpass': [16, 51],
		'Highpass': [16, 46],
		'Bandpass': [16, 10],
		'Diplexers': [16, 28],
		'90° Surface Mounts': [11, 47],
		'90° Bare Die/Modules': [11, 47],
		'MMIC Surface Mounts': [23, 56],
		'MMIC Bare Die/Modules': [23, 56],
		'Legacy IQ/IR/SSB': [23, 56],
		'Mixer Search': [23, 56],
		'MMIC/Microlithic Surface Mounts': [23, 56],
		'MMIC Bare Die/Modules': [23, 56],
		'T3': [23, 56],
		'Legacy': [23, 56],
		'Passive x2/x4': [25, 58],
		'Active x2/x4': [25, 58],
		'NLTL Comb Generators': [25, 58],
		'Legacy': [25, 58],
		'High Isolation': [32, 69],
		'Wilkinson 1:2': [32, 69],
		'Wilkinson 1:3': [32, 69],
		'Wilkinson 1:4': [32, 69],
		'Resistive 1:2': [32, 69],
		'NEW: Attenuators': [4, 8],
		'Adapters': [1, 2],
		'DC Blocks': [13, 22],
		'Limiter': [33, 70]}

restrict = ['See Plots', 'See Datasheet', '-']

manufacturer = 50

u = open("/Users/b2y/Work/RFBackDoor/Files/assets/users.txt", "r")
data = u.read()
users = data.split('\n')

s = open("/Users/b2y/Work/RFBackDoor/Files/assets/sites.txt", "r")
data = s.read()
sites = data.split('\n')

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Marki_Microwave_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])

append_list_as_row(filepathHeader, fHeader)
#########

specs = []
for i in links:
	userIndex = random.choice(users)
	siteIndex = random.choice(sites)

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

	session = requests.Session()
	response = session.get('https://www.markimicrowave.com/'+i, headers=headers)

	soup = BeautifulSoup(response.text, features='lxml')

	if 'other/other-products' in str(i):
		cat = str(i).split('#')[1]
		tbl0 = soup.find("div", {"id": cat})
	else:
		tbl0 = soup.find("div", {"class":"vc_active"})
	catDiv = tbl0.find_all('div', id=re.compile("categoryTableDiv-"))

	for a in catDiv:
		tblName = a.find("div", {"class": "CategoryTableHeader"}).text
		if tblName in cats:
			tbl = a.find("table")
			row = tbl.find_all('tr')
			tHead = []
			print(i)
			for x in row[1:2]:
				for y in x:
					if '!--' in str(y):
						main = str(y).split('--')[1]
						tHead.append(main+' '+y.text)
					else:
						tHead.append(y.text)

			for x in row[2:]:
				tBody = []
				fList = []
				fList.append(manufacturer)
				fList.append(cats[tblName][0])
				fList.append(cats[tblName][1])

				td = x.find_all('td')
				unqId = td[1].find('a')
				pdf = td[2].find('a')

				fList.append(str(unqId.text)+'"')
			#######
				userIndex = random.choice(users)
				siteIndex = random.choice(sites)

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

				session = requests.Session()
				response = ''
				while response == '':
					try:
						response = session.get('https://www.markimicrowave.com'+str(unqId['href']), headers=headers)
					except Exception as e:
						response = ''

				soup = BeautifulSoup(response.text, features='lxml')

				img1 = soup.find("div", {"class": "dynamicContents"})
				img2 = str(json.loads(img1.text)[0]['ProductVariant']['ThumbnailUrl']).replace(' ', '%20')
				if 'https' in img2:
					fList.append(img2)
				else:
					fList.append('https://www.markimicrowave.com'+img2)
			#######
				fList.append('https://www.markimicrowave.com'+str(pdf['href']))
				fList.append('https://www.markimicrowave.com'+str(unqId['href']))

				for y in x:
					if str(y) != ' ':
						if 'PDF Download' in str(y):
							pdf = y.find('a')['href']
							tBody.append('https://www.markimicrowave.com'+pdf)
						else:
							tBody.append(y.text)

				print(tHead)
				print('~')
				print(tBody)

				filtered = filterList(tHead, tBody)
				finaltHead = filtered[0]
				finaltBody = filtered[1]

				print(finaltHead)
				print('~~')
				print(finaltBody)
				print('~~~~~~~~~')

				for y in fHeader[7:]:
					chk = ''
					for i in finaltHead:
						try:
							if y == header[i]:
								chk = i
						except Exception:
							pass 
					if chk != '':
						if 'ghz' in chk.lower():
							try:
								toMhz = remDec(float(finaltBody[finaltHead.index(chk)])*1000)
							except Exception as e:
								toMhz = finaltBody[finaltHead.index(chk)]
						else:
							toMhz = finaltBody[finaltHead.index(chk)]

						if str(toMhz) in restrict:
							fList.append('')
						else:
							fList.append(toMhz)
					else:
						fList.append('')

				append_list_as_row(filepathHeader, fList)
			print('\n~~~~~~~~~~~~~~\n')


# for x in specs:
# 	print(x)