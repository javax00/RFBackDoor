from datetime import datetime
from bs4 import BeautifulSoup
from csv import writer
import requests
import getpass
import math
import json
import time
import os

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def wToDbm(num):
	f = 10*math.log10(float(num))+30
	s = str(f).split('.')
	return float(s[0]+'.'+s[1][:2])

links = [[2, 4, '4f20de0b-cfd3-461d-b3fd-b2d629907b2d'],
		[38, 74, '51533c50-fb97-4b24-bd80-6cda9b700651'],
		[38, 74, 'b81abf82-d0c5-48b9-8aaf-3ffdd2f210d0'],
		[38, 74, 'ca5a20b1-8ede-4a62-ad44-5a31939231d1'],
		[38, 74, '28ad9141-71f2-4b22-87ba-54176584b06b'],
		[38, 74, '89fcf489-7e16-4697-9320-5287f9c2aebb'],
		[38, 74, '860cfee7-d954-4890-b928-7ff1d07c4322'],
		[38, 74, '08469d09-7720-4eb7-a8f6-382bac27d066'],
		[38, 74, '563cbe18-64ee-4725-8d78-cbc95385c3ed'],
		[38, 74, 'f4c59793-1208-461f-a319-2e5dba156fbe'],
		[38, 74, 'a9d71290-ff60-499d-91c8-ce5e7f9c6253'],
		[38, 74, '86177c91-6412-4943-9f58-467c941b6f22'],
		[38, 74, '7fbaabf5-d6dc-4d47-897a-94eb6b4e1d81'],
		[38, 74, '2f99cf9b-703e-4826-964f-149f2bbde262'],
		[38, 74, 'b571d514-b2e5-4c97-8d24-ca30578f5ad5'],
		[38, 74, '5f878d3e-7a6b-438b-bd18-b446ecb19977'],
		[38, 74, 'cba9167a-e953-44a6-9793-63f42a922ccf'],
		[38, 74, 'e24dc048-8ffc-47d1-a6ca-344ffe20ef12']]

headers = {'Package': 'Package',
			'GP (dB)': 'Gain (max)',
			'Die Technology': 'Features',
			'VDS (V)': 'Drain Voltage (max)',
			'ηD (%)': 'Drain Efficiency',
			'PL(1dB) (W)': 'P1dB (watts)',
			'PL(1dB) (dBm)': 'P1dB (dBm)',
			'Fmin (MHz)': 'Frequency (min)',
			'Fmax (MHz)': 'Frequency (max)',
			'Matching': 'Impedance',
			'PL(AV) (W)': 'Average Power'}

manufacturer = 6

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Ampleon_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in headers:
	if headers[x] not in fHeader:
		fHeader.append(headers[x])

append_list_as_row(filepathHeader, fHeader)
#########

for x in links:
	session = requests.Session()
	response = session.get('https://www.ampleon.com/.rest/parametricsearch/v2/search?cat='+x[2], timeout=20)

	soup = BeautifulSoup(response.text, features='lxml')
	site_json = json.loads(soup.text)

	for j in site_json['products']:
		fList = []
		fList.append(manufacturer)
		fList.append(x[0])
		fList.append(x[1])

		for y in j:
			if str(site_json['headlines'][y]) == 'Type Number':
				fList.append(str(j[y]['value']))
				fList.append('https://www.ampleon.com/.imaging/mte/ampleon-theme/productdetail/dam/images/products/'+str(j[y]['value'])+'.png/jcr:content/'+str(j[y]['value'])+'.png')

				###############
				# jayson = {}
				# jayson["image_link"] = 'https://www.ampleon.com/.imaging/mte/ampleon-theme/productdetail/dam/images/products/'+str(j[y]['value'])+'.png/jcr:content/'+str(j[y]['value'])+'.png'
				# jayson["manufacturer"] = 'Ampleon'
				# jayson["product"] = str(j[y]['value'])

				# url = 'https://l0or20ra19.execute-api.us-east-2.amazonaws.com/development/upload-on-s3'
				# r = requests.post(url, data=json.dumps(jayson))

				# print('~~~~~~~')
				# print(r.status_code)
				# fList.append(r.text)
				###############

				fList.append('https://www.ampleon.com/documents/data-sheet/'+str(j[y]['value'])+'.pdf')
				fList.append('https://www.ampleon.com/pip/'+str(j[y]['value']))

		for y in fHeader[7:]:
			conf = ''
			for k in j:
				if str(site_json['headlines'][k]) == 'Matching':
					if y == headers[str(site_json['headlines'][k])]:
						if str(j[k]['value']) != 'I' and str(j[k]['value']) != 'I/O' and str(j[k]['value']) != '-':
							conf = str(j[k]['value'])
				elif str(site_json['headlines'][k]) == 'PL(AV) (W)':
					if y == headers[str(site_json['headlines'][k])]:
						# print(j[k]['value'])
						if j[k]['value'] != None:
							conf = wToDbm(j[k]['value'])
				elif str(site_json['headlines'][k]) != 'Type Number' and str(site_json['headlines'][k]) != 'Test Signal' and str(site_json['headlines'][k]) != 'Status':
					if y == headers[str(site_json['headlines'][k])]:
						if str(j[k]['value']) != '-' and str(j[k]['value']) != 'None':
							conf = str(j[k]['value'])
			if conf != '':
				fList.append(conf)
			else:
				fList.append('')

		append_list_as_row(filepathHeader, fList)
		print(fList)

	time.sleep(5)
print('Done.')
