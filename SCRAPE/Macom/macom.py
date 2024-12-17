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

manufacturer = 49

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def is_float(value):
	try:
		if '.' in value:
			return float(value)
		else:
			return int(float(value))
	except Exception as e:
		return value

def specIndex(lst, item):
	return [i for i, x in enumerate(lst) if x == item]

links = [[2, 4, 'rf-microwave-mmwave/amplifiers/amplifier-gain-blocks'],
		[2, 4, 'rf-microwave-mmwave/amplifiers/catv/catv-amplifiers'],
		[2, 4, 'rf-microwave-mmwave/amplifiers/catv/fttx-amplifiers'],
		[2, 4, 'rf-microwave-mmwave/amplifiers/distributed-amplifiers'],
		[2, 4, 'rf-microwave-mmwave/amplifiers/hybrid-amplifiers/hybrid-amplifiers-gain-block'],
		[2, 4, 'rf-microwave-mmwave/amplifiers/hybrid-amplifiers/hybrid-amplifiers-limiting'],
		[2, 50, 'rf-microwave-mmwave/amplifiers/hybrid-amplifiers/hybrid-amplifiers-lna'],
		[2, 4, 'rf-microwave-mmwave/amplifiers/linear-amplifiers'],
		[2, 50, 'rf-microwave-mmwave/amplifiers/low-noise-amplifiers'],
		[2, 52, 'rf-microwave-mmwave/amplifiers/low-phase-noise-amplifiers'],
		[2, 67, 'rf-microwave-mmwave/amplifiers/rf-power-amplifiers/power-amplifiers-MMICs'],
		[2, 67, 'rf-microwave-mmwave/amplifiers/rf-power-amplifiers/rf-power-amplifiers-5W'],
		[2, 67, 'rf-microwave-mmwave/amplifiers/rf-power-amplifiers/rf-power-pallet-modules'],
		[2, 90, 'rf-microwave-mmwave/amplifiers/variable-gain-amplifiers'],
		[2, 50, 'rf-microwave-mmwave/integrated-ics--modules/switch-lnas'],
		[4, 26, 'rf-microwave-mmwave/attenuators/digital-attenuators'],
		[4, 8, 'rf-microwave-mmwave/attenuators/fixed_attenuators'],
		[4, 93, 'rf-microwave-mmwave/attenuators/voltage-variable-attenuators'],
		[4, 48, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/resistor-products-attenuator-pads'],
		[5, 9, 'rf-microwave-mmwave/transformers-baluns'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/capacitors/capacitors-beamlead'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/capacitors/capacitors-binary-chip'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/capacitors/capacitors-dc-floating-rf-bypass-mounting'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/capacitors/capacitors-high-q-mnos-series'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/capacitors/capacitors-mns-series'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/capacitors/capacitors-mnos-series'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/kv-caps-1/200_v'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/kv-caps-1/500v'],
		[9, 15, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/kv-caps-1/1000v'],
		[11, 20, 'rf-microwave-mmwave/couplers'],
		[44, 127, 'rf-microwave-mmwave/diodes/PIN-Diodes/pin-limiter-diodes'],
		[44, 127, 'rf-microwave-mmwave/diodes/PIN-Diodes/pin-switch-and-attenuator-diodes'],
		[44, 127, 'rf-microwave-mmwave/diodes/varactor-multiplier-diodes'],
		[44, 127, 'rf-microwave-mmwave/diodes/schottky-diodes/schottky-mixer-and-detector-diodes'],
		[44, 127, 'rf-microwave-mmwave/diodes/schottky-diodes/thzdiodes'],
		[44, 127, 'rf-microwave-mmwave/diodes/varactor-tuning-diodes'],
		[14, 77, 'rf-microwave-mmwave/switches/cmos-switch-drivers'],
		[16, 28, 'rf-microwave-mmwave/filters-diplexers'],
		[20, 126, 'rf-microwave-mmwave/Capacitors-Resistors-Inductors/inductor-products'],
		[23, 30, 'rf-microwave-mmwave/frequency-conversion/downconverter'],
		[23, 56, 'rf-microwave-mmwave/frequency-conversion/hybrid-mixers'],
		[23, 56, 'rf-microwave-mmwave/frequency-conversion/mixers'],
		[23, 86, 'rf-microwave-mmwave/frequency-conversion/up-converters'],
		[25, 58, 'rf-microwave-mmwave/frequency-conversion/frequency-multipliers'],
		[26, 94, 'rf-microwave-mmwave/frequency-generation/voltage-controlled-oscillators'],
		[27, 11, 'rf-microwave-mmwave/bias-networks'],
		[28, 64, 'rf-microwave-mmwave/phase-detectors'],
		[29, 27, 'rf-microwave-mmwave/digital-phase-shifters'],
		[31, 68, 'rf-microwave-mmwave/power-detectors'],
		[32, 69, 'rf-microwave-mmwave/amplifiers/catv/active-splitters'],
		[32, 69, 'rf-microwave-mmwave/power-dividers-combiners'],
		[33, 70, 'rf-microwave-mmwave/limiters'],
		[36, 76, 'rf-microwave-mmwave/integrated-ics--modules/high-power-switch-bias-module'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-dpdt'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-limiter'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-spst'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-spdt'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-sp3t'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-sp4t'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-sp5t'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-sp6t'],
		[36, 76, 'rf-microwave-mmwave/switches/switches-sp8t'],
		[37, 78, 'rf-microwave-mmwave/frequency-generation/comb-generators'],
		[38, 74, 'rf-microwave-mmwave/amplifiers/rf-power-amplifiers/rf-power-transistors-silicon-bipolar'],
		[38, 74, 'rf-microwave-mmwave/amplifiers/rf-power-amplifiers/rf-power-transistors-silicon-mosfet'],
		[39, 72, 'rf-microwave-mmwave/frequency-conversion/receivers'],
		[39, 80, 'rf-microwave-mmwave/frequency-conversion/transceivers'],
		[39, 85, 'rf-microwave-mmwave/integrated-ics--modules/transmit_receive_front_end_modules']]

# links = [[2, 4, 'rf-microwave-mmwave/amplifiers/amplifier-gain-blocks']]

# specs = ['Amplitude Balance',
# 		'Attenuation Range',
# 		'Attenuation Step Size',
# 		'Bandwidth',
# 		'Bias Voltage',
# 		'Configuration',
# 		'Conversion Gain',
# 		'Conversion Loss',
# 		'Coupling',
# 		'Current (max)',
# 		'CW Input Power (dBm)',
# 		'Description',
# 		'Detectable Power Level (min)',
# 		'Drain Current (max)',
# 		'Drain Efficiency',
# 		'Features',
# 		'Flat Leakage',
# 		'Frequency (max)',
# 		'Frequency (min)',
# 		'Gain (min)',
# 		'Gain Flatness',
# 		'IF Frequency (min)',
# 		'IF Frequency (max)',
# 		'Image Rejection',
# 		'Impedance Ratio',
# 		'Input Frequency (min)',
# 		'Input Frequency (max)',
# 		'Input Power Level (min)',
# 		'Input Power Level (max)',
# 		'Insertion loss (min)',
# 		'IP3',
# 		'Isolation',
# 		'LO Power (max)',
# 		'LO/RF Frequency (min)',
# 		'LO/RF Frequency (max)',
# 		'LO/RF Isolation',
# 		'Lower Passband Insertion Loss',
# 		'Max Input Power',
# 		'Multiplication Factor',
# 		'Noise Figure',
# 		'Number of Channels',
# 		'Output Frequency (min)',
# 		'Output Frequency (max)',
# 		'Output Power',
# 		'P01db',
# 		'P1dB (dBm)',
# 		'Package',
# 		'PAE',
# 		'Peak Power (min)',
# 		'Phase Balance',
# 		'Phase Error',
# 		'Phase Noise (min)',
# 		'Phase Noise (max)',
# 		'Phase Range',
# 		'Phase Shifter Bits',
# 		'Power',
# 		'Power Limit',
# 		'Pulse width',
# 		'Recovery Time',
# 		'Rejection',
# 		'RX Gain',
# 		'Saturated Power (Psat)',
# 		'Step Attenuator Bits',
# 		'Switching Speed',
# 		'Temperature Range',
# 		'TX Gain',
# 		'Voltage (max)',
# 		'Harmonic Level (min)',
# 		'Harmonic Level (max)',
# 		'VSWR (single value or input/output']

# allowed = {'Operating Frequency (GHz)': 'Operating Frequency (NOT INCLUDED)', #CONVERT IF NEEDED
# 			'Output Harmonics 1': 'Harmonic Level (min)',
# 			'Output Harmonics 2': 'Harmonic Level (max)',
# 			'Output Harmonics 3': 'Harmonic Level (NOT INCLUDED)',
# 			'Amplitude Balance (dB)': 'Amplitude Balance',
# 			'Attenuator (bit count)': 'Step Attenuator Bits',
# 			'Attenuator Range (dB)': 'Attenuation Range',
# 			'Bias Current': 'Drain Current (max)',
# 			'Bias Current (mA)': 'Drain Current (max)',
# 			'Bias Voltage': 'Bias Voltage',
# 			'Bias Voltage (V)': 'Bias Voltage',
# 			'Configuration': 'Configuration',
# 			'Conversion Gain (dB)': 'Conversion Gain',
# 			'Conversion Loss (dB)': 'Conversion Loss',
# 			'Coupling, Nominal (dB)': 'Coupling',
# 			'CW Incident Power (W)': 'CW Input Power (dBm)',
# 			'CW Input Power (dBm)': 'CW Input Power (dBm)',
# 			'DC Current (mA)': 'Current (max)',
# 			'DC Power': 'Power',
# 			'Efficiency': 'Drain Efficiency',
# 			'Efficiency (%)': 'Drain Efficiency',
# 			'Features': 'Features',
# 			'Gain (dB)': 'Gain (min)',
# 			'Gain Flatness (db)': 'Gain Flatness',
# 			'IF Bandwidth': 'Bandwidth',
# 			'IIP3  (dBm)': 'IP3',
# 			'IIP3 (dBm)': 'IP3',
# 			'Image Rejection  (dBm)': 'Image Rejection',
# 			'Impedance Ratio': 'Impedance Ratio',
# 			'Input Frequency max (MHz)': 'Input Frequency (max)',
# 			'Input Frequency min (MHz)': 'Input Frequency (min)',
# 			'Input P0.1dB (dBm)': 'P01db',
# 			'Input P1dB (dBm)': 'Input Power Level (max)',
# 			'Input Power (dBm)': 'Input Power Level (min)',
# 			'Insertion Loss': 'Insertion loss (min)',
# 			'Insertion Loss (dB)': 'Insertion loss (min)',
# 			'IP0.1 dB (dBm)': 'P01db',
# 			'IP0.1dB  (dBm)': 'P01db',
# 			'IP1.0 dB (dBm)': 'P1dB (dBm)',
# 			'IP1dB (dBm)': 'P1dB (dBm)',
# 			'Isolation (dB)': 'Isolation',
# 			'Isolation LO-RF (dB)': 'LO/RF Isolation',
# 			'Leakage (mW)': 'Flat Leakage',
# 			'LO Drive (dBm)': 'LO Power (max)',
# 			'LO Input Power  (dBm)': 'LO Power (max)',
# 			'Low Insertion Loss (Transmit) (dB)': 'Lower Passband Insertion Loss',
# 			'Min Frequency (GHz)': 'Frequency (min)', #STICK TO ONE
# 			'Min Frequency (MHz)': 'Frequency (min)', #STICK TO ONE
# 			'Max Frequency (GHz)': 'Frequency (max)', #STICK TO ONE
# 			'Max Frequency (MHz)': 'Frequency (max)', #STICK TO ONE
# 			'Max Frequency, IF (MHz)': 'IF Frequency (max)',
# 			'Max Frequency, RF/LO (MHz)': 'LO/RF Frequency (max)',
# 			'Max Input Frequency (MHz)': 'Input Frequency (max)',
# 			'Max Input Power (dBm)': 'Max Input Power',
# 			'Max Output Frequency (MHz)': 'Output Frequency (max)',
# 			'Min Detectible Signal': 'Detectable Power Level (min)',
# 			'Min Frequency, IF (MHz)': 'IF Frequency (min)',
# 			'Min Frequency, RF/LO (MHz)': 'LO/RF Frequency (min)',
# 			'Min Input Frequency (MHz)': 'Input Frequency (min)',
# 			'Min Output Frequency (MHz)': 'Output Frequency (min)',
# 			'Multiply Factor': 'Multiplication Factor',
# 			'NF (dB)': 'Noise Figure',
# 			'Noise Figure (dB)': 'Noise Figure',
# 			'Number of Channels': 'Number of Channels',
# 			'OIP3 (dBm)': 'IP3',
# 			'Operating Current (mA)': 'Current (max)',
# 			'Operating Temp Range (?C)': 'Temperature Range',
# 			'Operating Voltage (VDC)': 'Voltage (max)',
# 			'Output Limiting Level (dBm)': 'Power Limit',
# 			'Output P1dB (dBm)': 'P1dB (dBm)',
# 			'Output Power (mW)': 'Output Power',
# 			'Package': 'Package',
# 			'Package Type': 'Package',
# 			'PAE (%)': 'PAE',
# 			'Peak Power (W)': 'Peak Power (min)',
# 			'Phase Angle (Degrees)': 'Phase Range',
# 			'Phase Balance (deg)': 'Phase Balance',
# 			'Phase Noise (10KHz)': 'Phase Noise (min)',
# 			'Phase Noise 100KHz Offset (dBc/Hz)': 'Phase Noise (max)',
# 			'Phase Shifter  (bit count)': 'Phase Shifter Bits',
# 			'Pout (W)': 'Output Power',
# 			'Pout at Fo (dBm)': 'Output Power',
# 			'Power, Maximum (W)': 'Max Input Power',
# 			'Power, Min Detectable (dBm)': 'Detectable Power Level (min)',
# 			'Psat (dBm)': 'Saturated Power (Psat)',
# 			'PSAT (W)': 'Saturated Power (Psat)',
# 			'Pulse Width (�S)': 'Pulse width',
# 			'Receive Gain (dB)': 'Rx Gain',
# 			'Receive Isolation (dB)': 'Isolation',
# 			'Receive Noise Figure (dBm)': 'Noise Figure',
# 			'Recovery Time (ns)': 'Recovery Time',
# 			'Rejection (dB)': 'Rejection',
# 			'RF Power (W)': 'Output Power',
# 			'RMS Phase Error (deg)': 'Phase Error',
# 			'Rx Gain (dB)': 'RX Gain',
# 			'RX Gain (dB)': 'RX Gain',
# 			'RX Noise Figure (dB)': 'Noise Figure',
# 			'Rx Noise Figure (NF) (dB)': 'Noise Figure',
# 			'Rx OIP3 (dBm)': 'IP3',
# 			'Rx Output P1dB (dBm)': 'P1dB (dBm)',
# 			'Short Description': 'Description',
# 			'Step Size (dB)': 'Attenuation Step Size',
# 			'Supply Voltage (V)': 'Voltage (max)',
# 			'Switching 10 - 90% (us)': 'Switching Speed',
# 			'Switching 90 -100% (us)': 'Switching Speed',
# 			'Transmit Gain (dB)': 'Tx Gain',
# 			'Transmit P1dB (dBm)': 'P1dB (dBm)',
# 			'TX Gain (dB)': 'TX Gain',
# 			'Tx Input P0.1dB CW (dBm)': 'Input Power Level (max)',
# 			'Tx Insertion Loss (dB)': 'Insertion loss (min)',
# 			'Type': 'Features',
# 			'Vdd (V)': 'Voltage (max)',
# 			'VSWR': 'VSWR (single value or input/output)'}

specs = ['Amplitude Balance',
		'Attenuation Range',
		'Drain Current (max)',
		'Bias Voltage',
		'Conversion Gain',
		'Conversion Loss',
		'Coupling',
		'CW Input Power (dBm)',
		'Current (max)',
		'Drain Efficiency',
		'Description',
		'Gain (min)',
		'Gain Flatness',
		'IP3',
		'Image Rejection',
		'Impedance Ratio',
		'Input Frequency (max)',
		'Input Frequency (min)',
		'P01db',
		'Input Power Level (max)',
		'Input Power Level (min)',
		'Insertion loss (min)',
		'P1dB (dBm)',
		'Isolation',
		'LO/RF Isolation',
		'Flat Leakage',
		'LO Power (max)',
		'Frequency (min)',
		'Frequency (max)',
		'IF Frequency (max)',
		'LO/RF Frequency (max)',
		'Max Input Power',
		'Output Frequency (max)',
		'IF Frequency (min)',
		'LO/RF Frequency (min)',
		'Output Frequency (min)',
		'Noise Figure',
		'Number of Channels',
		'Voltage (max)',
		'Power Limit',
		'Output Power',
		'Peak Power (min)',
		'Phase Balance',
		'Phase Noise (min)',
		'Phase Noise (max)',
		'Detectable Power Level (min)',
		'Saturated Power (Psat)',
		'Recovery Time',
		'Rejection',
		'Phase Error',
		'RX Gain',
		'Attenuation Step Size',
		'Switching Speed',
		'TX Gain',
		'VSWR (single value or input/output)']

allowed = {'Amplitude Balance (dB)': 'Amplitude Balance',
			'Attenuator Range (dB)': 'Attenuation Range',
			'Bias Current (mA)': 'Drain Current (max)',
			'Bias Voltage': 'Bias Voltage',
			'Bias Voltage (V)': 'Bias Voltage',
			'Conversion Gain (dB)': 'Conversion Gain',
			'Conversion Loss (dB)': 'Conversion Loss',
			'Coupling, Nominal (dB)': 'Coupling',
			'CW Incident Power (W)': 'CW Input Power (dBm)',
			'CW Input Power (dBm)': 'CW Input Power (dBm)',
			'DC Current (mA)': 'Current (max)',
			'description': 'Description',
			'Efficiency (%)': 'Drain Efficiency',
			'Gain (dB)': 'Gain (min)',
			'Gain Flatness (db)': 'Gain Flatness',
			'IIP3  (dBm)': 'IP3',
			'IIP3 (dBm)': 'IP3',
			'Image Rejection  (dBm)': 'Image Rejection',
			'Impedance Ratio': 'Impedance Ratio',
			'Input Frequency max (MHz)': 'Input Frequency (max)',
			'Input Frequency min (MHz)': 'Input Frequency (min)',
			'Transmit Input P0.1dB CW (dBm)': 'P01db',
			'Input P1dB (dBm)': 'Input Power Level (max)',
			'Input Power (dBm)': 'Input Power Level (min)',
			'Insertion Loss  (dB)': 'Insertion loss (min)',
			'Insertion Loss (dB)': 'Insertion loss (min)',
			'IP0.1 dB (dBm)': 'P01db',
			'IP0.1dB  (dBm)': 'P01db',
			'IP1dB (dBm)': 'P1dB (dBm)',
			'Isolation (dB)': 'Isolation',
			'Isolation LO-RF (dB)': 'LO/RF Isolation',
			'Leakage (mW)': 'Flat Leakage',
			'LO Drive (dBm)': 'LO Power (max)',
			'LO Input Power  (dBm)': 'LO Power (max)',
			'Min Frequency (GHz)': 'Frequency (min)', #STICK TO ONE
			'Min Frequency (MHz)': 'Frequency (min)', #STICK TO ONE
			'Max Frequency (GHz)': 'Frequency (max)', #STICK TO ONE
			'Max Frequency (MHz)': 'Frequency (max)', #STICK TO ONE
			'Max Frequency, IF (MHz)': 'IF Frequency (max)',
			'Max Frequency, RF/LO (MHz)': 'LO/RF Frequency (max)',
			'Max Input Frequency (MHz)': 'Input Frequency (max)',
			'Max Input Power (dBm)': 'Max Input Power',
			'Max Output Frequency (MHz)': 'Output Frequency (max)',
			'Min Frequency, IF (MHz)': 'IF Frequency (min)',
			'Min Frequency, RF/LO (MHz)': 'LO/RF Frequency (min)',
			'Min Input Frequency (MHz)': 'Input Frequency (min)',
			'Min Output Frequency (MHz)': 'Output Frequency (min)',
			'NF (dB)': 'Noise Figure',
			'Noise Figure (dB)': 'Noise Figure',
			'Number of Channels (None)': 'Number of Channels',
			'OIP3 (dBm)': 'IP3',
			'Operating Current (mA)': 'Current (max)',
			'Operating Voltage (VDC)': 'Voltage (max)',
			'Output Limiting Level (dBm)': 'Power Limit',
			'Output P1dB (dBm)': 'P1dB (dBm)',
			'Output Power (mW)': 'Output Power',
			'Peak Power (W)': 'Peak Power (min)',
			'Phase Balance (deg)': 'Phase Balance',
			'Phase Noise 10KHz': 'Phase Noise (min)',
			'Phase Noise 100KHz Offset (dBc/Hz)': 'Phase Noise (max)',
			'Pout (W)': 'Output Power',
			'Pout at Fo (dBm)': 'Output Power',
			'Power, Maximum (W)': 'Max Input Power',
			'Power,Min Detectable (dBm)': 'Detectable Power Level (min)',
			'PSAT (W)': 'Saturated Power (Psat)',
			'Receive Isolation (dB)': 'Isolation',
			'Rx Noise Figure (NF) (dB)': 'Noise Figure',
			'Recovery Time (ns)': 'Recovery Time',
			'Rejection (dB)': 'Rejection',
			'RF Power (W)': 'Output Power',
			'RMS Phase Error (deg)': 'Phase Error',
			'Rx Gain (dB)': 'RX Gain',
			'RX Gain (dB)': 'RX Gain',
			'RX Noise Figure (dB)': 'Noise Figure',
			'Rx Noise Figure (NF) (dB)': 'Noise Figure',
			'Rx OIP3 (dBm)': 'IP3',
			'Rx Output P1dB (dBm)': 'P1dB (dBm)',
			'Step Size (dB)': 'Attenuation Step Size',
			'Supply Voltage (V)': 'Voltage (max)',
			'Switching 10 - 90% (us)': 'Switching Speed',
			'Switching 90 -100% (us)': 'Switching Speed',
			'Transmit Gain (dB)': 'Tx Gain',
			'Transmit P1dB (dB)': 'P1dB (dBm)',
			'Transmit Gain (dB)': 'TX Gain',
			'Tx Input P0.1dB CW (dBm)': 'Input Power Level (max)',
			'Tx Insertion Loss (dB)': 'Insertion loss (min)',
			'Vdd (V)': 'Voltage (max)',
			'VSWR (None)': 'VSWR (single value or input/output)'}

u = open("/Users/b2y/Work/RFBackDoor/Files/assets/users.txt", "r")
data = u.read()
users = data.split('\n')

s = open("/Users/b2y/Work/RFBackDoor/Files/assets/sites.txt", "r")
data = s.read()
sites = data.split('\n')

username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

# GET IMPORTANT HEADERS

fHead = []
fHead.extend(['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link'])
for x in specs:
	fHead.append(x)
now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Macom_'+str(dt_string)+'.csv'
append_list_as_row(filepathHeader, fHead)

head = []
for x in links:
	print(str(links.index(x)+1)+' - '+str(len(links))+' - '+'https://www.macom.com/products/'+x[2])
	cat = x[0]
	subCat = x[1]

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
	response = session.get('https://www.macom.com/products/'+x[2], headers=headers)
	soup = BeautifulSoup(response.text, features='lxml')
	tr = soup.find_all("tr")
	for td in tr:
		temp = []
		final = []
		final.append(manufacturer)
		final.append(cat)
		final.append(subCat)

		for y in json.loads(td['data-part']):
			if y == 'specs':
				for j in json.loads(td['data-part'])[y]:
					try:
						temp.append([str(j['specName'])+' ('+str(j['uom'])+')', str(j['value'])])
					except Exception:
						temp.append([str(j['specName']), str(j['value'])])
					# print(str(j['specName'])+' ('+str(j['uom'])+')--'+str(j['value']))
			elif y != 'attributes':
				# print(y+'--'+str(json.loads(td['data-part'])[y]))
				temp.append([y, str(json.loads(td['data-part'])[y])])

		# part#
		for tmp in temp:
			if tmp[0] == 'partNumber':
				final.append(tmp[1])

		# img
		final.append('')

		# pdf
		for tmp in temp:
			if tmp[0] == 'datasheetHref':
				final.append(tmp[1])

		# link
		for tmp in temp:
			if tmp[0] == 'partUrl':
				final.append('https://www.macom.com/products'+tmp[1])

		for spec in specs:
			con = ''
			for tmp in temp:
				if tmp[0] in allowed and allowed[tmp[0]] == spec:
					if 'ghz' in tmp[0].lower():
						con = str(float(tmp[1])*1000).split('.')[0]
					else:
						con = tmp[1]
					break
			if con != '':
				final.append(con)
			else:
				final.append('')

		# for tmp in temp:
		# 	print(tmp)
		append_list_as_row(filepathHeader, final)
		# print('')






#	thead = soup.find("table", {"class"~"table"})#.find_all("th")
#	print(thead)
# 	tbody = soup.find("tbody").find_all("tr")

# 	# EXTRACT FROM WEBSITE
# 	data = []
# 	head = []
# 	body = []

# 	for y in thead:
# 		head.append(y.text.strip())
# 	data.append(head)

# 	for y in tbody:
# 		td = y.find_all("td")
# 		for yy in td:
# 			body.append(yy.text.strip())
# 		data.append(body)
# 		body = []

# 	# GET IMPORTANT BODY

# 	fData = []
# 	fBody = []


# 	for y in data[1:len(data)]:
# 		fBody.append(manufacturer)
# 		fBody.append(cat)
# 		fBody.append(subCat)
# 		if 'Part Number' in data[0]:
# 			c = 0
# 			for x in data[0]:
# 				if 'Part Number' == x:
# 					fBody.append(y[c])
# 				c += 1
# 		else:
# 			fBody.append('')

# 		if 'Product Image' in data[0]:
# 			c = 0
# 			for x in data[0]:
# 				if 'Product Image' == x:
# 					if str(y[c]) != '':
# 						fBody.append('https://cdn.macom.com/product_images/'+str(y[c]).replace(' ', '%20'))
# 					else:
# 						fBody.append('')
# 				c += 1
# 		else:
# 			fBody.append('')

# 		if 'Datasheet' in data[0]:
# 			c = 0
# 			for x in data[0]:
# 				if 'Datasheet' == x:
# 					if str(y[c]) != '':
# 						fBody.append('https://cdn.macom.com/datasheets/'+str(y[c]).replace(' ', '%20'))
# 					else:
# 						fBody.append('')
# 				c += 1
# 		else:
# 			fBody.append('')

# 		if 'Part Number' in data[0]:
# 			c = 0
# 			for x in data[0]:
# 				if 'Part Number' == x:
# 					fBody.append('https://www.macom.com/products/product-detail/'+str(y[c]))
# 				c += 1
# 		else:
# 			fBody.append('')

# 		# NEED TO CONVERT
# 		# Operating Frequency (GHz)

# 		for x in specs:
# 			freqMinCon = ''
# 			freqMaxCon = ''

# 			ky = ''
# 			con = []
# 			for key, val in allowed.items():
# 				if val == x:
# 					con.append(key)
# 			indCon = []
# 			if con != []:
# 				for j in con:
# 					try:
# 						indCon.append(data[0].index(j))
# 						ky = j
# 					except Exception:
# 						pass

# 				try:
# 					ind = data[0].index('Operating Frequency (GHz)')
# 					# print('Operating Frequency (GHz): '+str(y[ind]))

# 					fr = re.findall(r'[\d\.\d]+', y[ind])
# 					if len(fr) == 2:
# 						if 'ghz' in y[ind].lower():
# 							freqMinCon = is_float(fr[0])*1000
# 							freqMaxCon = is_float(fr[1])*1000
# 						else:
# 							freqMinCon = is_float(fr[0])
# 							freqMaxCon = is_float(fr[1])
# 					else:
# 						freqMinCon = is_float(fr[0])
# 				except Exception as e:
# 					pass

# 				harLev = []

# 				try:
# 					oh1 = data[0].index('Output Harmonics 1')

# 					frD1 = int(re.findall(r'[\d\.\-\d]+', y[oh1])[0])
# 					harLev.append(frD1)
# 				except Exception as e:
# 					pass

# 				try:
# 					oh2 = data[0].index('Output Harmonics 2')

# 					frD2 = int(re.findall(r'[\d\.\-\d]+', y[oh2])[0])
# 					harLev.append(frD2)
# 				except Exception as e:
# 					pass

# 				try:
# 					oh3 = data[0].index('Output Harmonics 3')

# 					frD3 = int(re.findall(r'[\d\.\-\d]+', y[oh3])[0])
# 					harLev.append(frD3)
# 				except Exception as e:
# 					pass

# 				if x == 'Harmonic Level (min)' and harLev != []:
# 					print(x+': '+str(min(harLev)))
# 					fBody.append(min(harLev))
# 				elif x == 'Harmonic Level (max)' and harLev != []:
# 					print(x+': '+str(max(harLev)))
# 					fBody.append(max(harLev))
# 				elif x == 'Frequency (min)' and freqMinCon != '':
# 					print(x+': '+str(freqMinCon))
# 					fBody.append(freqMinCon)
# 				elif x == 'Frequency (max)' and freqMaxCon != '':
# 					print(x+': '+str(freqMaxCon))
# 					fBody.append(freqMaxCon)
# 				elif indCon != []:
# 					for h in indCon:
# 						if 'Min Frequency (GHz)' == ky:
# 							fBody.append(is_float(y[h])*1000)
# 						elif 'Max Frequency (GHz)' == ky:
# 							fBody.append(is_float(y[h])*1000)
# 						else:
# 							fBody.append(y[h])
# 				else:
# 					fBody.append('')



# 		# c = 0
# 		# freqMinCon = ''
# 		# freqMaxCon = ''
# 		# for x in allowed:
# 		# 	num = 999
# 		# 	for i in range(0, len(y)):
# 		# 		if data[0][i] == x:
# 		# 			num = i

# 		# 	if num != 999:
# 		# 		if x == 'Operating Frequency (GHz)' and y[num] != '':
# 		# 			fr = re.findall(r'[\d\.\d]+', y[num])
# 		# 			if len(fr) == 2:
# 		# 				if 'ghz' in y[num].lower():
# 		# 					freqMinCon = is_float(fr[0])*1000
# 		# 					freqMaxCon = is_float(fr[1])*1000
# 		# 				else:
# 		# 					freqMinCon = is_float(fr[0])
# 		# 					freqMaxCon = is_float(fr[1])
# 		# 			else:
# 		# 				freqMinCon = is_float(fr[0])

# 		# 		if x != 'Operating Frequency (GHz)':
# 		# 			fBody.append(y[num])
# 		# 	# else:
# 		# 		# fBody.append('')

# 		# 	print(x)
# 		# 	if x == 'Min Frequency (MHz)' and freqMinCon != '':
# 		# 		fBody.append(freqMinCon)

# 		# 	if x == 'Max Frequency (MHz)' and freqMaxCon != '':
# 		# 		fBody.append(freqMaxCon)

# 		# 	c += 1

# 		# freqMinCon = ''
# 		# freqMaxCon = ''

# 		fData.append(fBody)
# 		fBody = []

# 	for x in fData:
# 		append_list_as_row(filepathHeader, x)
# 		# print(x)
# 		# print('~~')

# 	time.sleep(2)
# # except Exception as e:
# # 	err = 0
# # 	print(e)
# # 	time.sleep(5)
# print('Done.')

