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

links = [[36, 76, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc0422a4b057c&collectionid=db3a304314dca389011502f07fe10b7b&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[2, 50, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc0424d4a06af&collectionid=db3a30431b3e89eb011bd4ee7aa07e61&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[2, 50, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc0422c9e058c&collectionid=db3a304314dca389011540e0498815e9&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[2, 50, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc0422ef80598&collectionid=db3a304314dca389011540e1d03815ed&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[39, 72, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc043906710ff&collectionid=db3a304344ae06150144b5aa2b150055&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[38, 74, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc04636a11636&collectionid=ff80808112ab681d0112ab6b2bb80750&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[38, 74, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc04644251656&collectionid=ff80808112ab681d0112ab6b2cf10754&collectiontype=Channel&showallopns=false&calculatefilters=true'],
		[38, 74, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc045eb851560&collectionid=ff80808112ab681d0112ab6b153c070c&collectiontype=Channel&showallopns=false&calculatefilters=true']]

# links = [[36, 76, 'https://www.infineon.com/products/pc/frontendprecalculation?tableconfigid=5546d46c5dc022bf015dc0422a4b057c&collectionid=db3a304314dca389011502f07fe10b7b&collectiontype=Channel&showallopns=false&calculatefilters=true']]

header = {'5546d4694909da48014909dc0f5e0238': 'Switch Type',
			'5546d4694909da48014909dbffb20140': 'Control Type',
			'5546d4694909da48014909dc03ca017d': 'Frequency (min)',
			'5546d4694909da48014909dc03ca017d1': 'Frequency (min)',
			'5546d4694909da48014909dc03ca017d2': 'Frequency (max)',
			'5546d4694909da48014909dc0f3d0234': 'Voltage (max)',
			'5546d4694909da48014909dbf7ef00c9': 'Isolation',
			'5546d4694909da48014909dbf6dc00bd': 'Insertion Loss (min)',
			'5546d4694909da48014909dc045d0187': 'Gain (max)',
			'5546d4694909da48014909dbfc6f0103': 'P1dB (dBm)',
			'5546d4694909da48014909dbfadb00e2': 'Noise Figure',
			'5546d4694909da48014909dc03c3017c': 'Frequency (min)',
			'5546d4694909da48014909dc03c3017c1': 'Frequency (min)',
			'5546d4694909da48014909dc03c3017c2': 'Frequency (max)',
			'5546d4694909da48014909dc04c2018f': 'Current (max)',
			'5546d462773f9324017742f6d64740d2': 'IP3',
			'5546d462773f9324017742edaae7404c': 'Gain (max)',
			'5546d462773f9324017742edaaff404e': 'P1dB (dBm)',
			'5546d46277921c320177cf5ebf477673': 'Package',
			'5546d46277fc743901783a3138c949d0': 'Voltage (max)',
			'5546d462773f9324017742edaaf3404d': 'Gain (max)',
			'5546d4694909da48014909dbfcbb0108': 'Max Input Power',
			'5546d4694909da48014909dbfc570101': 'Power',
			'8ac78c8c80f4d32901810410a25c0fdb': 'Noise Figure',
			'8ac78c8c80f4d32901810410a2660fdc': 'Gain (max)',
			'8ac78c8c80f4d32901810410a2740fdd': 'IP3',
			'8ac78c8c80f4d32901810419eade0fde': 'P1dB (dBm)',
			'8ac78c8c80027ecd0180610a97877b8a': 'Drain Voltage (max)',
			'8ac78c8c80027ecd0180610a97777b89': 'Drain Current (max)',
			'8ac78c8c80f4d3290181449dea874f26': 'Noise Figure',
			'8ac78c8c80f4d3290181449dea7c4f25': 'Gain (max)'}

manufacturer = 40

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Infineon_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])

append_list_as_row(filepathHeader, fHeader)
#########

specs = []
for x in links:
	session = requests.Session()
	response = session.get(x[2])

	soup = BeautifulSoup(response.text, features='lxml')
	site_json = json.loads(soup.text)

	for j in site_json['ispns']:
		print('['+str(links.index(x)+1)+'/'+str(len(links))+'] - '+str(site_json['ispns'].index(j)+1)+'/'+str(len(site_json['ispns'])))
		fList = [manufacturer, x[0], x[1], j['name']]

		with requests.Session() as s:
			r = s.get('https://www.infineon.com'+j['openCmsPath'])
			soup1 = BeautifulSoup(r.text, features='lxml')
			try:
				fList.append('https://www.infineon.com'+soup1.find_all("img", {"class":"img-responsive-lazy"})[1]['src'])
			except Exception as e:
				fList.append('')

		try:
			fList.append('https://www.infineon.com'+j['primaryDocumentUrl']['en'])
		except Exception as e:
			fList.append('')

		fList.append('https://www.infineon.com'+j['openCmsPath'])

		for y in fHeader[7:]:
			chk = ''
			for i in j['electricalParameterValues']:
				try:
					temp = ''
					if header[i['parameterId']] == y:
						if i['parameterId'] == '5546d4694909da48014909dc03ca017d' or i['parameterId'] == '5546d4694909da48014909dc03c3017c':
							if 'ghz' in i['stringValue'].lower():
								if '-' in i['stringValue']:
									temp = i['stringValue'].replace('GHz','').split('-')
								elif '–' in i['stringValue']:
									temp = i['stringValue'].replace('GHz','').split('–')
						if y == 'Frequency (min)':
							chk = str(float(temp[0])*1000)
							fList.append(chk)
							chk = str(float(temp[1])*1000)
						else:
							chk = i['stringValue']
				except Exception:
					try:
						temp = ''
						pid = j['parameterId'].split('_')[0]
						if header[pid] == y:
							if pid == '5546d4694909da48014909dc03ca017d' or pid == '5546d4694909da48014909dc03c3017c':
								if 'ghz' in i['nominalValueDisplayUnit'].lower():
									if '-' in i['nominalValueDisplayUnit']:
										temp = i['nominalValueDisplayUnit'].replace('GHz','').split('-')
									elif '–' in i['nominalValueDisplayUnit']:
										temp = i['nominalValueDisplayUnit'].replace('GHz','').split('–')
							if y == 'Frequency (min)':
								chk = str(float(temp[0])*1000)
								fList.append(chk)
								chk = str(float(temp[1])*1000)
							else:
								chk = i['nominalValueDisplayUnit']
					except Exception as e:
						pass
			fList.append(chk)
		append_list_as_row(filepathHeader, fList)
	time.sleep(2)























