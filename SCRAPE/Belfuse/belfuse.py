from datetime import datetime
from bs4 import BeautifulSoup
from csv import writer
import requests
import getpass
import math
import json
import time
import os

manufacturer = 102

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def getNum(num):
	result = ''.join([n for n in num if n.isdigit()])

	if result == '':
		return 0
	else:
		return result

links = [[1, 2, '6a5a1a2b-01b7-4d85-b453-f0db43e45179'],
		[1, 2, '6badf983-769a-4973-aef7-c5a178cfd476'],
		[1, 2, '3d695ee3-5353-4cb8-9c32-31296231b769'],
		[4, 8, 'b9594459-0a4b-4c53-9a88-bb37f1eb93c2'],
		[4, 8, '3653e322-ec09-4bb0-b1d7-54b297cff511'],
		[4, 8, 'c632a533-8caa-4ea1-8bd2-8a3a8d6b43ba'],
		[4, 8, 'd9f0a72c-5269-4cc1-abb6-395d9f6bfd90'],
		[4, 8, 'e4337119-52e0-4af8-9eea-dfb0735469bf'],
		[4, 8, '852df42a-cc85-4ef7-a1ad-3878a558a6f4'],
		[4, 8, 'e2fa8550-2b68-4932-8ae3-540b58ec1dfe'],
		[4, 8, '91f6a058-0cd1-474d-a1ae-e11eb168cdd3'],
		[4, 8, '1bb7b907-468c-4e08-b377-06bd9e07818e'],
		[4, 8, 'f880c5e4-5d5c-4b56-b3c5-57b3eb39ab18'],
		[4, 8, '55325a97-0402-4064-b68b-4c5213fdd267'],
		[4, 8, 'efde2d34-6b31-4ad0-9e6c-eea3b40586d3'],
		[11, 29, '2afcffdf-1b9a-44db-a4c0-1e6af9a7ed56'],
		[11, 47, '5821ea05-717b-4b00-b47e-e0cb89d64c51'],
		[13, 22, '57eec1f8-ffa5-4b6d-ad16-6c9d8dd62051'],
		[13, 22, '48b022ff-e974-4f6d-b900-508647659a76'],
		[13, 22, '5ee29903-6528-4cff-8d39-551dc0439228'],
		[22, 125, '581f331c-003d-4e19-b959-9a9621c53143'],
		[22, 125, '754f5ce6-9e90-4a10-9a04-39607cf390a7'],
		[22, 125, 'e3381db8-a235-4993-b1fc-0d98905ea9ff'],
		[22, 125, '0861a8ab-4cbd-43ad-bc5b-8279d8c66744'],
		[22, 125, '741e0941-6d87-491a-aa95-74f22915968d'],
		[22, 125, '05136e10-f60a-449c-a092-705eee869b83'],
		[22, 125, '8c861744-3f27-401e-af97-ad81aa064f49'],
		[22, 125, '9fa5f33c-cdd7-474a-a7d1-84a5b06cccce'],
		[22, 125, 'f6352b0c-28be-40b9-8f7c-523566a92681'],
		[22, 125, 'aa5c6056-6d64-4beb-8b7e-a9ab11f61b15'],
		[22, 125, '2be8de79-f9d4-466e-bfde-b5fa47dc194b'],
		[22, 125, '60d49ad3-3931-4515-9046-09a9aec103aa'],
		[22, 125, 'daa10633-efe2-4cb8-b57c-536e1b0d7259'],
		[22, 125, '0dcdc49d-adfb-4e1e-8cde-f32376dc415b'],
		[32, 69, '05fcf511-4a47-4131-b18d-708368bc05ef'],
		[32, 69, '051c2846-35eb-4ec0-ba87-49b63bccb70d']]

headers = {'Description': 'Description',
			'Freq Low (GHz)': 'Frequency (min)',
			'Freq High (GHz)': 'Frequency (max)',
			'Interface 1': 'Connector 1 Type',
			'Interface 2': 'Connector 2 Type',
			'Gender 1': 'Connector 1 gender',
			'Gender 2': 'Connector 2 gender',
			'VSWR': 'VSWR (single value or input/output)',
			'Insertion Loss (dB)': 'Insertion loss (min)',
			'Attenuation value (dB)': 'Attenuation (min)',
			'Coupling Value (dB)': 'Coupling',
			'Power (W)': 'Power',
			'Power Divisions': 'Power Split',
			'Body Material': 'Features',
			'Body Finish': 'Features'}

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Bel_Fuse_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link', 'Description', 'Frequency (min)', 'Frequency (max)', 'Connector 1 Type', 'Connector 2 Type', 'Connector 1 gender', 'Connector 2 gender', 'VSWR (single value or input/output)', 'Insertion loss (min)', 'Attenuation (min)', 'Coupling', 'Power', 'Power Split', 'Features']
append_list_as_row(filepathHeader, fHeader)
#########


allSpec = []
for l in links:
	err = 0
	while err == 0:
		try:
			session = requests.Session()
			response = session.get('https://www.belfuse.com/product/part-group-filter?pgroup_identifier='+l[2])

			soup = BeautifulSoup(response.text, features='lxml')
			site_json = json.loads(soup.text)

			for x in site_json['results']:
				for j in x['partNumbers']:
					fList = []
					fList.append(manufacturer)
					fList.append(l[0])
					fList.append(l[1])
					fList.append(j['partNumber'])

					response = session.get('https://www.belfuse.com/product/part-details?partn='+str(j['partNumber']))
					soup = BeautifulSoup(response.text, features='lxml')

					con = soup.find_all("img", {"class":"img-responsive"})[2]['src']
					fList.append('https://www.belfuse.com'+con)

					if str(j['resourceDocument']) != '{}':
						fList.append('https://www.belfuse.com'+str(j['resourceDocument']['Drawing']))
					else:
						fList.append('')

					fList.append('https://www.belfuse.com/product/part-details?partn='+j['partNumber'])

					for i in j:
						if str(i) == 'specifications':
							print('aaaa')
							for y in fHeader[7:]:
								newSpec, val, feat, con = '', '', '', 0
								print('MAIN: '+y)
								for k in j[i]:
									if str(k) == 'Freq Low (GHz)' or str(k) == 'Freq High (GHz)':
										newSpec = str(headers[k])
										val = str(float(getNum(j[i][k]))*1000)
										print('    '+str(headers[k])+': '+str(float(getNum(j[i][k]))*1000))
									elif str(k) == 'Body Material' or str(k) == 'Body Finish':
										feat += str(j[i][k])+', '
									else:
										newSpec = str(headers[k])
										val = str(j[i][k])
										print('    '+str(headers[k])+': '+str(j[i][k]))

									if y == newSpec:
										con += 1
										break
									# print('\n111')
									# print(newSpec)
									# print(y)
									# print('222\n')
									# if newSpec != '':
									# 	if y == newSpec:
									# 		fList.append(val)
									# 	else:
									# 		fList.append('')


								if y == 'Features':
									if feat[0:-2] != '':
										fList.append(feat[0:-2])
								else:
									if con == 0:
										fList.append('')
									else:
										fList.append(val)

							print('~~~')
						# else:
						# 	print(str(i)+': '+str(j[i]))
					print('~~~')
					append_list_as_row(filepathHeader, fList)
			err = 1
		except Exception as e:
			print('ERROR: '+str(e))
			# print(json.dumps(site_json, indent=4))
			err = 0
