from bs4 import BeautifulSoup
from datetime import datetime
from csv import writer
import requests
import getpass
import random
import json
import time
import os
import re

u = open("/Users/b2y/Work/RFBackDoor/Files/assets/users.txt", "r")
data = u.read()
users = data.split('\n')

s = open("/Users/b2y/Work/RFBackDoor/Files/assets/sites.txt", "r")
data = s.read()
sites = data.split('\n')

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def init_checkDups(mylist):
	dups = {}
	for i, val in enumerate(mylist):
		val = val[0]
		val1 = val[1]
		if val not in dups:
			dups[val] = [i, 1]
		else:
			if dups[val][1] == 1:
				newValMin = mylist[dups[val][0]][1]
				newValMax = mylist[i][1]
				mylist[dups[val][0]] = [mylist[dups[val][0]][0]+" min", newValMin]

			dups[val][1] += 1
			mylist[i] = [str(mylist[i][0])+" max", newValMax]

	return mylist

def checkDups(mylist):
	dups = {}
	minim = ''
	maxim = ''
	for i, val in enumerate(mylist):
		val = val[0]
		val1 = val[1]
		if val not in dups:
			dups[val] = [i, 1]
		else:
			if dups[val][1] == 1:
				newVal = mylist[dups[val][0]][1]#+'\n'+mylist[i][1]
				mylist[dups[val][0]] = [mylist[dups[val][0]][0], newVal]

			dups[val][1] += 1
			mylist.remove(mylist[i])
	return mylist

def num_there(s):
	return any(i.isdigit() for i in s)

def filterNum(s):
	p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
	if re.search(p, s) is not None:
		for catch in re.finditer(p, s):
			return catch[0].replace(",", "")

def reDec(s):
	if '.' in str(s):
		con = str(s).split('.')
		if int(con[-1]) == 0:
			return int(con[0])
		else:
			return float(s)
	else:
		return int(s)

def clDec(s):
	if s == '0.0000000000':
		return '0'
	else:
		c = 0
		for x in range(len(s)-1, -1, -1):
			if s[x] != '0':
				break
			c += 1
		return str(s[0:-c])

def convertMHz(x):
	x = str(x)
	if x == '':
		return ""
	else:
		if 'ms' not in x and 'hours' not in x:
			con = []
			temp = x.split()
			for y in temp:
				if num_there(y):
					if '-' in y:
						temp1 = y.split('-')
						for i in temp1:
							con.append(i)
					else:
						con.append(y)

			final = []
			for y in con:
				if 'g' in y.lower():
					con = reDec(float(filterNum(y))*1000)
					final.append(con)
				elif 'm' in y.lower():
					con = reDec(filterNum(y))
					final.append(con)
				elif 'k' in y.lower():
					con = clDec(format(reDec(float(filterNum(y)))*0.001, '.10f'))
					final.append(con)
				elif 'h' in y.lower():
					con = clDec(format(reDec(float(filterNum(y)))*0.000001, '.10f'))
					final.append(con)
				else:
					if 'g' in x.lower() or 'k' in x.lower():
						return "error"
					elif 'm' in x.lower():
						con = reDec(filterNum(y))
						final.append(con)
					else:
						con = clDec(format(reDec(float(filterNum(y)))*0.000001, '.10f'))
						final.append(con)
			f = []
			for y in final:
				f.append(float(y))
			if len(f) >= 3:
				return [reDec(min(f)), reDec(max(f)), x]
			elif len(f) == 2:
				return [reDec(min(f)), reDec(max(f))]
			else:
				return [str(final[0])]
		else:
			return ""

manufacturer = 8

# prods = [['TX RX MODULE',
# 			['TRANSCEIVER', '10623', '211dd520ef9a440989417925e9638f80']]]

prods = [['2',
			['4', '10863', 'd260217b07ad4c3baefb1046adedd9fa'],
			['4', '12831', '3c9e9a9628b44d1ca4fa8b4bd863cac3'],
			['4', '11156', 'fcfe7519b97e41eb9410e52c9075ca23'],
			['4', '10678', 'f7ea42ba44174423ab65e452af117c39'],
			['4', '10676', '139566874b6542afa32d987bc68ca842'],
			['90', '10689', '176bc2f3c98b4c3bb15d93f755c3a8c9'],
			['90', '11159', 'b8401aa5505c444883d3da1777e6d370'],
			['90', '11158', '46e2cf0d0e3f454392b5369cb81b9eb6'],
			['31', '10677', 'ab8b7a5d02ef40cfb6588af835fa7d7b'],
			['67', '10682', '34229dcb5211439697006cf5a490a7c1'],
			['50', '10675', '2bf52ef0e4634665a551d919a6482af8']],
		['23',
			['56', '10709', '8d6c07612a544909b3d1101f8dd13d1f'],
			['56', '10869', '20cad302f8fc4fafb98f367de32dac29'],
			['56', '10707', '0a725e9f50db4419bdb95286d1cccfdc'],
			['56', '10710', 'fb827ab5c1e748189635fc6ae24b9f63'],
			['56', '10711', '800b1b1f88094b948c723a7cfb7b2e1f'],
			['86', '10764', '7b653140ae0240b1a6a76fbbb8f5c8ee'],
			['86', '10708', 'b637623779f0433c85983b01ffe78390'],
			['86', '10687', 'fbeca0fb2b644718a51c3a533c054fdd'],
			['86', '11054', '5961853965304756975a33e6d1c0e4e2'],
			['86', '10864', '29ed9380e9ad4a189843b518487c418f'],
			['30', '10693', '8cb4f38297a1495cbdf361e3e777a630'],
			['30', '10706', 'e0f5bd00d3c5411b9d577792aa03c0cf'],
			['30', '10763', '50645895d48f4e748be60ddd9df46df5']],
		['36',
			['76', '10871', 'f901c2358a8e4717955cdc008e4e2b99'],
			['76', '10725', '6eda7da016ab4337b0f817cfc81686d0'],
			['76', '11151', 'eea2f6d445144c6ca0c9c5605b510036'],
			['76', '10723', '0c29d119202247d4b72dbfce87b8e69f'],
			['76', '12829', '017d791de62146c1aa4238288a9558ae'],
			['76', '12830', 'aedad22ed1ae4235a5842ef7d106ec09'],
			['76', '10647', 'e80d033c60aa4313a7ea8c263c62357e']],
		['31',
			['68', '10704', 'edde76b302a4466d9f9c8b9e577168ea'],
			['68', '12856', '8bd83c258215446bab1d86275c874b55'],
			['68', '11409', 'fb663d0fe75a47b9a8b3cb045d59146c'],
			['68', '10701', '1dc7af707b0545ecaac57769c6b39fe2'],
			['68', '10703', '460a7b0eb26b4810ad8069952ed04cb0'],
			['68', '12853', '1bbe5090ab4c487d9c5853a7299b405b']],
		['39',
			['85', '11300', '17210d5e2bb9443e812282272929c61b'],
			['85', '10726', 'fc0fbb46ca1744bf85237a1126dc9a5f'],
			['85', '11808', 'cf443a30c19f49e09d5530a72c492127'],
			['85', '12836', 'ed79b6c550734a959c14219e6481fbf4'],
			['80', '10623', '211dd520ef9a440989417925e9638f80'],
			['80', '10727', '24ace065381948ee8d250dfe9085268f'],
			['72', '11299', 'd4b241a7358448c99075614d57483be0'],
			['72', '11492', 'd415d94a7bbe457ba391e6e046ff5e8e']],
		['26',
			['60', '10865', '108591da07a7470287f305eee5cf320c'],
			['60', '11381', '01d18e1eaa4b45f58076f2b5b2cab290'],
			['60', '10734', '36fd07bd52e4456db3ece4056875c8e4'],
			['60', '10719', '34f2e0ecbdbc475db8cab6af2a094beb'],
			['60', '10717', 'd61461e0a25b4437bd386547838d983b'],
			['60', '10718', 'aba27655af384f8292bb83d9854bc1b7']],
		['4',
			['8', '10861', '4345da9a7bd3403aa2ac7cef72f6030b'],
			['8', '10685', '1a564ab64eea49189643d0388af8441a'],
			['8', '10684', '56fb6131f0834c6787bacffbc0002f3d'],
			['8', '10686', 'dd5acd2a55824de6bda17c818f60ae07']],
		['29',
			['66', '10699', '2c352d8f7e6046b0b6f6b57e96ccb524'],
			['66', '10700', 'a977405932664741a3e8af4e57aa9958'],
			['66', '10705', '8898a872c7c5427bab93bc807e52555b'],
			['66', '10870', '29988e66e82847b0af752d140286dfc7']],
		['30',
			['65', '11183', 'bf50751f8ff44b798a463e6818f125c0'],
			['65', '11182', 'b6091423925143908352fd0828d35e40'],
			['65', '11181', '27466293cef54243b91bd18a3c0255e2'],
			['65', '12850', '0f65a6b969dd4105916cd6cab4ce67f6']],
		['16',
			['120', '12849', 'bb3d4f3707d84bc3a9031fffc5b132c4'],
			['51', '10692', '5fa09b2967744e9c9a049366e23debbb'],
			['10', '12822', '382437d6974e48ceb0834481d15f1f1b']],
		['18',
			['39', '10720', '0ae2bf8444bc4f27864edf7cbf2282c1'],
			['39', '10866', '8381012cfffe419fbc677f438133ca08']],
		['37',
			['78', '11018', '28a8312dac074da6b84949618a1191c8']],
		['28',
			['64', '10721', '3369b8dbe0ea4ca3867f2c4a62d00aac']],
		['25',
			['58', '10722', '56400a0ea4ea4440ac94647a5ff80024']],
		['24',
			['57', '11267', '55af276563d7415fbb012456b54fa885']],
		['27',
			['11', '11195', '77db9b42c90d46f9b23a2a2a4c425571']]]

specs = [["RF Primary Function", "Description"],
		["Product Description", "Description"],
		["Device Overview", "Description"],
		["Comments", "Description"],
		["Clock Function", "Description"],
		["Freq Response RF", "Frequency (min)"],
		["Freq Response RF min", "Frequency (min)"],
		["Freq Response RF max", "Frequency (max)"],
		["Freq Response", "Frequency (min)"],
		["Freq Response min", "Frequency (min)"],
		["Freq Response max", "Frequency (max)"],
		["Frequency Ranges", "Frequency (min)"],
		["Frequency Ranges min", "Frequency (min)"],
		["Frequency Ranges max", "Frequency (max)"],
		["Frequency Range", "Frequency (min)"],
		["Frequency Range min", "Frequency (min)"],
		["Frequency Range max", "Frequency (max)"],
		["Insertion Loss", "Insertion loss (min)"],
		["Insertion Loss min", "Insertion loss (min)"],
		["Insertion Loss max", "Insertion loss (max)"],
		["Package", "Package"],
		["Psat", "Saturated Power (Psat)"],
		["Gain dB", "Gain (min)"],
		["Gain dB min", "Gain (min)"],
		["Gain dB max", "Gain (max)"],
		["Gain", "Gain (min)"],
		["Gain min", "Gain (min)"],
		["Gain max", "Gain (max)"],
		["NF", "Noise Figure"],
		["Rx NF / IIP3", "Noise Figure"],
		["OP1dB", "P1dB (dBm)"],
		["IP1dB", "P1dB (dBm)"],
		["OIP3", "IP3"],
		["IIP3", "IP3"],
		["Tx OIP3", "IP3"],
		["Vs", "Voltage (min)"],
		["Vs min", "Voltage (min)"],
		["Vs max", "Voltage (max)"],
		["Vs span", "Voltage (min)"],
		["Vs span min", "Voltage (min)"],
		["Vs span max", "Voltage (max)"],
		["Is", "Current (min)"],
		["Is min", "Current (min)"],
		["Is max", "Current (max)"],
		["Gain Set", "Control Type"],
		["Program Method", "Control Type"],
		["Output Power", "Output Power"],
		["Residual Phase Noise", "Phase Noise (min)"],
		["Residual Phase Noise min", "Phase Noise (min)"],
		["Residual Phase Noise max", "Phase Noise (max)"],
		["Phase Noise @ 10k", "Phase Noise (min)"],
		["Phase Noise @ 10k min", "Phase Noise (min)"],
		["Phase Noise @ 10k max", "Phase Noise (max)"],
		["Phase Noise @ 1M", "Phase Noise (min)"],
		["Phase Noise @ 1M min", "Phase Noise (min)"],
		["Phase Noise @ 1M max", "Phase Noise (max)"],
		["PN Closed-Loop at 10kHz Offset", "Phase Noise (min)"],
		["PN Closed-Loop at 10kHz Offset min", "Phase Noise (min)"],
		["PN Closed-Loop at 10kHz Offset max", "Phase Noise (max)"],
		["PN Closed-Loop at 1 MHz offset", "Phase Noise (min)"],
		["PN Closed-Loop at 1 MHz offset min", "Phase Noise (min)"],
		["PN Closed-Loop at 1 MHz offset max", "Phase Noise (max)"],
		["Phase Noise @ 100k", "Phase Noise (min)"],
		["Phase Noise @ 100k min", "Phase Noise (min)"],
		["Phase Noise @ 100k max", "Phase Noise (max)"],
		["Phase Noise Floor", "Phase Noise (min)"],
		["Phase Noise Floor min", "Phase Noise (min)"],
		["Phase Noise Floor max", "Phase Noise (max)"],
		["1/f Noise (10kHz Offset at 1GHz Carrier)", "Phase Noise (min)"],
		["1/f Noise (10kHz Offset at 1GHz Carrier) min", "Phase Noise (min)"],
		["1/f Noise (10kHz Offset at 1GHz Carrier) max", "Phase Noise (max)"],
		["Return Loss", "Return Loss"],
		["BW -3 dB", "Bandwidth"],
		["Freq BB 3 dB BW", "Bandwidth"],
		["IF/Channel BW", "Bandwidth"],
		["Slew Rate", "Slew rate"],
		["Attenuation", "Attenuation (min)"],
		["Attenuation min", "Attenuation (min)"],
		["Attenuation max", "Attenuation (max)"],
		["Attenuation Range", "Attenuation Range"],
		["Vs+", "Control Voltage (min)"],
		["Vs+ min", "Control Voltage (min)"],
		["Vs+ max", "Control Voltage (max)"],
		["Vcontrol (low)", "Control Voltage (min)"],
		["Vcontrol (low) min", "Control Voltage (min)"],
		["Vcontrol (low) max", "Control Voltage (max)"],
		["Vcontrol (high)", "Control Voltage (min)"],
		["Vcontrol (high) min", "Control Voltage (min)"],
		["Vcontrol (high) max", "Control Voltage (max)"],
		["# of Channels", "Number of Channels"],
		["# Rx Channels", "Number of Channels"],
		["Interface", "Interface"],
		["Vtune", "Tuning Voltage (min)"],
		["Vtune min", "Tuning Voltage (min)"],
		["Vtune max", "Tuning Voltage (max)"],
		["Data Rate Device", "Data Rate (input/output)"],
		["Low Center Frequency", "Center Frequency"],
		["High Center Frequency", "Center Frequency 2"],
		["Freq Ref Input", "Input Frequency (min)"],
		["Freq Ref Input min", "Input Frequency (min)"],
		["Freq Ref Input max", "Input Frequency (max)"],
		["Input Frequency", "Input Frequency (min)"],
		["Input Frequency min", "Input Frequency (min)"],
		["Input Frequency max", "Input Frequency (max)"],
		["Output Frequency", "Output Frequency (min)"],
		["Output Frequency min", "Output Frequency (min)"],
		["Output Frequency max", "Output Frequency (max)"],
		["Conversion Gain", "Conversion Gain"],
		["Conv. Gain", "Conversion Gain"],
		["Input Power", "Input Power Level (min)"],
		["Input Power min", "Input Power Level (min)"],
		["Input Power max", "Input Power Level (max)"],
		["Freq Output Divide By", "Divide Ratio (min)"],
		["Freq Output Divide By min", "Divide Ratio (min)"],
		["Freq Output Divide By max", "Divide Ratio (max)"],
		["Freq Ouput Multiplier", "Multiplication Factor"],
		["Freq Response LO", "LO Frequency (min)"],
		["Freq Response LO min", "LO Frequency (min)"],
		["Freq Response LO max", "LO Frequency (max)"],
		["Clock Input", "Clock Frequency (min)"],
		["Clock Input min", "Clock Frequency (min)"],
		["Clock Input max", "Clock Frequency (max)"],
		["Freq Response IF", "IF Frequency (min)"],
		["Freq Response IF min", "IF Frequency (min)"],
		["Freq Response IF max", "IF Frequency (max)"],
		["LO Drive Nominal", "LO Power (min)"],
		["LO Drive Nominal min", "LO Power (min)"],
		["LO Drive Nominal max", "LO Power (max)"],
		["LO Drive Nom.", "LO Power (min)"],
		["LO Drive Nom. min", "LO Power (min)"],
		["LO Drive Nom. max", "LO Power (max)"],
		["LO/RF Isolation", "LO/RF Isolation"],
		["LO/RF Iso", "LO/RF Isolation"],
		["LO/IF Isolation", "LO/IF Isolation"],
		["LO/IF Iso", "LO/IF Isolation"],
		["Image Rejection", "Image Rejection"],
		["Rx Image Rejection", "Image Rejection"],
		["LO Spurs", "Spurious Rejection"],
		["Sideband Suppression", "Sideband Rejection"],
		["Noise Spectral Density", "Noise Spectral Density"],
		["IF/RF Noise Density", "Noise Spectral Density"],
		["Phase Range", "Phase Range"],
		["Vgate", "Gate Voltage (min)"],
		["Vgate min", "Gate Voltage (min)"],
		["Vgate max", "Gate Voltage (max)"],
		["Phase Error", "Phase Error"],
		["Phase Error RMS", "Phase Error"],
		["Amplitude Error", "Amplitude Error"],
		["PFD", "PFD Frequency (min)"],
		["PFD min", "PFD Frequency (min)"],
		["PFD max", "PFD Frequency (max)"],
		["RF Threshold", "Power Limit"],
		["Channels", "Channel"],
		["Resolution", "Resolution"],
		["Settling Time", "Settling Time"],
		["Tuning Word Width", "Tuning Word Width"],
		["Sample Rate", "Sample Rate"],
		["SINAD", "SINAD"],
		["Absorptive/Reflective", "Features"],
		["Amp Architecture", "Features"],
		["Device Config", "Features"],
		["Integrated VCO", "Features"],
		["Interface Protocol", "Features"],
		["Modulation Mode", "Features"],
		["Protocols Supported", "Features"],
		["RF Features", "Features"],
		["Special Features", "Features"],
		["Channel Spacing", "Channel Spacing"],
		["Control Bits", "Control Bits"],
		["Data Output Interface", "Data out Interface"],
		["Device Match", "Device Match"],
		["Control  Step Size", "Gain Step"],
		["Number of Outputs", "Num Outputs"],
		["Freq Output Divider", "Output Divider Frequency (min)"],
		["Freq Output Divider min", "Output Divider Frequency (min)"],
		["Freq Output Divider max", "Output Divider Frequency (max)"],
		["IP-0.1 dB", "P01db"],
		["Power", "Power"],
		["DAC Resolution", "Resolution Bits"],
		["Response Time", "Response Time"],
		["Vs Span Dual", "Voltage Span (min)"],
		["Vs Span Dual min", "Voltage Span (min)"],
		["Vs Span Dual max", "Voltage Span (max)"],
		["Vs Span Single", "Voltage Span (min)"],
		["Vs Span Single min", "Voltage Span (min)"],
		["Vs Span Single max", "Voltage Span (max)"]]

specsFinal = []
for x in specs:
	if x[1] not in specsFinal:
		specsFinal.append(x[1])

toMHz = ["Frequency (min)",
		"Frequency (max)",
		"Bandwidth",
		"Center Frequency",
		"Center Frequency 2",
		"Input Frequency (min)",
		"Input Frequency (max)",
		"Output Frequency (min)",
		"Output Frequency (max)",
		"LO Frequency (min)",
		"LO Frequency (max)",
		"Clock Frequency (min)",
		"Clock Frequency (max)",
		"IF Frequency (min)",
		"IF Frequency (max)",
		"PFD Frequency (min)",
		"PFD Frequency (max)",
		"Sample Rate",
		"Output Divider Frequency (min)",
		"Output Divider Frequency (max)"]

username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Analog_Devices_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in specsFinal:
	fHeader.append(x)

append_list_as_row(filepathHeader, fHeader)

for prod in prods:
	for y in range(0, len(prod)-1):
		prodList = prod[1:][y]

		err = 0
		while err == 0:
			try:
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

				url1 = 'https://www.analog.com/cdp/pst/view/en/'+str(prodList[1])+'.js'

				r = requests.get(url1, headers=headers, timeout=20)
				soup = BeautifulSoup(r.text, features='lxml')
				site_json = json.loads(soup.text)
				err = 1
			except Exception as e:
				print(e)
				err = 0
				time.sleep(3)

		header_list = []

		for i in site_json['columns']:
			if i['display_in_default_view'] == 'true':
				header_list.append([i['external_name'], i['field']])
		r.close()

		err = 0
		while err == 0:
			try:
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

				url2 = 'https://www.analog.com/cdp/pst/data/en/'+str(prodList[2])+'.js'

				r = requests.get(url2, headers=headers, timeout=20)
				soup = BeautifulSoup(r.text, features='lxml')
				site_json = json.loads(soup.text)
				err = 1
			except Exception as e:
				print(e)
				err = 0
				time.sleep(3)

		print(site_json['description'])
		for i in site_json['data']:
			fList = [manufacturer, prod[0], prodList[0]]
			specsF = []
			for y in init_checkDups(header_list):
				if str(y[0]) == 'Part #':
					fList.append(str(i[y[1]]['displayValue']))
					try:
						if 'image-unavailable' in str(i['s20']['value'][0]):
							fList.append('')
						else:
							if str(i['s20']['value'][0]) == 'https://www.analog.com':
								fList.append('')
							else:
								fList.append(str(i['s20']['value'][0]))
					except Exception:
						fList.append('')

					fList.append(str('https://analog.com/en/'+i['0']['generic']+'/datasheet'))
					fList.append('https://analog.com/en/'+i['0']['generic'])
				for spec in specs:
					if str(y[0]).lower() == str(spec[0]).lower():
						specsF.append([str(spec[1]), str(i[y[1]]['displayValue'])])

			print(specsF)
			new = []
			newDesc = ''
			for x in specsF:
				if x[0] in toMHz:
					mh = convertMHz(x[1])
					if mh == 'error' or mh == '':
						new.append([x[0], ''])
					elif len(mh) == 1:
						new.append([x[0], mh[0]])
					elif len(mh) == 2:
						new.append([x[0], mh[0]])
						new.append([x[0].replace("min", "max"), mh[1]])
					elif len(mh) == 3:
						new.append([x[0], mh[0]])
						new.append([x[0].replace("min", "max"), mh[1]])
						newDesc = mh[2]
				else:
					new.append(x)

			print('~')
			# print(new)
			print('~')
			for i in range(0, 5):
				checkedDups = checkDups(new)
				if newDesc != '':
					checkedDups.append(['Description', newDesc])
				newDesc = ''
			print(checkedDups)

			for x in specsFinal:
				con = ''
				for y in checkedDups:
					if x.lower() == y[0].lower():
						con = y[1]
				if con != '':
					fList.append(con)
				else:
					fList.append('')

			print(fList)
			append_list_as_row(filepathHeader, fList)
			fList = []
			print('~~~~~~~~~~\n')

		r.close()
		time.sleep(5)
	time.sleep(5)
print('DONE.')
