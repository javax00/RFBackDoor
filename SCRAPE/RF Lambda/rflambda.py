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

links = [[1, 17, 'https://www.rflambda.com/search_coaxialadapter.jsp'],
		[1, 97, 'https://www.rflambda.com/search_wgadapter.jsp'],
		[2, 1, 'https://www.rflambda.com/search_acamplifier.jsp'],
		[2, 3, 'https://www.rflambda.com/search_alcautocontrolamplifier.jsp'],
		[2, 4, 'https://www.rflambda.com/search_bidirectionalamplifier.jsp'],
		[2, 45, 'https://www.rflambda.com/search_higheffeciencypoweramplifier.jsp'],
		[2, 50, 'https://www.rflambda.com/search_lownoiseamplifier.jsp'],
		[2, 52, 'https://www.rflambda.com/search_lowphasenoiseamplifier.jsp'],
		[2, 62, 'https://www.rflambda.com/search_frontoverdriveprotectedlna.jsp'],
		[2, 67, 'https://www.rflambda.com/search_poweramplifier.jsp'],
		[2, 90, 'https://www.rflambda.com/search_agcamplifier.jsp'],
		[3, 99, 'https://www.rflambda.com/search_wgantenna.jsp'],
		[4, 8, 'https://www.rflambda.com/search_attenuator.jsp'],
		[4, 26, 'https://www.rflambda.com/search_digitalprogrammableattenuator.jsp'],
		[4, 36, 'https://www.rflambda.com/search_wgattenuator.jsp'],
		[4, 53, 'https://www.rflambda.com/search_manualattenuator.jsp'],
		[4, 93, 'https://www.rflambda.com/search_voltageattenuator.jsp'],
		[4, 100, 'https://www.rflambda.com/search_wgmanualattenuator.jsp'],
		[7, 13, 'https://www.rflambda.com/search_rfcablesuperflex.jsp'],
		[7, 79, 'https://www.rflambda.com/search_testingcables.jsp'],
		[8, 92, 'https://www.rflambda.com/search_calibrationkits.jsp'],
		[10, 16, 'https://www.rflambda.com/search_circulator.jsp'],
		[10, 101, 'https://www.rflambda.com/search_wgcirculatorisolator.jsp'],
		[11, 29, 'https://www.rflambda.com/search_directionalcoupler.jsp'],
		[11, 29, 'https://www.rflambda.com/search_directionalcoupler.jsp'],
		[11, 47, 'https://www.rflambda.com/search_hybrid.jsp'],
		[11, 47, 'https://www.rflambda.com/search_hybrid.jsp'],
		[11, 47, 'https://www.rflambda.com/search_hybrid.jsp'],
		[11, 103, 'https://www.rflambda.com/search_wgcoupler.jsp'],
		[15, 32, 'https://www.rflambda.com/search_cavityduplexer.jsp'],
		[18, 104, 'https://www.rflambda.com/search_wgduplexer.jsp'],
		[16, 120, 'https://www.rflambda.com/search_filter.jsp'],
		[16, 120, 'https://www.rflambda.com/search_filter.jsp'],
		[16, 120, 'https://www.rflambda.com/search_filter.jsp'],
		[16, 59, 'https://www.rflambda.com/search_notchfilter.jsp'],
		[16, 105, 'https://www.rflambda.com/search_wgfilter.jsp'],
		[19, 43, 'https://www.rflambda.com/search_gantemplates.jsp'],
		[21, 49, 'https://www.rflambda.com/search_isolator.jsp'],
		[22, 18, 'https://www.rflambda.com/search_loadtermination.jsp'],
		[22, 55, 'https://www.rflambda.com/search_mismatchloadtermination.jsp'],
		[22, 107, 'https://www.rflambda.com/search_wgtermination.jsp'],
		[23, 30, 'https://www.rflambda.com/search_downconverter.jsp'],
		[23, 56, 'https://www.rflambda.com/search_mixer.jsp'],
		[23, 86, 'https://www.rflambda.com/search_upconverter.jsp'],
		[24, 57, 'https://www.rflambda.com/search_cavitydualfreqencycombiner.jsp'],
		[29, 5, 'https://www.rflambda.com/search_analogcontrolphaseshifter.jsp'],
		[29, 27, 'https://www.rflambda.com/search_digitalcontrolphaseshifter.jsp'],
		[29, 54, 'https://www.rflambda.com/search_phaseshifter.jsp'],
		[29, 108, 'https://www.rflambda.com/search_wgphaseshifter.jsp'],
		[31, 68, 'https://www.rflambda.com/search_powerdetector.jsp'],
		[31, 109, 'https://www.rflambda.com/search_wgpowerdetector.jsp'],
		[32, 19, 'https://www.rflambda.com/search_medpowercombinersplitter.jsp'],
		[32, 102, 'https://www.rflambda.com/search_wgcombiner.jsp'],
		[33, 70, 'https://www.rflambda.com/search_limiter.jsp'],
		[35, 75, 'https://www.rflambda.com/search_wgrotaryjoint.jsp'],
		[36, 33, 'https://www.rflambda.com/search_electromechanicalswitch.jsp'],
		[36, 76, 'https://www.rflambda.com/search_switchers.jsp'],
		[36, 87, 'https://www.rflambda.com/search_switchersusb.jsp'],
		[36, 111, 'https://www.rflambda.com/search_wgswitch.jsp'],
		[37, 78, 'https://www.rflambda.com/search_synthesizer.jsp'],
		[39, 85, 'https://www.rflambda.com/search_txrxmodel.jsp'],
		[41, 38, 'https://www.rflambda.com/search_wgflexible.jsp']]

# links = [[16, 120, 'https://www.rflambda.com/search_filter.jsp']]

header = {'1dbCompression': 'P1dB (dBm)',
			'accuracy': 'Accuracy',
			'ampBalance': 'Amplitude Balance',
			'AmplitudeStability': 'Amplitude Stability',
			'ampUnbalance': 'Amplitude Balance',
			'application': 'Features',
			'attenmax': 'Attenuation (max)',
			'attenstep': 'Attenuation Step Size',
			'attenuation': 'Attenuation (min)',
			'attenuationRange': 'Attenuation Range',
			'attenuationrange': 'Attenuation Range',
			'attenuationstep': 'Attenuation Step Size',
			'averageForwardPower': 'Average Power',
			'averagePower': 'Average Power',
			'averagepower': 'Average Power',
			'averagePowerStr': 'Average Power',
			'averageReversePower': 'Average Power',
			'avgPower': 'Average Power',
			'avgPowerHandling': 'Average Power',
			'band1freq': 'Frequency Band',
			'band1type': 'Features',
			'bandwidth': 'Bandwidth',
			'biasing': 'Voltage (min)',
			'bw': 'Bandwidth',
			'cablelength': 'Length',
			'ch2_h_freq': 'Frequency 2 (max)',
			'ch2_l_freq': 'Frequency 2 (min)',
			'channel': 'Channel',
			'channelRejection': 'Rejection',
			'coaxialType': 'Coax Type',
			'connector': 'Connector 1 Type',
			'connectora': 'Connector 1 Type',
			'connectorb': 'Connector 2 Type',
			'connectorName': 'Connector 1 Type',
			'connectorStr': 'Connector 1 Type',
			'connectorstr': 'Connector 1 Type', # SPLIT
			'control': 'Control Type',
			'controlProtocol': 'Control Type',
			'controltype': 'Control Type',
			'conversionGain': 'Conversion Gain',
			'conversiongain': 'Conversion Gain',
			'coupling': 'Coupling',
			'couplingPortType': 'Coupling Port Type',
			'ctrlBits': 'Control Bits',
			'current': 'Current (min)',
			'cwInputPower': 'Input Power Level (max)',
			'dcpower': 'Power',
			'dcPowerVolt': 'Voltage (max)',
			'degree': 'Configuration',
			'description': 'Description',
			'detecting': 'Detectable Power Level (min)',
			'directivity': 'Directivity',
			'efficiency': 'Drain Efficiency',
			'flangeType': 'Flange Type',
			'flatness': 'Amplitude Flatness',
			'forwardPower': 'Power',
			'freq': 'Frequency (min)', # SPLIT
			'freq_band': 'Frequency Band',
			'freqHoppingStep': 'Frequency Hopping Step',
			'from_connector': 'Connector 1 Type',
			'from_gender': 'Connector 1 gender',
			'gain': 'Gain (max)',
			'gain_rx': 'RX Gain',
			'gain_tx': 'TX Gain',
			'gender': 'Connector 1 gender',
			'gendera': 'Connector 1 gender',
			'genderb': 'Connector 2 gender',
			'h_freq': 'Frequency (max)',
			'h_freq_in': 'Input Frequency (max)',
			'h_freq_out': 'Output Frequency (max)',
			'h_freq_rx': 'Rx Frequency (max)',
			'h_freq_tx': 'TX Frequency (max)',
			'h_rejectionfreq': 'Lower Stopband Frequency (max)',
			'h_temperature': 'Temperature Range',
			'idq': 'Drain Current (min)',
			'if_h_freq': 'IF Frequency (max)',
			'if_l_freq': 'IF Frequency (min)',
			'ilripple': 'Insertion Loss Ripple',
			'Impdeance': 'Impedance',
			'impedance': 'Impedance',
			'inBandSpuriousRejection': 'Spurious Rejection',
			'inbandspurousrejection': 'Spurious Rejection',
			'inputDynamiticRange': 'Dynamic Range',
			'inputMaxPower': 'Max Input Power',
			'inputvswr': 'VSWR (single value or input/output)',
			'insertionLoss': 'Insertion loss (min)',
			'insertionloss': 'Insertion loss (min)',
			'insertLoss': 'Insertion loss (min)',
			'insertloss': 'Insertion loss (min)',
			'interface': 'Connector 1 Type',
			'isolation': 'Isolation',
			'l_freq': 'Frequency (min)',
			'l_freq_in': 'Input Frequency (min)',
			'l_freq_out': 'Output Frequency (min)',
			'l_freq_rx': 'Rx Frequency (min)',
			'l_freq_tx': 'TX Frequency (min)',
			'l_rejectionfreq': 'Lower Stopband Frequency (min)',
			'l_temperature': 'Temperature Range',
			'length': 'Length',
			'lowphasenoise': 'Phase Noise (min)',
			'm_ampUnbalance_max': 'Amplitude Balance',
			'm_insertLoss_max': 'Insertion loss (max)',
			'm_isolation_min': 'Insertion loss (min)',
			'm_phaseUnbalance_max': 'Phase Balance',
			'macrodefectdensity': 'Macrodefect Density',
			'material': 'Features',
			'maxFlatLeakage': 'Flat Leakage',
			'maxpower': 'Max Input Power',
			'nf': 'Noise Figure',
			'nf_rx': 'Noise Figure',
			'oip3': 'IP3',
			'outputPower': 'Output Power',
			'p1db': 'P1dB (dBm)',
			'p1db_rx': 'P1dB (dBm)',
			'p1db_tx': 'P1dB (dBm)',
			'packagingName': 'Package',
			'paepct': 'PAE',
			'passband': 'Lower Passband Frequency (min)',  # SPLIT
			'passband1': 'Lower Passband Frequency (min)',  # SPLIT
			'passband2': 'Lower Passband Frequency (max)',  # SPLIT
			'passband3': 'Upper Passband Frequency (min)',  # SPLIT
			'passband4': 'Upper Passband Frequency (max)',  # SPLIT
			'peakInputPower': 'Max Input Power',
			'peakMaxFlatLeakage1': 'Flat Leakage',
			'peakPower': 'Peak Power (max)',
			'peakpower': 'Peak Power (max)',
			'peakPowerHandling': 'Max Input Power',
			'phaseAdjustment': 'Phase Adjustments',
			'phaseBalance': 'Phase Balance',
			'phasedeviation': 'Phase Deviation',
			'phasenoise': 'Phase Noise (min)',
			'phaserange': 'Phase Range',
			'PhaseStability': 'Phase Stability',
			'pinnumber': 'Num Outputs',
			'plane': 'Plane',
			'polarity': 'Polarity',
			'ports': 'Ports',
			'power': 'Power',
			'powerHandling': 'Power',
			'rejection': 'Rejection',
			'resistivity': 'Resistivity',
			'resolution': 'Resolution',
			'returnloss': 'Return Loss',
			'rf_h_freq': 'RF Frequency (max)',
			'rf_l_freq': 'RF Frequency (min)',
			'sensitivity': 'Sensitivity',
			'size': 'Length',
			'speed': 'Speed',
			'splitterWays': 'Num Outputs',
			'spur': 'Spur Level',
			'spurious': 'Spur Level',
			'standardCase': 'Package',
			'step': 'Attenuation Step Size',
			'style': 'Features',
			'switchingSpeed': 'Switching Speed',
			'switchtype': 'Switch Type',
			'templateline': 'Template Line',
			'thicknessuniformity': 'Thickness Variation',
			'to_connector': 'Connector 2 Type',
			'to_gender': 'Connector 2 gender',
			'type': 'Switch Type',
			'volt': 'Voltage (max)',
			'voltage': 'Voltage (max)',
			'vswr': 'VSWR (single value or input/output)',
			'VSWR': 'VSWR (single value or input/output)',
			'waveguidetype': 'Waveguide Type',
			'waveguideType': 'Waveguide Type',
			'ways': 'Num Outputs'}

manufacturer = 83

#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/RFLambda_'+str(dt_string)+'.csv'
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
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
driver = webdriver.Chrome(options=options, desired_capabilities=capabilities, service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(5)
#########

specs = []
for link in links:
	driver.get(link[2])
	time.sleep(3)
	print(str(links.index(link)+1)+'-'+str(len(links)))

	logs_raw = driver.get_log("performance")
	logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

	def log_filter(log_):
		return (
			# is an actual response
			log_["method"] == "Network.responseReceived"
			# and json
			and "json" in log_["params"]["response"]["mimeType"]
		)

	for log in filter(log_filter, logs):
		lp = 0
		while lp == 0:
			try:
				request_id = log["params"]["requestId"]
				jsn = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
				datas = json.loads(jsn['body'])
				lp = 1
			except Exception as e:
				print('ERROR: Trying again.')
				time.sleep(5)
				lp = 0

		if 'items' in str(datas):
			for data in datas['items']:
				if 'h_temperature' in data and 'l_temperature' in data:
					temp1 = data['h_temperature']
					temp2 = data['l_temperature']
					del data['h_temperature']
					del data['l_temperature']
					data['h_temperature'] = str(temp1)+' - '+str(temp2)

				if 'connectorstr' in data and str(data['connectorstr']) != '' and ',' in str(data['connectorstr']):
					tmp = data['connectorstr'].split(',')
					temp1 = tmp[0]
					temp2 = tmp[1]
					del data['connectorstr']
					data['connectora'] = str(temp1)
					data['connectorb'] = str(temp2)

				if 'freq' in data and str(data['freq']) != '':
					if '-' in str(data['freq']) or '~' in str(data['freq']):
						try:
							tmp = data['freq'].split('~')
							temp1 = tmp[0]
							temp2 = tmp[1]
						except Exception as e:
							tmp = data['freq'].split('-')
							temp1 = tmp[0]
							temp2 = tmp[1]
						del data['freq']
						data['l_freq'] = str(temp1)
						data['h_freq'] = str(temp2)

				if 'passband' in data and str(data['passband']) != '':
					# print('passband')
					# print(data['passband'])
					# print('~')
					try:
						tmp1 = data['passband'].split('<br>')
						tmp2 = tmp1.split('~')
						temp1 = tmp1[0].tmp2[0]
						temp2 = tmp1[0].tmp2[1]
						temp3 = tmp1[1].tmp2[0]
						temp4 = tmp1[1].tmp2[1]
						del data['passband']
						data['passband1'] = str(temp1)
						data['passband2'] = str(temp2)
						data['passband3'] = str(temp3)
						data['passband4'] = str(temp4)
					except Exception:
						try:
							tmp = data['passband'].split('-')
							temp1 = tmp[0]
							temp2 = tmp[1]
							del data['passband']
							data['passband1'] = str(temp1)
							data['passband2'] = str(temp2)
						except Exception as e:
							tmp = data['passband'].split('<br>')
							temp1 = tmp[0]
							temp2 = tmp[1]
							del data['passband']
							data['passband1'] = str(temp1)
							data['passband2'] = str(temp2)

				fList = []
				fList.append(manufacturer)
				fList.append(link[0])
				fList.append(link[1])
				fList.append(data['S_PN'])
				fList.append('')
				if str(data['pdf']) != 'N/A':
					fList.append('https://www.rflambda.com'+str(data['pdf'])[1:])
				else:
					fList.append('')
				fList.append('')
				for y in fHeader[7:]:
					chk = ''
					for d in data:
						try:
							if header[d] == y:
								if d == 'l_freq' or d == 'h_freq':
									chk = str(int(float(data[d])*1000))
								else:
									chk = str(data[d])
								break
						except Exception:
							pass
					fList.append(chk)
				append_list_as_row(filepathHeader, fList)

# for x in specs:
# 	print(x)
driver.quit()




