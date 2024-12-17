from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
import re

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def num_there(s):
	return any(i.isdigit() for i in s)

def moreData(driver):
	scrl = 0
	while scrl == 0:
		try:
			element = driver.find_element(By.ID, "lz_loading_message")
			if 'none' in str(element.get_attribute("style")):
				scrl = 1
				driver.execute_script("arguments[0].scrollIntoView();", element)
				time.sleep(5)
				height = driver.execute_script("return document.body.scrollHeight")
				driver.execute_script(f"window.scrollTo(0,{height})")
				time.sleep(5)
				driver.execute_script(f"window.scrollTo(0,0)")
			else:
				driver.execute_script("arguments[0].scrollIntoView();", element)
				time.sleep(5)
				height = driver.execute_script("return document.body.scrollHeight")
				driver.execute_script(f"window.scrollTo(0,{height})")
				time.sleep(5)
				scrl = 0
		except Exception:
			scrl = 1
			driver.execute_script(f"window.scrollTo(0,0)")

links = {'adapters': '1',
		'Amplifiers': 'amplifier',
		'Attenuators': 'attenuator',
		'BiasTees': '1',
		'Cables': '3',
		'Couplers': '2',
		'dc_blocks': '1',
		'equalizers': 'equalizer',
		'RF-Filters': 'filter',
		'Mixers': 'mixer',
		'Multipliers': '3',
		'MatchingPads': '1',
		'Limiters': '1',
		'ModulatorsDemodulators': '1',
		'Oscillators': '1',
		'PhaseDetectors': '1',
		'PhaseShifters': '1',
		'pd_coax': '1',
		'Splitters': '2',
		'90_180_degree_hybrid': '2',
		'rf_chokes': '1',
		'Switches': '1',
		'Synthesizers': '1',
		'terminations': '1',
		'Transformers': '2'}
links = {'Mixers': 'mixer'}

header = {'1 dB Compression (dBm), Min.': 'P1dB (dBm)',
		'1 dB Compression (dBm), Typ.': 'P1dB (dBm)',
		'3XI/Q Harmonic Suppression (dBc), Min.': 'Harmonic Rejection',
		'3XI/Q Harmonic Suppression (dBc), Typ.': 'Harmonic Rejection',
		'5XI/Q Harmonic Suppression (dBc), Min.': 'Harmonic Rejection',
		'5XI/Q Harmonic Suppression (dBc), Typ.': 'Harmonic Rejection',
		'Amplitude Unbalance (dB) Max.': 'Amplitude Balance',
		'Amplitude Unbalance (dB) Typ.': 'Amplitude Balance',
		'Amplitude Unbalance (dB), Typ.': 'Amplitude Balance',
		'Attenuation Flatness (dB) Typ.': 'Amplitude Flatness',
		'Attenuation Flatness (dB), 100 - 1000 MHz': 'Amplitude Flatness',
		'Attenuation Flatness (dB), 1000 - 3000 MHz': 'Amplitude Flatness',
		'Attenuation Flatness (dB), DC - 100 MHz': 'Amplitude Flatness',
		'Attenuation(dB)Typ.': 'Attenuation (max)',
		'Carrier Rej. (dBc), Min.': 'Carrier Rejection',
		'Carrier Rej. (dBc), Typ.': 'Carrier Rejection',
		'Carrier Rejection (dBc), Max.': 'Carrier Rejection',
		'Carrier Rejection (dBc), Typ.': 'Carrier Rejection',
		'Case Style': 'Features',
		'Category': 'Features',
		'Common Port (MHz)': 'Frequency (max)',
		'Config.': 'Configuration',
		'Configuration': 'Configuration',
		'Conn. 1': 'Connector 1 Type',
		'Conn. 2': 'Connector 2 Type',
		'Connector 1Gender': 'Connector 1 gender',
		'Connector 1Mounting Type': 'Connector 1 Mount',
		'Connector 1Orientation': 'Connector 1 Polarity',
		'Connector 1Type': 'Connector 1 Type',
		'Connector 2Gender': 'Connector 2 gender',
		'Connector 2Mounting Type': 'Connector 2 Mount',
		'Connector 2Orientation': 'Connector 2 Polarity',
		'Connector 2Type': 'Connector 2 Type',
		'Connector Description': 'Features',
		'Connector Type': 'Connector 1 Type',
		'Connector, Typ.': 'Connector 1 Type',
		'ConnectorType': 'Connector 1 Type',
		'Construction': 'Features',
		'Control Freq. Hi (MHz)': 'Control Frequency (max)',
		'Control Freq. Low (MHz)': 'Control Frequency (min)',
		'Control Interface': 'Control Type',
		'Control Interfaces': 'Control Type',
		'Control Voltage (V)': 'Control Voltage (max)',
		'Conv. Loss (dB) (?)': 'Conversion Loss',
		'Conv. Loss (dB) Max.': 'Conversion Loss',
		'Conv. Loss (dB) Typ.': 'Conversion Loss',
		'Conv. Loss (dB), (?)': 'Conversion Loss',
		'Conv. Loss (dB), Max.': 'Conversion Loss',
		'Conv. Loss (dB), Typ.': 'Conversion Loss',
		'Conversion Loss (dB) Typ.': 'Conversion Loss',
		'Coupling(dB)': 'Coupling',
		'Crossover Isolation (dB)': 'Isolation',
		'Current (mA)': 'Current (max)',
		'Current Control (mA)': 'Control Current (min)',
		'DC Current (mA) Typ. @ +12V': 'Current (max)',
		'DC Current (mA) Typ. @ +24V': 'Current (max)',
		'DC Current (ma)': 'Current (max)',
		'DC Current (mA)': 'Current (max)',
		'DC Out Impedance (?)': 'Impedance',
		'DC port Isolation (dB) Typ.': 'Isolation',
		'DC Voltage (V)': 'Voltage (max)',
		'Description': 'Description',
		'Directivity (dB) Typ.': 'Directivity',
		'F High (GHz)': 'Frequency (max)',
		'F High (MHz)': 'Frequency (max)',
		'F Low (GHz)': 'Frequency (min)',
		'F Low (MHz)': 'Frequency (min)',
		'F. High (GHz)': 'Frequency (max)',
		'F. High (MHz)': 'Frequency (max)',
		'F. Low (GHz)': 'Frequency (min)',
		'F. Low (MHz)': 'Frequency (min)',
		'F1 Fundamental Suppression Below F[X] (dBc) Typ.': 'Fundamental Suppression (F)',
		'Feature': 'Features',
		'Filter Type': 'Features',
		'Freq. (GHz) High': 'Frequency (max)',
		'Freq. (GHz) Low': 'Frequency (min)',
		'Freq. (MHz) Max.': 'Frequency (max)',
		'Freq. (MHz) Min.': 'Frequency (min)',
		'Freq. Hi (GHz)': 'Frequency (max)',
		'Freq. Hi (MHz)': 'Frequency (max)',
		'Freq. High (GHz)': 'Frequency (max)',
		'Freq. High (MHz)': 'Frequency (max)',
		'Freq. Low (GHz)': 'Frequency (min)',
		'Freq. Low (MHz)': 'Frequency (min)',
		'Freq. Range High (MHz)': 'Frequency (max)',
		'Freq. Range In Hi (MHz)': 'Frequency (max)',
		'Freq. Range In Low (MHz)': 'Frequency (min)',
		'Freq. Range Low (MHz)': 'Frequency (min)',
		'FreqencyHigh (GHz)': 'Frequency (max)',
		'Frequency High (MHz)': 'Frequency (max)',
		'Frequency Low (MHz)': 'Frequency (min)',
		'Gain(dB) Typ.': 'Gain (max)',
		'Harmonic Suppression (dBc) 3xI/Q Min.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc) 3xI/Q Typ.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc) 5xI/Q Min.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc) 5xI/Q Typ.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc), 3XI/Q Max.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc), 3XI/Q Typ.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc), 5XI/Q Max.': 'Harmonic Rejection',
		'Harmonic Suppression (dBc), 5XI/Q Typ.': 'Harmonic Rejection',
		'Harmonics (dBc) Max.': 'Harmonic Level (max)',
		'Harmonics (dBc) Typ.': 'Harmonic Level (max)',
		'Harmonics (dBc), Max.': 'Harmonic Level (max)',
		'Harmonics (dBc), Typ.': 'Harmonic Level (max)',
		'I&Q Freq. Hi (MHz)': 'Frequency (max)',
		'I&Q Freq. Low (MHz)': 'Frequency (min)',
		'I&Q Freq. Range High (MHz)': 'Frequency (max)',
		'I&Q Freq. Range Low (MHz)': 'Frequency (min)',
		'IF Freq. High (MHz)': 'IF Frequency (max)',
		'IF Freq. Low (MHz)': 'IF Frequency (min)',
		'Impedance (?)': 'Impedance',
		'Impedance Ratio': 'Impedance Ratio',
		'In-Out Iso. (dB) Freq. Band Min.': 'Isolation',
		'In-Out Iso. (dB) Freq. Band Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Low Range Max.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Low Range Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Low Range, Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Mid Range, Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Mid-Range Max.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Mid-Range Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Upper Range Max.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Upper Range Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Upper Range, Typ.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Upper-Range Max.': 'Isolation',
		'In-Out Isolation (dB) at 0 mA, Upper-Range Typ.': 'Isolation',
		'In-Out Isolation (dB), Min.': 'Isolation',
		'In-Out Isolation (dB), Typ.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 10-100 Max.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 10-100 Min.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 10-100 Typ.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 100-1250 Min.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 100-1250 Typ.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 100-1500 Min.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 100-1500 Typ.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 1250-2500 Min.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 1250-2500 Typ.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 1500-3000 Min.': 'Isolation',
		'In-Out Isolation Frequency Band (dB) 1500-3000 Typ.': 'Isolation',
		'Inductance (µH) @ 0 mA': 'Inductance',
		'Inductance (µH) @ 100 mA': 'Inductance',
		'Inductance (µH) @ 200 mA': 'Inductance',
		'Input Current (mA) Max.': 'Current (max)',
		'Input Freq. High (MHz)': 'Input Frequency (max)',
		'Input Freq. Low (MHz)': 'Input Frequency (min)',
		'Input IP3 (dBm) Typ.': 'IP3',
		'Input P1dB (dBm) Typ.': 'P1dB (dBm)',
		'Input Power (dBm) at 1 dB Compr., at ±20 mA': 'Input Power Level (max)',
		'Input Power Max.': 'Input Power Level (max)',
		'Input Power Min.': 'Input Power Level (min)',
		'Input Power, Max.': 'Input Power Level (max)',
		'Input Power(W)Max': 'Input Power Level (max)',
		'Input Pwr @ 1 dB Compr. at ±20 mA, Typ.': 'Input Power Level (max)',
		'Input VSWR (:1) Typ.': 'VSWR (single value or input/output)',
		'Insertion Loss (dB) Above Theoretical, Typ.': 'Insertion loss (max)',
		'Insertion Loss (dB) Max.': 'Insertion loss (max)',
		'Insertion Loss (dB) Typ.': 'Insertion loss (max)',
		'Insertion Loss (dB), Low-Band, Max.': 'Insertion loss (max)',
		'Insertion Loss (dB), Low-Band, Typ.': 'Insertion loss (max)',
		'Insertion Loss (dB), Max.': 'Insertion loss (max)',
		'Insertion Loss (dB), Typ.': 'Insertion loss (max)',
		'Insertion Loss (dB), Typ': 'Insertion loss (max)',
		'Insertion Loss (dB), Upper-Band, Max.': 'Insertion loss (max)',
		'Insertion Loss (dB), Upper-Band, Typ.': 'Insertion loss (max)',
		'Insertion Loss (dB)': 'Insertion loss (max)',
		'Insertion Loss F1(dB)Typ': 'Lower Passband Insertion Loss',
		'Insertion Loss F2(dB)Typ': 'Lower Passband Insertion Loss',
		'Insertion Loss Low-Band Max. (dB)': 'Insertion loss (max)',
		'Insertion Loss Low-Band Typ. (dB)': 'Insertion loss (max)',
		'Insertion Loss Upper-Band Max. (dB)': 'Insertion loss (max)',
		'Insertion Loss Upper-Band Typ. (dB)': 'Insertion loss (max)',
		'Interface': 'Interface',
		'Isolation (dB), Typ.': 'Isolation',
		'Isolation (dB), Typ': 'Isolation',
		'Length (ft)': 'Length',
		'Linear Range Insertion Loss (dB) Typ.': 'Insertion loss (max)',
		'LO Freq. High (MHz)': 'LO Frequency (max)',
		'LO Freq. Low (MHz)': 'LO Frequency (min)',
		'LO Level (dBm)': 'LO Power (max)',
		'LO-IF Isolation (dB) Typ.': 'LO/IF Isolation',
		'LO-RF Isolation (dB) Typ.': 'LO/RF Isolation',
		'LTCC Construction': 'Features',
		'Mainline Loss(dB) Typ.': 'Insertion loss (max)',
		'Max Input Power (W)': 'Input Power Level (max)',
		'Mid-Band Insertion Loss (dB) at ±20 mA, Max.': 'Insertion loss (max)',
		'Mid-Band Insertion Loss (dB) at ±20 mA, Typ.': 'Insertion loss (max)',
		'Multiply Factor [X]': 'Multiplication Factor',
		'NF(dB) Typ.': 'Noise Figure',
		'No. of Ways': 'Ports',
		'Nom. Attenuation (dB)': 'Attenuation (max)',
		'Number of Switches': 'Number of Switches',
		'OIP3 (dBm) Typ.': 'IP3',
		'Option': 'Features',
		'Output Freq. High (MHz)': 'Output Frequency (max)',
		'Output Freq. Low (MHz)': 'Output Frequency (min)',
		'Output Port Freq. (MHz)': 'Frequency (max)',
		'Output Power Limit (dBm) Typ.': 'Output Power',
		'Output VSWR (:1) Typ.': 'VSWR (single value or input/output)',
		'P1dB(dBm) Typ.': 'P1dB (dBm)',
		'Passband (MHz)': 'Passband Frequency (max)',
		'Passband F1 (MHz)': 'Passband Frequency (min)',
		'Passband F1 (MHz)': 'Passband Frequency (min)',
		'Passband F2  (MHz)': 'Passband Frequency (max)',
		'Passband F2 (MHz)': 'Passband Frequency (max)',
		'Passband IL (dB)': 'Passband Insertion Loss',
		'PFD. Spurious (dBc)': 'Spur Level',
		'Phase Noise (dBc/Hz) @ 1 00kHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 1 0kHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 1 kHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 1 MHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 10 kHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 100 Hz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 100 kHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 1000 Hz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 1000 kHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Noise (dBc/Hz) @ 1MHz Offset, Typ.': 'Phase Noise (max)',
		'Phase Range (deg.) Min.': 'Phase Range',
		'Phase Unbalance (deg.) Max.': 'Phase Balance',
		'Phase Unbalance (deg.) Typ.': 'Phase Balance',
		'Phase Unbalance (deg), Typ.': 'Phase Balance',
		'PLL Power Supply Voltage (V), Nom.': 'Voltage (max)',
		'PLL Power Supply, Current (mA), Max.': 'Current (max)',
		'Power Input (W) as Splitter, Max.': 'Input Power Level (max)',
		'Power InputMax.(W)': 'Input Power Level (max)',
		'Power Output (dBm) Typ., Aux.': 'Output Power',
		'Power Output (dBm) Typ., Max.': 'Output Power',
		'Power Output (dBm) Typ.': 'Output Power',
		'Power Output (dBm), Typ.': 'Output Power',
		'Power Rating (W), Max.': 'Input Power Level (max)',
		'Pulling (MHz) pk - pk @  12 dBr, Typ.': 'Pulling',
		'Pulse Response Fall Time (nsec), Typ.': 'Fall Time',
		'Pulse Response Rise Time (nsec), Typ.': 'Rise Time',
		'Pushing (MHz/V), Typ.': 'Pushing',
		'Ref Freq. (MHz)': 'Reference Frequency (max)',
		'Ref. Spurious (dBc)': 'Spur Level',
		'Rejection (dB)': 'Rejection',
		'Rejection @ F3  (dB)': 'Rejection',
		'Rejection @ F3 (dB)': 'Rejection',
		'Rejection @ F4  (dB)': 'Rejection',
		'Rejection @ F4 (dB)': 'Rejection',
		'Return Loss (dB) Typ.': 'Return Loss',
		'Return Loss (dB), Typ. @ 1 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 12 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 18 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 2 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 20 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 4 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 40 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 50 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 6 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 65 GHz': 'Return Loss',
		'Return Loss (dB), Typ. @ 8 GHz': 'Return Loss',
		'Return Loss (dB)': 'Return Loss',
		'RF Freq. Hi (MHz)': 'Frequency (max)',
		'RF Freq. High (MHz)': 'RF Frequency (max)',
		'RF Freq. Low (MHz)': 'RF Frequency (min)',
		'RF Input Power (dBm) Max.': 'Input Power Level (max)',
		'RF Input Power (dBm) Min.': 'Input Power Level (min)',
		'RF Power (W) Max.': 'Input Power Level (max)',
		'RF Power (W), Max.': 'Input Power Level (max)',
		'RF Power In (dBm)': 'Input Power Level (max)',
		'RF/LO Freq. Hi (MHz)': 'LO/RF Frequency (max)',
		'RF/LO Freq. Low (MHz)': 'LO/RF Frequency (min)',
		'RF/LO Freq. Range Hi (MHz)': 'LO/RF Frequency (max)',
		'RF/LO Freq. Range Low (MHz)': 'LO/RF Frequency (min)',
		'RF1 - RF2 Isolation (dB) Min.': 'Isolation',
		'Scale Factor (mV/deg.)': 'Scale Factor',
		'Settling Time (mSec), Typ.': 'Settling Time',
		'Sideband Rej. (dBc), Min.': 'Sideband Rejection',
		'Sideband Rej. (dBc), Typ.': 'Sideband Rejection',
		'Sideband Rejection (dBc) Min.': 'Sideband Rejection',
		'Sideband Rejection (dBc) Typ.': 'Sideband Rejection',
		'Stopband F3  (MHz)': 'Stopband Frequency (min)',
		'Stopband F3 (MHz)': 'Stopband Frequency (min)',
		'Stopband F4  (MHz)': 'Stopband Frequency (max)',
		'Stopband F4 (MHz)': 'Stopband Frequency (max)',
		'Supply Current (mA)': 'Current (max)',
		'Supply Voltage (V), Typ': 'Voltage (max)',
		'Supply Voltage (V)': 'Voltage (max)',
		'Switch Type': 'Switch Type',
		'Technology': 'Features',
		'Termination': 'Termination Type',
		'Total Range Insertion Loss (dB) at ±20 mA, Max.': 'Insertion loss (max)',
		'Total Range Insertion Loss (dB) at ±20 mA, Typ.': 'Insertion loss (max)',
		'Total-Band Insertion Loss (dB) at ±20 mA, Max.': 'Insertion loss (max)',
		'Total-Band Insertion Loss (dB) at ±20 mA, Typ.': 'Insertion loss (max)',
		'Tune Voltage (V) Max.': 'Tuning Voltage (max)',
		'Tune Voltage (V) Min.': 'Tuning Voltage (min)',
		'Tuning Sensitivity (MHz/V) Typ.': 'Sensitivity',
		'VCO Power Supply, Current (mA), Max.': 'Current (max)',
		'VCO Power Supply, Voltage (V), Nom.': 'Voltage (max)',
		'Voltage (V)': 'Voltage (max)',
		'VSWR (:1) Typ.': 'VSWR (single value or input/output)',
		'VSWR (:1), 100 - 1000 MHz': 'VSWR (single value or input/output)',
		'VSWR (:1), 1000 - 3000 MHz': 'VSWR (single value or input/output)',
		'VSWR (:1), DC - 100 MHz': 'VSWR (single value or input/output)',
		'VSWR (:1), Max.': 'VSWR (single value or input/output)',
		'VSWR (:1), Typ.': 'VSWR (single value or input/output)',
		'VSWR (:1), Typ': 'VSWR (single value or input/output)',
		'VSWR (:1)Typ.': 'VSWR (single value or input/output)',
		'VSWR(:1) Typ.': 'VSWR (single value or input/output)'}

cats = {'DC to 67 GHz': [1, 2],
		'Low Noise Amplifiers\n(NF < 3 dB)': [2, 50],
		'High Power Amplifiers\n(>2W)': [2, 67],
		'Linear Amplifiers\n(IP3 > +40 dBm)': [2, 4],
		'CATV Amplifiers (75Ω)': [2, 4],
		'Gain Blocks': [2, 4],
		'Variable Gain\nAmplifiers': [2, 90],
		'Dual Matched\nAmplifiers': [2, 4],
		'Pulse Amplifiers': [2, 4],
		'Fixed Attenuator': [4, 8],
		'Digital Step Attenuator': [4, 26],
		'Voltage Variable Attenuator': [4, 93],
		'Programmable Attenuator': [4, 8],
		'Impedance Matching Pads, Surface Mount, 50 to 75 ohm, DC to 3000 MHz.': [4, 48],
		'Impedance Matching Pads, Coaxial, 50 to 75 Ohm, DC to 3000 MHz': [4, 48],
		'Attenuators / Switches / Bi-Phase, Surface Mount, 2 MHz to 1 GHz': [4, 8],
		'Attenuators / Switches / Bi-Phase Modulators, Coaxial, 1 MHz to 2 GHz': [4, 8],
		'Attenuator / Switches / Bi-Phase, Plug-In, 1 MHz to 2 GHz': [4, 8],
		'Attenuators / Switches / Bi-Phase, Surface Mount, 2 MHz to 1 GHz': [4, 8],
		'Attenuators/Switches/Bi-Phase, Coaxial, 1 MHz to 2 GHz': [4, 8],
		'Attenuator / Switches / Bi-Phase, Plug-In, 1 MHz to 2 GHz': [4, 8],
		'RF Transformers and Baluns': [5, 9],
		'Surface Mount, Wideband, 100 kHz to 40000 MHz': [6, 12],
		'Coaxial, Wideband, 100 kHz to 28000 MHz': [6, 12],
		'Coaxial, Diplexer, 10 MHz to 5900 MHz': [6, 12],
		'Plug-In, Wideband, 100 kHz to 3000 MHz': [6, 12],
		'MMIC, Bias-Tee Die, Wideband,1500MHz to 40000MHz': [6, 12],
		'RF Cables': [7, 13],
		'RF Couplers': [11, 20],
		'Coaxial DC Blocks, Wide Band, 0.1 MHz to 65 GHz': [13, 22],
		'Surface Mount, Diplexers': [16, 28],
		'Fixed Slope': [16, 35],
		'Voltage Variable': [16, 35],
		'Band Pass': [16, 10],
		'Band Pass + Balun': [16, 10],
		'Dual Passband': [16, 28],
		'Low Pass': [16, 51],
		'High Pass': [16, 46],
		'Band Stop': [16, 59],
		'Diplexer': [16, 28],
		'Triplexer': [16, 81],
		'Low Pass Flat Time Delay': [16, 51],
		'Low Pass Dual/Differential': [16, 51],
		'All Pass/Thru Line': [16, 120],
		'RF Chokes, Very Wideband, 5 to 10000 MHz, Up to 15 ADC': [20, 73],
		'Terminations, Coaxial, DC to 65 GHz': [22, 18],
		'Active Mixer': [23, 56],
		'Double Balanced Mixer': [23, 56],
		'Triple Balanced Mixer': [23, 56],
		'High Reliability': [23, 56],
		'Up Converter': [23, 86],
		'I & Q Modulators, Surface Mount, 52 MHz to 2000 MHz': [23, 56],
		'I & Q Demodulators, Surface Mount, 104 MHz to 1880 MHz': [23, 56],
		'I & Q Modulators': [23, 56],
		'I & Q Demodulators': [23, 56],
		'Frequency Multipliers': [25, 58],
		'Voltage Controlled Oscillators, Surface Mount, Linear Tuning, Wideband, 12.5 to 5400 MHz': [26, 94],
		'Voltage Controlled Oscillators, Surface Mount, 5V Tuning for PLLs, 24 to 6840 MHz': [26, 94],
		'Voltage Controlled Oscillators, Dual Output, 25 to 1025 MHz': [26, 94],
		'Voltage Controlled Oscillators, Plug-In, Linear Tuning, Wideband, 15 to 2120 MHz': [26, 94],
		'Phase Detectors, Surface Mount, High Output (1000 mV DC), 1 to 650 MHz': [28, 64],
		'Phase Detectors, Coaxial, High Output (1000 mV DC), 1 to 100 MHz': [28, 64],
		'Phase Detectors, Plug-In, High Output (1000 mV DC), 1 to 400 MHz': [28, 64],
		'Phase Shifters, Surface Mount, 180 Degree Voltage Variable, 1.8 to 2484 MHz': [29, 5],
		'Phase Shifters, Surface Mount, 360 Degree Voltage Variable, 10 to 1500 MHz': [29, 5],
		'Phase Shifters, Coaxial, 360 Degree Voltage Variable': [29, 5],
		'Power Detectors, Coaxial, -60 to +20 dBm, 10 to 43500 MHz': [31, 68],
		'RF Power Splitters/Dividers/Combiners': [32, 69],
		'90-Degree and 180-DegreeHybrid Splitter/Combiners': [32, 69],
		'Limiters, Surface Mount, 5 to 37 dBm, 0.2 MHz to 8200 MHz': [33, 70],
		'Limiters, Coaxial, 5 to 33 dBm, 10 MHz to 8200 MHz': [33, 70],
		'Limiters, Plug-In, 3 to 20 dBm, 100 kHz to 900 MHz': [33, 70],
		'Switches, Surface-Mount, SPST/SPDT/SP4T/SP6T, 50 Ohms, DC to 6.0 GHz': [36, 76],
		'Switches, Surface Mount, SPDT/SP6T, 75 Ohms, DC to 3.0 GHz': [36, 76],
		'Switches, Surface Mount, Transfer, Low Video Leakage, DC to 2 GHz': [36, 76],
		'Switches, Coaxial, SPDT/SP4T with/without TTL Drivers, DC to 6 GHz': [36, 76],
		'Switches, Coaxial, SPST/SPDT with/without TTL Drivers, High Isolation, DC to 6 GHz': [36, 76],
		'Mechanical Switches, SPDT/SP4T/SP6T/SP8T Transfer, DC to 18 GHz, Coaxial': [36, 76],
		'Switches, Coaxial, PIN Diode, SPDT/SP4T with TTL Drivers, 10 to 3000 MHz': [36, 76],
		'Switches, Coaxial, PIN Diode, SPST/SPDT, 10 to 2500 MHz': [36, 76],
		'Mechanical Switches  |  USB / Ethernet  |  DC to 50 GHz': [36, 76],
		'Solid State Absorptive Switches  |  USB / SPI / I²C / TTL |  DC to 43.5 GHz': [36, 76],
		'Plug-In, PIN Diode, SPDT/SP4T with TTL Drivers, 10 to 3000 MHz': [36, 76],
		'Switches, Plug-In, PIN Diode, SPST/SPDT, 10 to 2500 MHz': [36, 76],
		'Switches, Die, SPDT 50 Ohms, DC to 4.5 GHz': [36, 76],
		'Synthesizer, Surface Mount, Tunable Narrow Bandwidth, 668 to 3580 MHz': [37, 78],
		'RF Transistors': [38, 74]}

manufacturer = 59

# for loop in range(5):
#########
username = getpass.getuser()
if not os.path.exists('/Users/'+username+'/Work/RFBackDoor'):
	os.makedirs('/Users/'+username+'/Work/RFBackDoor')

now = datetime.now()
dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
filepathHeader = '/Users/'+username+'/Work/RFBackDoor/Mini_Circuit_'+str(dt_string)+'.csv'
fHeader = ['Manufacturer', 'Category', 'Subcategory', 'Part Number', 'Image', 'PDF', 'Product Link']

for x in header:
	if header[x] not in fHeader:
		fHeader.append(header[x])

append_list_as_row(filepathHeader, fHeader)

#########
options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--log-level=3")
options.add_argument("enable-automation")
options.add_argument("--no-proxy-server")
options.add_argument("--disk-cache-size=0")
options.add_argument("--aggressive-cache-discard")
options.add_argument("--disable-cache")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-offline-load-stale-cache")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#########

for link in links:
	err = 0
	while err == 0:
		try:
			driver.get('https://www.minicircuits.com/WebStore/'+link+'.html')
			driver.implicitly_wait(5)

			print('----- '+link+': '+links[link])

			try:
				driver.find_element(By.ID, 'hs-eu-confirmation-button').click()
			except Exception:
				pass

			moreData(driver)
		except Exception as e:
			err = 0
			continue

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		if links[link] == '1':
			try:
				pagehtml = driver.page_source
				soup = bs4.BeautifulSoup(pagehtml, "html.parser")

				final = []
				tblDivs = soup.find_all('div', {'class': 'mark_tables'})

				for tblDiv in tblDivs:
					try:
						moreData(driver)
						h = []
						b = []
						sub = str(tblDiv.find('h2', {'class': 'model_name_title'}).text)
						print('sub: '+sub)
						tbl = tblDiv.find_all('table')
						for y in tbl:
							if 'fixed' not in str(y):
								thead = y.find('thead').find_all('th')
								for th in thead:
									h.append(th.text)

								tbody = y.find('tbody').find_all('tr', {'name': 'data_row'})
								print(len(tbody))
								for trb in tbody:
									tdata = trb.find_all('td')
									bTemp = []
									bTemp.append(manufacturer)
									bTemp.append(cats[sub][0])
									bTemp.append(cats[sub][1])
									mn = ''

									op = tdata[0].find('output')
									if str(op) == 'None':
										mn = tdata[0].text.strip()
									else:
										mn = op.text

									try:
										img = tdata[h.index('Case Style')].find('output').text.strip()
									except Exception:
										img = ''

									l = tdata[0].find('a')['href']

									bTemp.append(mn)
									if img != '':
										bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
									else:
										bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
									bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
									bTemp.append('https://www.minicircuits.com/WebStore/'+l)

									for y in fHeader[7:]:
										chk = ''
										for i in thead:
											try:
												if y == header[i.text]:
													chk = i.text
											except Exception:
												pass
										if chk != '':
											nth = []
											for n in thead:
												nth.append(n.text)
											ind = nth.index(chk)
											op = tdata[ind].find('output')
											if 'ghz' in chk.lower():
												val = ''
												if str(op) == 'None':
													val = tdata[ind].text.strip()
												else:
													val = op.text

												if num_there(val) == True:
													a = float(re.sub('[a-zA-Z]+', '', val))*1000
													bTemp.append(str(a))
												else:
													bTemp.append(val)
											else:
												if str(op) == 'None':
													bTemp.append(tdata[ind].text.strip())
												else:
													bTemp.append(op.text)
										else:
											bTemp.append('')
									b.append(bTemp)

								final.append([link, sub, h, b])
						err = 1
					except Exception as e:
						print('NAG ERROR OY: '+str(e))
						err = 0
						continue
			except Exception as e:
				print('NAG ERROR OY 1: '+str(e))
				err = 0

			print('- result -')
			if err == 1:
				dups = []
				for x in final:
					# append_list_as_row(filepathHeader, ['>>>', x[0], x[1]])
					# append_list_as_row(filepathHeader, x[2])
					cout = 0
					for i in x[3]:
						if i not in dups:
							dups.append(i)
							append_list_as_row(filepathHeader, i)
							cout += 1
					print(x[1])
					print(cout)
		elif links[link] == '2':
			h = []
			b = []
			try:
				moreData(driver)

				pagehtml = driver.page_source
				soup = bs4.BeautifulSoup(pagehtml, "html.parser")

				sub = soup.find('section', {'class': 'product_top'}).find('h1').text
				print('sub: '+sub)

				tbl = soup.find('tbody', {'id': 'table1'})
				thead = tbl.parent.find('tr', {'class': 'bg_color'}).find_all('th')
				for x in thead:
					h.append(x.text)

				tbody = tbl.find_all('tr', {'name': 'data_row'})
				print(len(tbody))
				for trb in tbody:
					tdata = trb.find_all('td')
					bTemp = []
					bTemp.append(manufacturer)
					bTemp.append(cats[sub][0])
					bTemp.append(cats[sub][1])
					mn = ''

					op = tdata[0].find('output')
					if str(op) == 'None':
						mn = tdata[0].text.strip()
					else:
						mn = op.text

					img = tdata[h.index('Case Style')].find('output').text.strip()
					l = tdata[0].find('a')['href']

					bTemp.append(mn)
					if img != '':
						bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
					else:
						bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
					bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
					bTemp.append('https://www.minicircuits.com/WebStore/'+l)

					for y in fHeader[7:]:
						chk = ''
						for i in thead:
							try:
								if y == header[i.text]:
									chk = i.text
							except Exception:
								pass
						if chk != '':
							nth = []
							for n in thead:
								nth.append(n.text)
							ind = nth.index(chk)
							op = tdata[ind].find('output')
							if 'ghz' in chk.lower():
								val = ''
								if str(op) == 'None':
									val = tdata[ind].text.strip()
								else:
									val = op.text

								if num_there(val) == True:
									a = float(re.sub('[a-zA-Z]+', '', val))*1000
									bTemp.append(str(a))
								else:
									bTemp.append(val)
							else:
								if str(op) == 'None':
									bTemp.append(tdata[ind].text.strip())
								else:
									bTemp.append(op.text)
						else:
							bTemp.append('')
					b.append(bTemp)

				err = 1
			except Exception as e:
				b = []
				h = []
				print('NAG ERROR OY: '+str(e))
				err = 0

			if err == 1:
				print('- result -')
				dups = []
				# append_list_as_row(filepathHeader, ['>>>', link, sub])
				# append_list_as_row(filepathHeader, h)
				for i in b:
					if i not in dups:
						dups.append(i)
						append_list_as_row(filepathHeader, i)
				print(sub)
				print(len(dups))
		elif links[link] == '3':
			h = []
			b = []
			try:
				moreData(driver)
				pagehtml = driver.page_source
				soup = bs4.BeautifulSoup(pagehtml, "html.parser")

				sub = soup.find('section', {'class': 'product_top'}).find('h1').text
				print('sub: '+sub)

				tbl = soup.find('div', {'class': 'container_main'}).find_all('table')[1]
				thead = tbl.find('tr', {'class': 'bg_color'}).find_all('th')
				for x in thead:
					h.append(x.text)

				tbody = tbl.find('tbody').find_all('tr')
				print(len(tbody))
				for trb in tbody:
					tdata = trb.find_all('td')
					bTemp = []
					bTemp.append(manufacturer)
					bTemp.append(cats[sub][0])
					bTemp.append(cats[sub][1])
					mn = ''

					op = tdata[0].find('output')
					if str(op) == 'None':
						mn = tdata[0].text.strip()
					else:
						mn = op.text

					img = tdata[h.index('Case Style')].find('output').text.strip()
					l = tdata[0].find('a')['href']

					bTemp.append(mn)
					if img != '':
						bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
					else:
						bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
					bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
					bTemp.append('https://www.minicircuits.com/WebStore/'+l)

					for y in fHeader[7:]:
						chk = ''
						for i in thead:
							try:
								if y == header[i.text]:
									chk = i.text
							except Exception:
								pass
						if chk != '':
							nth = []
							for n in thead:
								nth.append(n.text)
							ind = nth.index(chk)
							op = tdata[ind].find('output')
							if 'ghz' in chk.lower():
								if str(op) == 'None':
									val = tdata[ind].text.strip()
								else:
									val = op.text

								if num_there(val) == True:
									a = float(re.sub('[a-zA-Z]+', '', val))*1000
									bTemp.append(str(a))
								else:
									bTemp.append(val)
							else:
								if str(op) == 'None':
									bTemp.append(tdata[ind].text.strip())
								else:
									bTemp.append(op.text)
						else:
							bTemp.append('')
					b.append(bTemp)

				print('- result -')
				dups = []
				# append_list_as_row(filepathHeader, ['>>>', link, sub])
				# append_list_as_row(filepathHeader, h)
				for i in b:
					if i not in dups:
						dups.append(i)
						append_list_as_row(filepathHeader, i)
				print(sub)
				print(len(dups))

				err = 1
			except Exception as e:
				print('NAG ERROR OY: '+str(e))
				err = 0
		elif links[link] == 'amplifier':
			final = []
			rf = 0
			try:
				for i in range(9):
					h = []
					b = []
					sub = ''

					# a = driver.find_elements(By.CLASS_NAME, "inner_content_dual")[1]
					# a.find_element(By.NAME, "Amplifiers.categorys."+str(i)+".selected").click()
					# time.sleep(10)

					a = driver.find_elements(By.CLASS_NAME, "inner_content_dual")[1]
					if a.find_element(By.NAME, "Amplifiers.categorys."+str(i)+".selected").is_selected() == False:
						a.find_element(By.NAME, "Amplifiers.categorys."+str(i)+".selected").click()
					time.sleep(5)
					a = driver.find_elements(By.CLASS_NAME, "inner_content_dual")[1]
					if a.find_element(By.NAME, "Amplifiers.categorys."+str(i)+".selected").is_selected() == True:
						time.sleep(5)


					catg = driver.find_elements(By.XPATH, "//div[@class='inner_content_dual']")[1]
					div = catg.find_elements(By.TAG_NAME, "div")
					for x in div:
						if str("Amplifiers.categorys."+str(i)+".selected") in str(x.get_attribute("outerHTML")):
							sub = x.find_elements(By.TAG_NAME, "span")[1].text.strip()
					print('sub: '+sub)

					pagehtml = driver.page_source
					soup = bs4.BeautifulSoup(pagehtml, "html.parser")

					tbl = soup.find('tbody', {'id': 'table1'})
					thead = tbl.parent.find('tr', {'class': 'bg_color'}).find_all('th')
					for x in thead:
						h.append(x.text)

					tbody = tbl.find_all('tr', {'class': 'data_rows'})
					print(len(tbody))

					if len(tbody) >= 600:
						print('6000000000000000000000000000000000000000000000000')
						rf = 1
						break
					else:
						for trb in tbody:
							tdata = trb.find_all('td')
							bTemp = []
							bTemp.append(manufacturer)
							bTemp.append(cats[sub][0])
							bTemp.append(cats[sub][1])
							mn = ''

							op = tdata[0].find('output')
							if str(op) == 'None':
								mn = tdata[0].text.strip()
							else:
								mn = op.text

							img = tdata[h.index('Case Style')].find('output').text.strip()
							l = tdata[0].find('a')['href']

							bTemp.append(mn)
							if img != '':
								bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
							else:
								bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
							bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
							bTemp.append('https://www.minicircuits.com/WebStore/'+l)

							for y in fHeader[7:]:
								chk = ''
								for th in thead:
									try:
										if y == header[th.text]:
											chk = th.text
									except Exception:
										pass
								if chk != '':
									nth = []
									for n in thead:
										nth.append(n.text)
									ind = nth.index(chk)
									op = tdata[ind].find('output')
									if 'ghz' in chk.lower():
										val = ''
										if str(op) == 'None':
											val = tdata[ind].text.strip()
										else:
											val = op.text

										if num_there(val) == True:
											a = float(re.sub('[a-zA-Z]+', '', val))*1000
											bTemp.append(str(a))
										else:
											bTemp.append(val)
									else:
										if str(op) == 'None':
											bTemp.append(tdata[ind].text.strip())
										else:
											bTemp.append(op.text)
								else:
									bTemp.append('')
							b.append(bTemp)

						# a = driver.find_elements(By.CLASS_NAME, "inner_content_dual")[1]
						# a.find_element(By.NAME, "Amplifiers.categorys."+str(i)+".selected").click()
						# time.sleep(10)

						for u in range(9):
							ch = 0 
							while ch == 0:
								a = driver.find_elements(By.CLASS_NAME, "inner_content_dual")[1]
								if a.find_element(By.NAME, "Amplifiers.categorys."+str(u)+".selected").is_selected() == True:
									a.find_element(By.NAME, "Amplifiers.categorys."+str(u)+".selected").click()
									time.sleep(10)
								a = driver.find_elements(By.CLASS_NAME, "inner_content_dual")[1]
								if a.find_element(By.NAME, "Amplifiers.categorys."+str(u)+".selected").is_selected() == False:
									ch = 1
								else:
									ch = 0

						final.append([link, sub, h, b])

				if rf == 1:
					err = 0
				else:
					err = 1
			except Exception as e:
				print('NAG ERROR OY: '+str(e))
				err = 0

			print('- result -')
			if err == 1:
				dups = []
				for x in final:
					# append_list_as_row(filepathHeader, ['>>>', x[0], x[1]])
					# append_list_as_row(filepathHeader, x[2])
					cout = 0
					for i in x[3]:
						if i not in dups:
							dups.append(i)
							append_list_as_row(filepathHeader, i)
							cout += 1
					print(x[1])
					print(cout)
		elif links[link] == 'equalizer':
			try:
				final = []
				for i in range(2):
					cat = {1: 'Fixed Slope', 0: 'Voltage Variable'}
					h = []
					b = []

					moreData(driver)

					sub = str(cat[i])
					print('sub: '+sub)

					pagehtml = driver.page_source
					soup = bs4.BeautifulSoup(pagehtml, "html.parser")

					tbl = soup.find_all('div', {'class': 'container_main'})[i].find_all('table')[1]
					thead = tbl.find('tr', {'class': 'bg_color'}).find_all('th')
					for x in thead:
						h.append(x.text)

					tbody = tbl.find('tbody').find_all('tr')
					print(len(tbody))
					for trb in tbody:
						tdata = trb.find_all('td')
						bTemp = []
						bTemp.append(manufacturer)
						bTemp.append(cats[sub][0])
						bTemp.append(cats[sub][1])
						mn = ''

						op = tdata[0].find('output')
						if str(op) == 'None':
							mn = tdata[0].text.strip()
						else:
							mn = op.text

						img = tdata[h.index('Case Style')].find('output').text.strip()
						l = tdata[0].find('a')['href']

						bTemp.append(mn)
						if img != '':
							bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
						else:
							bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
						bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
						bTemp.append('https://www.minicircuits.com/WebStore/'+l)

						for y in fHeader[7:]:
							chk = ''
							for th in thead:
								try:
									if y == header[th.text]:
										chk = th.text
								except Exception:
									pass
							if chk != '':
								nth = []
								for n in thead:
									nth.append(n.text)
								ind = nth.index(chk)
								op = tdata[ind].find('output')
								if 'ghz' in chk.lower():
									val = ''
									if str(op) == 'None':
										val = tdata[ind].text.strip()
									else:
										val = op.text

									if num_there(val) == True:
										a = float(re.sub('[a-zA-Z]+', '', val))*1000
										bTemp.append(str(a))
									else:
										bTemp.append(val)
								else:
									if str(op) == 'None':
										bTemp.append(tdata[ind].text.strip())
									else:
										bTemp.append(op.text)
							else:
								bTemp.append('')
						b.append(bTemp)

					final.append([link, sub, h, b])
				err = 1
			except Exception as e:
				print('NAG ERROR OY: '+str(e))
				err = 0

			print('- result -')
			if err == 1:
				dups = []
				for x in final:
					# append_list_as_row(filepathHeader, ['>>>', x[0], x[1]])
					# append_list_as_row(filepathHeader, x[2])
					cout = 0
					for i in x[3]:
						if i not in dups:
							dups.append(i)
							append_list_as_row(filepathHeader, i)
							cout += 1
					print(x[1])
					print(cout)
		elif links[link] == 'mixer':
			try:
				final = []
				for i in range(5):
					h = []
					b = []
					sub = ''
					time.sleep(5)

					ch = 0 
					while ch == 0:
						a = driver.find_elements(By.CLASS_NAME, "mixers_header_top")[1]
						if a.find_element(By.NAME, "Mixers.subcategorys."+str(i)+".selected").is_selected() == False:
							time.sleep(3)
							a.find_element(By.NAME, "Mixers.subcategorys."+str(i)+".selected").click()
						time.sleep(10)
						a = driver.find_elements(By.CLASS_NAME, "mixers_header_top")[1]
						if a.find_element(By.NAME, "Mixers.subcategorys."+str(i)+".selected").is_selected() == True:
							ch = 1
						else:
							ch = 0

					moreData(driver)

					catg = driver.find_elements(By.CLASS_NAME, "mixers_header_top")[1]
					div = catg.find_elements(By.TAG_NAME, "div")
					for x in div:
						if str("Mixers.subcategorys."+str(i)+".selected") in str(x.get_attribute("outerHTML")):
							sub = x.find_elements(By.TAG_NAME, "span")[1].text.strip()
					print('sub: '+sub)

					pagehtml = driver.page_source
					soup = bs4.BeautifulSoup(pagehtml, "html.parser")

					tbl = soup.find('tbody', {'id': 'table1'})
					thead = tbl.parent.find('tr', {'class': 'bg_color'}).find_all('th')
					for x in thead:
						h.append(x.text)

					tbody = tbl.find_all('tr', {'class': 'data_rows'})
					print(len(tbody))
					for trb in tbody:
						tdata = trb.find_all('td')
						bTemp = []
						bTemp.append(manufacturer)
						bTemp.append(cats[sub][0])
						bTemp.append(cats[sub][1])
						mn = ''

						op = tdata[0].find('output')
						if str(op) == 'None':
							mn = tdata[0].text.strip()
						else:
							mn = op.text

						img = tdata[h.index('Case Style')].find('output').text.strip()
						l = tdata[0].find('a')['href']

						bTemp.append(mn)
						if img != '':
							bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
						else:
							bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
						bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
						bTemp.append('https://www.minicircuits.com/WebStore/'+l)

						for y in fHeader[7:]:
							chk = ''
							for th in thead:
								try:
									if y == header[th.text]:
										chk = th.text
								except Exception:
									pass
							if chk != '':
								nth = []
								for n in thead:
									nth.append(n.text)
								ind = nth.index(chk)
								op = tdata[ind].find('output')
								if 'ghz' in chk.lower():
									val = ''
									if str(op) == 'None':
										val = tdata[ind].text.strip()
									else:
										val = op.text

									if num_there(val) == True:
										a = float(re.sub('[a-zA-Z]+', '', val))*1000
										bTemp.append(str(a))
									else:
										bTemp.append(val)
								else:
									if str(op) == 'None':
										bTemp.append(tdata[ind].text.strip())
									else:
										bTemp.append(op.text)
							else:
								bTemp.append('')
						b.append(bTemp)

					for u in range(5):
						a = driver.find_elements(By.CLASS_NAME, "mixers_header_top")[1]
						if a.find_element(By.NAME, "Mixers.subcategorys."+str(u)+".selected").is_selected() == True:
							a.find_element(By.NAME, "Mixers.subcategorys."+str(u)+".selected").click()
							time.sleep(10)

					final.append([link, sub, h, b])
				err = 1
			except Exception as e:
				print('NAG ERROR OY: '+str(e))
				err = 0

			print('- result -')
			if err == 1:
				dups = []
				for x in final:
					# append_list_as_row(filepathHeader, ['>>>', x[0], x[1]])
					# append_list_as_row(filepathHeader, x[2])
					cout = 0
					for i in x[3]:
						if i not in dups:
							dups.append(i)
							append_list_as_row(filepathHeader, i)
							cout += 1
					print(x[1])
					print(cout)
		elif links[link] == 'attenuator':
			try:
				final = []
				for i in range(4):
					h = []
					b = []
					# try:
					# 	a = driver.find_elements(By.CLASS_NAME, "attenuators_header_top")[1]
					# except Exception:
					# 	a = driver.find_element(By.CLASS_NAME, "attenuators_header_top")
					# a.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].click()
					# time.sleep(10)

					# tbl_header = driver.find_elements(By.CLASS_NAME, "tbl_attenuators_header")
					# for th in tbl_header:
					# 	if 'none' not in str(th.get_attribute('style')):
					# 		# if th.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].is_selected() == False:
					# 		th.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].click()
					# 		time.sleep(10)
					# 	else:
					# 		print(th)

					ch = 0
					while ch == 0:
						try:
							a = driver.find_elements(By.CLASS_NAME, "attenuators_header_top")[1]
						except Exception:
							a = driver.find_element(By.CLASS_NAME, "attenuators_header_top")
						if a.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].is_selected() == False:
							a.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].click()
						time.sleep(10)
						try:
							a = driver.find_elements(By.CLASS_NAME, "attenuators_header_top")[1]
						except Exception:
							a = driver.find_element(By.CLASS_NAME, "attenuators_header_top")
						if a.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].is_selected() == True:
							ch = 1
						else:
							ch = 0

					moreData(driver)

					sub = driver.find_elements(By.CLASS_NAME, "subCategorySwitchCheckBox")[i].get_attribute('id')
					print('sub: '+sub)

					pagehtml = driver.page_source
					soup = bs4.BeautifulSoup(pagehtml, "html.parser")

					try:
						tb = soup.find('div', {'class': 'container_main'})
						tbl = tb.find_all('table')[1]
					except Exception:
						tb = soup.find_all('div', {'class': 'container_main'})[1]
						tbl = tb.find_all('table')[1]
					thead = tbl.find('tr', {'class': 'bg_color'}).find_all('th')
					for x in thead:
						h.append(x.text)

					tbody = tbl.find('tbody').find_all('tr')
					print(len(tbody))
					for trb in tbody:
						tdata = trb.find_all('td')
						bTemp = []
						bTemp.append(manufacturer)
						bTemp.append(cats[sub][0])
						bTemp.append(cats[sub][1])
						mn = ''

						op = tdata[0].find('output')
						if str(op) == 'None':
							mn = tdata[0].text.strip()
						else:
							mn = op.text

						img = tdata[h.index('Case Style')].find('output').text.strip()
						l = tdata[0].find('a')['href']

						bTemp.append(mn)
						if img != '':
							bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
						else:
							bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
						bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')
						bTemp.append('https://www.minicircuits.com/WebStore/'+l)

						for y in fHeader[7:]:
							chk = ''
							for th in thead:
								try:
									if y == header[th.text]:
										chk = th.text
								except Exception:
									pass
							if chk != '':
								nth = []
								for n in thead:
									nth.append(n.text)
								ind = nth.index(chk)
								op = tdata[ind].find('output')
								if 'ghz' in chk.lower():
									val = ''
									if str(op) == 'None':
										val = tdata[ind].text.strip()
									else:
										val = op.text

									if num_there(val) == True:
										a = float(re.sub('[a-zA-Z]+', '', val))*1000
										bTemp.append(str(a))
									else:
										bTemp.append(val)
								else:
									if str(op) == 'None':
										bTemp.append(tdata[ind].text.strip())
									else:
										bTemp.append(op.text)
							else:
								bTemp.append('')
						b.append(bTemp)

					final.append([link, sub, h, b])
				err = 1
			except Exception as e:
				driver.get('data:,')
				time.sleep(5)
				print('NAG ERROR OY: '+str(e))
				err = 0

			print('- result -')
			if err == 1:
				dups = []
				for x in final:
					# append_list_as_row(filepathHeader, ['>>>', x[0], x[1]])
					# append_list_as_row(filepathHeader, x[2])
					cout = 0
					for i in x[3]:
						if i not in dups:
							dups.append(i)
							append_list_as_row(filepathHeader, i)
							cout += 1
					print(x[1])
					print(cout)
		elif links[link] == 'filter':
			try:
				final = []
				for i in range(11):
					moreData(driver)
					h = []
					b = []
					a = driver.find_elements(By.CLASS_NAME, "filterby_menu_li")[i]
					sub = str(a.text)
					a.click()
					time.sleep(10)

					print('sub: '+sub)

					pagehtml = driver.page_source
					soup = bs4.BeautifulSoup(pagehtml, "html.parser")

					tbl = soup.find('div', {'class': 'container_main'}).find_all('table')[1]
					thead = tbl.find('tr', {'class': 'bg_color'}).find_all('th')
					for x in thead:
						h.append(x.text)

					tbody = tbl.find('tbody').find_all('tr')
					print(len(tbody))
					for trb in tbody:
						tdata = trb.find_all('td')
						bTemp = []
						bTemp.append(manufacturer)
						bTemp.append(cats[sub][0])
						bTemp.append(cats[sub][1])
						mn = ''

						# Get Model Number
						op = tdata[0].find('output')
						if str(op) == 'None':
							mn = tdata[0].text.strip()
						else:
							mn = op.text
						if mn == '':
							if 'first_cell_border' in str(tdata[0]):
								mn = 'first_cell_border'
							elif 'last_cell_border' in str(tdata[0]):
								mn = 'last_cell_border'

						# Model Number
						bTemp.append(mn)

						# Image
						try:
							img = tdata[h.index('Case Style')].find('output').text.strip()
							if img != '':
								bTemp.append('https://www.minicircuits.com/images/case_style/'+img+'.png')
							else:
								bTemp.append('https://www.minicircuits.com/images/model/'+mn+'.png')
						except Exception:
							if 'first_cell_border' in str(tdata[h.index('Case Style')]):
								bTemp.append('first_cell_border')
							elif 'last_cell_border' in str(tdata[h.index('Case Style')]):
								bTemp.append('last_cell_border')

						# PDF
						if 'first_cell_border' == mn:
							bTemp.append('first_cell_border')
						elif 'last_cell_border' == mn:
							bTemp.append('last_cell_border')
						else:
							bTemp.append('https://www.minicircuits.com/pdfs/'+mn+'.pdf')

						# LINK
						try:
							l = tdata[0].find('a')['href']
							bTemp.append('https://www.minicircuits.com/WebStore/'+l)
						except Exception:
							if 'first_cell_border' in str(tdata[h.index('Model Number')]):
								bTemp.append('first_cell_border')
							elif 'last_cell_border' in str(tdata[h.index('Model Number')]):
								bTemp.append('last_cell_border')

						for y in fHeader[7:]:
							chk = ''
							for th in thead:
								try:
									if y == header[th.text]:
										chk = th.text
								except Exception:
									pass
							if chk != '':
								nth = []
								for n in thead:
									nth.append(n.text)
								ind = nth.index(chk)
								op = tdata[ind].find('output')
								if 'ghz' in chk.lower():

									if str(op) == 'None':
										val = ''
										if str(tdata[ind].text.strip()) == '':
											if 'first_cell_border' in str(tdata[ind]):
												val = 'first_cell_border'
											elif 'last_cell_border' in str(tdata[ind]):
												val = 'last_cell_border'
										else:
											val = tdata[ind].text.strip()
									else:
										if str(op.text) == '':
											if 'first_cell_border' in str(tdata[ind]):
												val = 'first_cell_border'
											elif 'last_cell_border' in str(tdata[ind]):
												val = 'last_cell_border'
										else:
											val = op.text

									if num_there(val) == True:
										a = float(re.sub('[a-zA-Z]+', '', val))*1000
										bTemp.append(str(a))
									else:
										bTemp.append(val)
								else:
									if str(op) == 'None':
										if str(tdata[ind].text.strip()) == '':
											if 'first_cell_border' in str(tdata[ind]):
												bTemp.append('first_cell_border')
											elif 'last_cell_border' in str(tdata[ind]):
												bTemp.append('last_cell_border')
										else:
											bTemp.append(tdata[ind].text.strip())
									else:
										if str(op.text) == '':
											if 'first_cell_border' in str(tdata[ind]):
												bTemp.append('first_cell_border')
											elif 'last_cell_border' in str(tdata[ind]):
												bTemp.append('last_cell_border')
										else:
											bTemp.append(op.text)


							else:
								bTemp.append('')
						b.append(bTemp)

					newb = []
					for x in range(len(b)):
						t = []
						for y in range(len(b[x])):
							if 'first_cell_border' in str(b[x][y]):
								if 'first_cell_border' in str(b[x+1][y]) or 'last_cell_border' in str(b[x+1][y]):
									t.append('')
								else:
									n = str(b[x][y]).replace('first_cell_border', b[x+1][y])
									t.append(n)
							elif 'last_cell_border' in str(b[x][y]):
								if 'first_cell_border' in str(b[x-1][y]) or 'last_cell_border' in str(b[x-1][y]):
									t.append('')
								else:
									n = str(b[x][y]).replace('last_cell_border', b[x-1][y])
									t.append(n)
							else:
								if 'first_cell_border' in str(b[x][y]) or 'last_cell_border' in str(b[x][y]):
									t.append('')
								else:
									t.append(b[x][y])
						newb.append(t)

					final.append([link, sub, h, newb])
				err = 1
			except Exception as e:
				driver.get('data:,')
				time.sleep(5)
				print('NAG ERROR OY: '+str(e))
				err = 0

			print('- result -')
			if err == 1:
				dups = []
				for x in final:
					# append_list_as_row(filepathHeader, ['>>>', x[0], x[1]])
					# append_list_as_row(filepathHeader, x[2])
					cout = 0
					for i in x[3]:
						if i not in dups:
							dups.append(i)
							append_list_as_row(filepathHeader, i)
							cout += 1
					print(x[1])
					print(cout)
		else:
			err = 0
			print('ambot')

driver.quit()
# print('CUT HERE '+str(loop))
