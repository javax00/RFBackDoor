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

links = [[2, 90, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=amplifier-digital-vga&_=1661922252538'],
		[2, 90, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=amplifier-analog-vga&_=1661922252539'],
		[2, 67, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=amplifier-hpa&_=1661922252540'],
		[2, 50, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=amplifier-lna&_=1661922252541'],
		[2, 67, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=amplifier-mpa&_=1661922252542'],
		[4, 8, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=attenuator-analog&_=1661922252543'],
		[4, 26, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=attenuator-digital&_=1661922252544'],
		[39, 85, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=core-chip-rx-tx&_=1661922252545'],
		[31, 68, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=detector&_=1661922252546'],
		[23, 30, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=down-converter&_=1661922252547'],
		[38, 74, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=gan-power-transistor&_=1661922252548'],
		[38, 74, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=internally-matched-gan-power-transistor&_=1661922252549'],
		[23, 56, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=mixer&_=1661922252550'],
		[25, 58, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=multiplier&_=1661922252551'],
		[26, 60, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=oscillator-dro&_=1661922252552'],
		[26, 94, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=oscillator-vco&_=1661922252553'],
		[29, 66, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=phase-shifter&_=1661922252554'],
		[32, 69, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=power-divider-combiner&_=1661922252555'],
		[36, 76, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=switch&_=1661922252556'],
		[38, 74, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=transistor&_=1661922252557']]

# links = [[2, 90, 'https://www.ums-rf.com/wp-json/el/ums/get_products?term=amplifier-digital-vga&_=1661922252538']]

header = {'rf_bandwidth_ghz_min': 'Frequency (min)',# – convert to MHz
			'rf_bandwidth_ghz_max': 'Frequency (max)',# – convert to MHz
			'gain_db': 'Gain (max)',
			'noise_figure_db': 'Noise Figure',
			'dynamic_range_db': 'Dynamic Range',
			'p-1db_out_dbm': 'P1dB (dBm)',
			'sat_output_power_dbm': 'Saturated Power (Psat)',
			'bias_ma': 'Current (max)',
			'bias_v': 'Bias Voltage',
			'case': 'Package',
			'gain_flatness_db': 'Gain Flatness',
			'gain_control_range_db': 'Gain Control Range',
			'ip3_dbm': 'IP3',
			'pae': 'PAE',
			'insertion_loss_db': 'Insertion loss (min)',
			'amplitude_control_db': 'Attenuation Range',
			'p-1db_in_dbm': 'P1dB (dBm)',
			'number_of_bits': 'Control Bits',
			'control_voltage_v': 'Control Voltage (min)',
			'gain_rx_db': 'RX Gain',
			'gain_tx_db': 'TX Gain',
			'pout_rx_dbm': 'RX Output Power',
			'pout_tx_dbm': 'TX Output Power',
			'nf_rx_db': 'Noise Figure',
			'number_of_bit_atten': 'Control Bits',
			'number_of_bit_phase': 'Control Bits',
			'loss_db': 'Insertion loss (min)',
			'input_power_dbm': 'Max Input Power',
			'type': 'Features',
			'lo_bandwidth_ghz_min': 'LO Frequency (min)',# – convert to MHz
			'lo_bandwidth_ghz_max': 'LO Frequency (max)',# – convert to MHz
			'if_bandwidth_ghz_min': 'IF Frequency (min)',# – convert to MHz
			'if_bandwidth_ghz_max': 'IF Frequency (max)',# – convert to MHz
			'conv_gain_db': 'Conversion Gain',
			'lo_input_power_dbm': 'LO Power (max)',
			'operating_frequency_ghz': 'Frequency (max)',# – convert to MHz
			'saturated_power_w': 'Saturated Power (Psat)',# – convert to dBm
			'pae_a_freq_ghz': 'PAE',
			'small_signal_gain_db': 'Gain (max)',
			'power_w': 'Output Power',
			'associated_gain_db': 'Gain (max)',
			'dc_bias': 'Bias Voltage',
			'xn': 'Multiplication Factor',
			'input_bandwidth_ghz_min': 'Input Frequency (min)',# – convert to MHz
			'input_bandwidth_ghz_max': 'Input Frequency (max)',# – convert to MHz
			'output_bandwidth_ghz_min': 'Output Frequency (min)',# – convert to MHz
			'output_bandwidth_ghz_max': 'Output Frequency (max)',# – convert to MHz
			'output_power_dbm': 'Output Power',
			'central_output_freq_ghz': 'Frequency (max)',# – convert to MHz
			'tuning_mhz': 'Tuning Frequency (max)',
			'noise_a_100khz_dbc_hz': 'Phase Noise (min)',
			'tuning_bandwidth_ghz': 'Tuning Frequency (max)',
			'phase_range': 'Phase Range',
			'phase_error_p-p': 'Phase Error',
			'amplitude_unbalance_db': 'Amplitude Balance',
			'phase_unbalance': 'Phase Balance',
			'return_loss_db': 'Return Loss',
			'isolation_db': 'Isolation'}

manufacturer = 95

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/UMS_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])
append_list_as_row(filepathHeader, fHeader)
#########

dups = []
for x in links:
	session = requests.Session()
	response = session.get(x[2], timeout=20)

	soup = BeautifulSoup(response.text, features='lxml')
	site_json = json.loads(soup.text)

	for j in site_json:
		print('['+str(links.index(x)+1)+'/'+str(len(links))+'] - '+str(site_json.index(j)+1)+'/'+str(len(site_json)))
		fList = [manufacturer, x[0], x[1], j['reference_produit']]

		with requests.Session() as session1:
			session1 = requests.Session()
			response1 = session1.get(j['url'], timeout=20)
			soup1 = BeautifulSoup(response1.text, features='lxml')
			time.sleep(1)

			try:
				img = soup1.find_all("img")[1]['src']
			except Exception as e:
				img = ''

			try:
				pdf = soup1.find_all("a", {"class": "product-attachment_slide"})[0]['href']
			except Exception as e:
				pdf = ''

		fList.extend([img, pdf, j['url']])

		for y in fHeader[7:]:
			chk = ''
			for i in j:
				try:
					if header[i] == y:
						if i == 'rf_bandwidth_ghz_min' or i == 'rf_bandwidth_ghz_max' or i == 'lo_bandwidth_ghz_min' or i == 'lo_bandwidth_ghz_max' or i == 'if_bandwidth_ghz_min' or i == 'if_bandwidth_ghz_max' or i == 'operating_frequency_ghz' or i == 'input_bandwidth_ghz_min' or i == 'input_bandwidth_ghz_max' or i == 'output_bandwidth_ghz_min' or i == 'output_bandwidth_ghz_max' or i == 'central_output_freq_ghz':
							chk = str(int(float(j[i])*1000))
						elif i == 'saturated_power_w':
							chk = str(wToDbm(j[i]))
						else:
							chk = j[i]
						break
				except Exception:
					pass
			fList.append(chk)

		append_list_as_row(filepathHeader, fList)


















