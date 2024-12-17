from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from csv import writer
import pandas as pd
import requests
import getpass
import random
import math
import json
import time
import bs4
import os

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

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
				newVal = mylist[dups[val][0]][1]+'\n'+mylist[i][1]
				mylist[dups[val][0]] = [mylist[dups[val][0]][0], newVal]

			dups[val][1] += 1
			mylist.remove(mylist[i])
	return mylist

u = open("/Users/b2y/Work/RFBackDoor/Files/assets/users.txt", "r")
data = u.read()
users = data.split('\n')

s = open("/Users/b2y/Work/RFBackDoor/Files/assets/sites.txt", "r")
data = s.read()
sites = data.split('\n')

headers = {'designtype': 'Description',
			'conntype': 'Description',
			'con1series': 'Connector 1 Type',
			'con1gender': 'Connector 1 gender',
			'con2series': 'Connector 2 Type',
			'con2gender': 'Connector 2 gender',
			'con1angle': 'Connector 1 Body Style',
			'con1mountmethod': 'Connector 1 Mount',
			'con2mountmethod': 'Connector 2 Mount',
			'imp1': 'Connector 1 Impedance',
			'imp2': 'Connector 2 Impedance',
			'con1polarity': 'Connector 1 Polarity',
			'con2polarity': 'Connector 2 Polarity',
			'con1connmethod': 'Connector 1 Connection Method',
			'con2connmethod': 'Connector 2 Connection Method',
			'maxfreq': 'Frequency (max)',
			'direction': 'Description',
			'minfreq': 'Frequency (min)',
			'vswrmaxinp': 'VSWR (single value or input/output)',
			'powermaxinp': 'Max Input Power',
			'dim1': 'Length',
			'con1attachmethod': 'Flange Type',
			'con1group': 'Flange Type',
			'gainflatness': 'Gain (min)',
			'gainnominal': 'Gain (max)',
			'flatness': 'Gain Flatness',
			'p1db': 'P1dB (dBm)',
			'tointer': 'IP3',
			'tointerf1': 'IP3',
			'voltsens': 'Voltage (min)',
			'voltmaxdc': 'Voltage (max)',
			'currentdc': 'Current (min)',
			'design': 'Description',
			'acc2f1': 'Noise Figure',
			'currentdcmax': 'Voltage (max)',
			'powermaxinpf2': 'Gain (min)',
			'noisefig': 'Noise Figure',
			'layout': 'Description',
			'polarization': 'Polarization',
			'option': 'Number of Channels',
			'gainnominalunit': 'Gain (min)',
			'radomemtl': 'Radome Material',
			'tempmaxop': 'Temperature Range',
			'tempminop': 'Temperature Range',
			'phasediff': 'Phase Adjustments',
			'powerpeak': 'Peak Power (max)',
			'rfshield': 'Isolation',
			'con3gender': 'DC Port Gender',
			'con3series': 'DC Port Series',
			'rfcableflextype': 'Description',
			'rfcablegn': 'Coax Type',
			'con2angle': 'Connector 2 Body Style',
			'imp3': 'Impedance',
			'bendradiusot': 'Bend Radius',
			'bendradiusrep': 'Bend Radius',
			'noshields': 'Number of Shields',
			'jacketmtl': 'Jacket Material',
			'velocitypropagation': 'Propagation Velocity',
			'rfcablecoaxtype': 'Coax Type',
			'isomin': 'Isolation',
			'ports': 'Ports',
			'conntermtype': 'Termination Type',
			'connit0': 'Interface',
			'con2attachmethod': 'Flange Type 2',
			'con3attachmethod': 'Flange Type 3',
			'con3connmethod': 'Flange Type 3',
			'tss': 'Sensitivity',
			'opf3': 'Frequency (min)',
			'opf5': 'Frequency (max)',
			'ilf1': 'Rejection',
			'lopower': 'Output Power',
			'acc1f3': 'Recovery Time',
			'acc2f4': 'Recovery Time',
			'opf9': 'Reference Frequency (min)',
			'acc1f5': 'Phase Noise (min)',
			'switchtime': 'Switching Speed',
			'spec15': 'Control Type',
			'con4series': 'Control Type',
			'conntermsubtype': 'Package',
			'acc2f10': 'Tuning Voltage (min)',
			'acc2f9': 'Tuning Voltage (max)',
			'acc2max': 'Rotation Speed',
			'controlvolt': 'Control Voltage (min)',
			'risetime': 'Switching Speed',
			'voltdcsupplyv1': 'Voltage (min)'}

unSelc = ['Select', 'Sku', 'Keywords', 'Category', 'Reach', 'Price', 'Name', 'Purchase']
fieldHeaders = []
fieldSKU = []
manufac = 34

#########
# username = os.getlogin()
# if not os.path.exists('C:\\Users\\'+username+'\\Desktop\\RFBackDoor'):
# 	os.makedirs('C:\\Users\\'+username+'\\Desktop\\RFBackDoor')

# now = datetime.now()
# dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
# filepathHeader = 'C:\\Users\\'+username+'\\Desktop\\RFBackDoor\\Fairview_Microwave_'+str(dt_string)+'.csv'
# fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF']

username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Fairview_Microwave_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in headers:
	if headers[x] not in fHeader:
		fHeader.append(headers[x])

append_list_as_row(filepathHeader, fHeader)
#########

df = pd.read_csv('fairViewMicrowave_links.csv')

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

driver.get('https://www.fairviewmicrowave.com/')
driver.add_cookie({"name": "categoryView", "value": "table"})
time.sleep(5)

for i in df.index:
	cat = ''
	subCat = ''
	for x in df:
		if str(x) == 'Category_id':
			cat = str(df[x][i])
		if str(x) == 'Subcategory_id':
			subCat = str(df[x][i])
		if str(x) == 'Links':
			if str(df[x][i]) != 'nan':
				c = 0

				url = str(df[x][i])
				print(url)

				driver.get(url)
				driver.add_cookie({"name": "categoryView", "value": "table"})
				time.sleep(2)

				pagehtml = driver.page_source
				soup = bs4.BeautifulSoup(pagehtml, "html.parser")

				try:
					site_json = json.loads(soup.text)
					totProd = math.ceil(int(site_json['iTotalRecords'])/100)

					for x in site_json['aaData']:
						fList = []
						fspec = []
						fspecs = {}
						for i in x:
							if str(i) == 'Select':
								sku = str(x[i]).split('"')[7].replace('/','-')
								c += 1
								print(str(c)+'. '+sku)
								fList.extend([manufac, cat, subCat, sku, 'https://www.fairviewmicrowave.com/images/Product/large/'+sku+'.jpg', 'https://www.fairviewmicrowave.com/images/productPDF/'+sku+'.pdf'])
							if str(i) == 'Sku':
								sku = str(x[i]).split('"')[3]
								fList.append('https://www.fairviewmicrowave.com'+sku)
							if str(i) not in unSelc:
								for y in headers:
									if y == str(i).split('99')[1]:
										if headers[y] == 'Frequency (max)' or headers[y] == 'Frequency (min)':
											if str(x[i]) == 'None' or str(x[i]) == 'N/A' or str(x[i]) == '-':
												print('ERROR')
												pass
											else:
												fspec.append([headers[y], str(int(float(x[i])*1000))])
										else:
											fspec.append([headers[y], str(x[i])])

						for x in checkDups(fspec):
							fspecs[x[0]] = x[1]

						for x in fHeader[7:]:
							if x in fspecs:
								if str(fspecs[x]) == 'None' or str(fspecs[x]) == 'N/A' or str(fspecs[x]) == '-' or str(fspecs[x]) == '':
									fList.append('')
								else:
									fList.append(str(fspecs[x]))
							else:
								fList.append('')

						for x in fList[7:]:
							if x != '':
								append_list_as_row(filepathHeader, fList)
								break

					if totProd >= 2:
						nxtPg = 100
						for x in range(totProd-1):
							driver.get(url+'&iDisplayStart='+str(nxtPg))
							driver.add_cookie({"name": "categoryView", "value": "table"})
							time.sleep(2)

							pagehtml = driver.page_source
							soup = bs4.BeautifulSoup(pagehtml, "html.parser")
							site_json = json.loads(soup.text)

							for x in site_json['aaData']:
								fList = []
								fspec = []
								fspecs = {}
								for i in x:
									if str(i) == 'Select':
										sku = str(x[i]).split('"')[7]
										c += 1
										print(str(c)+'. '+sku)
										fList.extend([manufac, cat, subCat, sku, 'https://www.fairviewmicrowave.com/images/Product/large/'+sku+'.jpg', 'https://www.fairviewmicrowave.com/images/productPDF/'+sku+'.pdf'])
									if str(i) == 'Sku':
										sku = str(x[i]).split('"')[3]
										fList.append('https://www.fairviewmicrowave.com'+sku)
									if str(i) not in unSelc:
										for y in headers:
											if y == str(i).split('99')[1]:
												if headers[y] == 'Frequency (max)' or headers[y] == 'Frequency (min)':
													if str(x[i]) == 'None' or str(x[i]) == 'N/A' or str(x[i]) == '-':
														print('ERROR')
														pass
													else:
														fspec.append([headers[y], str(int(float(x[i])*1000))])
												else:
													fspec.append([headers[y], str(x[i])])

								for x in checkDups(fspec):
									fspecs[x[0]] = x[1]

								for x in fHeader[7:]:
									if x in fspecs:
										if str(fspecs[x]) == 'None' or str(fspecs[x]) == 'N/A' or str(fspecs[x]) == '-':
											fList.append('')
										else:
											fList.append(str(fspecs[x]))
									else:
										fList.append('')

								for x in fList[7:]:
									if x != '':
										append_list_as_row(filepathHeader, fList)
										break

							nxtPg += 100

				except Exception as e:
					print('ERROR: '+str(e))
					print(e)
				print('')

driver.quit()
# print(fieldHeaders)
# print('~~~')
# print(fieldSKU)
print('Done.')
