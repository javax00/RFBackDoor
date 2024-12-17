import mysql.connector
import pandas as pd
import psycopg2
import datetime

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="rfbackdoor"
)

def getPLN():
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM api_products ORDER BY id DESC LIMIT 1")
	myresult = mycursor.fetchall()

	if myresult == []:
		return 0
	else:
		return int(myresult[0][0])

def getPSLN():
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM api_productspecification ORDER BY id DESC LIMIT 1")
	myresult = mycursor.fetchall()

	if myresult == []:
		return 0
	else:
		return int(myresult[0][0])

def getSpecs():
	mycursor = mydb.cursor()
	mycursor.execute("SELECT id,name FROM api_specification")
	myresult = mycursor.fetchall()

	if myresult == []:
		return 0
	else:
		return myresult

def reDec(s):
	if any(c.isalpha() for c in str(s)) == False:
		if '.' in str(s):
			con = str(s).split('.')
			if len(con) >= 3:
				return s
			else:
				if str(con[-1]) == '0':
					return int(con[0])
				else:
					return s
		else:
			return s
	else:
		return s

def getIndex(myList, v):
	for i, x in enumerate(myList):
		if v in x:
			# return (i, x.index(v))
			return i+1

def getListIndex(myList, v):
	for i, x in enumerate(myList):
		if v in x:
			# return (i, x.index(v))
			return x

cats = [["AMPLIFIER", "4", "2"],
		["VGA AMPLIFIER", "90", "2"],
		["DRIVER AMPLIFIER", "31", "2"],
		["POWER AMPLIFIER", "67", "2"],
		["LOW NOISE AMPLIFIER", "50", "2"],
		["MIXER", "56", "23"],
		["UP CONVERTER", "86", "23"],
		["DOWN CONVERTER", "30", "23"],
		["SWITCH", "76", "36"],
		["POWER DETECTOR", "68", "31"],
		["TX RX MODULE", "85", "39"],
		["TRANSCEIVER", "80", "39"],
		["RECEIVER", "72", "39"],
		["OSCILLATOR", "60", "26"],
		["ATTENUATOR", "8", "4"],
		["PHASE SHIFTER", "66", "29"],
		["PHASE-LOCKED LOOP", "65", "30"],
		["FILTER", "120", "16"],
		["LOW PASS FILTER", "51", "16"],
		["BAND PASS FILTER", "10", "16"],
		["FREQUENCY DIVIDER", "39", "18"],
		["SYNTHESIZER", "78", "37"],
		["PHASE DETECTOR", "64", "28"],
		["MULTIPLIER", "58", "25"],
		["MULTIPLEXER", "57", "24"],
		["BIAS CONTROLLER", "11", "27"]]

prodSpecs = ["Manufacturer", "Category", "Subcategory", "Part Number", "Image", "PDF"]


from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askopenfilename
from csv import writer
import pandas as pd
import kthread
import random
import time
import os

window = Tk()
window.title("Upload Database")
window.wm_iconbitmap('logo.ico')
window.resizable(0,1)
window.minsize(width=360, height=260)

def threadStart():
	global B
	B.config(state="disabled")
	global thread
	thread = kthread.KThread(target=onClicked)
	thread.start()

def threadStop():
	global B
	B.config(state="normal")
	global thread
	if thread.is_alive():
		thread.terminate()

def onClicked():
	global filename
	global txtbox
	global B
	txtbox.delete('1.0', END)

	B.config(state="disabled")

	txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

	df = pd.read_csv(filename)
	specList = getSpecs()

	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="rfbackdoor")

	cur = mydb.cursor()
	cur.execute("""SELECT
						p.id,
						p.product_partnumber,
						GROUP_CONCAT(ps.specification_id,'^',ps.value SEPARATOR '~')
					FROM
						api_products as p,
						api_productspecification as ps
					WHERE
						p.id=ps.product_id
						GROUP BY p.id""")
	query_results = cur.fetchall()

	dbFinal = []
	for x in query_results:
		con = []
		con.append(x[0])
		con.append(x[1])
		for y in x[2].split('~'):
			con.append(y.split('^'))
		dbFinal.append(con)

	delListDb = []
	for x in dbFinal:
		delListDb.append([x[0], x[1]])

	dup = []
	final_product_insert = []
	final_product_spec_insert = []
	final_product_update = []
	final_product_spec_update = []
	final_product_delete = []
	count_p = getPLN()
	count_ps = getPSLN()
	cL = []
	pn = ''
	for i in df.index:
		con = []
		for x in df:
			if str(x) == 'Part Number':
				con.append(str(df[x][i]))
				pn = str(df[x][i])
		for x in df:
			if str(x) == 'Image':
				if str(df[x][i]) == 'nan':
					con.append('')
				else:
					con.append(str(df[x][i]))
		for x in df:
			if str(x) == 'PDF':
				con.append(str(df[x][i]))
		for x in df:
			if str(x) == 'Subcategory':
				for y in cats:
					if str(df[x][i]) == y[0]:
						con.append(str(y[2]))
		for x in df:
			if str(x) == 'Manufacturer':
				con.append(str(df[x][i]))
		for x in df:
			if str(x) == 'Subcategory':
				for y in cats:
					if str(df[x][i]) == y[0]:
						con.append(str(y[1]))

		if con[0] not in dup:
			val = str(getIndex(dbFinal, con[0]))
			if val == 'None':
				count_p += 1
				for x in df:
					if str(x) not in prodSpecs:
						if str(df[x][i]) != 'nan':
							for y in specList:
								if y[1] == x:
									count_ps += 1
									final_product_spec_insert.append([count_ps, str(reDec(df[x][i])), count_p, y[0]])

				con.insert(0, count_p)
				final_product_insert.append(con)
			else:
				conVal1 = []
				conVal = getListIndex(dbFinal, int(val))
				needUpdate = 0
				for x in df:
					if str(x) not in prodSpecs:
						if str(df[x][i]) != 'nan':
							for y in specList:
								if y[1] == x:
									conVal1.append([str(y[0]), str(reDec(df[x][i]))])
				c = 0
				for x in dbFinal:
					if conVal1 == x[2:]:
						c += 1
				if c == 0:
					conVal1.insert(0, conVal[0]+1)
					final_product_update.append(con)
					final_product_spec_update.append(conVal1)

		dup.append(pn)

	delListCSV = []
	for i in df.index:
		for x in df:
			if str(x) == 'Part Number':
				delListCSV.append(str(df[x][i]))
	for x in delListDb:
		if x[1] not in delListCSV:
			final_product_delete.append(x[0])

	# print(final_product_insert)
	# print(final_product_spec_insert)
	# print('~')
	# print(final_product_update)
	# print(final_product_spec_update)
	# print('~')
	# print(final_product_delete)
	# print('~~')


	#**********************************
	# INSERT
	if final_product_insert == []:
		txtbox.delete('1.0', END)
		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		txtbox.insert(END, 'Insert product: {}'.format(len(final_product_insert)))
	else:
		count = 0
		tot = len(final_product_insert)+len(final_product_spec_insert)
		for x in final_product_insert:
			mycursor = mydb.cursor()
			ct = datetime.datetime.now(datetime.timezone.utc)

			sql = "INSERT INTO api_products (id, product_partnumber, image_link, pdf_link, created_at, updated_at, category_id, manufacturer_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			val = (x[0], x[1], x[2], x[3], ct, ct, x[4], x[5], x[6])
			mycursor.execute(sql, val)
			mydb.commit()

			count += 1
			txtbox.delete('1.0', END)
			txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
			txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			txtbox.insert(END, 'Insert product: {} - {}%'.format(len(final_product_insert), int((count/tot)*100)))

		for x in final_product_spec_insert:
			mycursor = mydb.cursor()
			ct = datetime.datetime.now(datetime.timezone.utc)

			sql = "INSERT INTO api_productspecification (value, created_at, updated_at, product_id, specification_id) VALUES (%s, %s, %s, %s, %s)"
			val = (x[1], ct, ct, x[2], x[3])
			mycursor.execute(sql, val)
			mydb.commit()

			count += 1
			txtbox.delete('1.0', END)
			txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
			txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			txtbox.insert(END, 'Insert product: {} - {}%'.format(len(final_product_insert), int((count/tot)*100)))
		mycursor.close()

	# UPDATE
	if final_product_update == []:
		txtbox.delete('1.0', END)
		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
		txtbox.insert(END, 'Update product: {}'.format(len(final_product_update)))
	else:
		count = 0
		tot = len(final_product_update)+len(final_product_spec_update)
		for x in final_product_update:
			mycursor = mydb.cursor()
			ct = datetime.datetime.now(datetime.timezone.utc)

			sql = "UPDATE api_products SET image_link=%s, pdf_link=%s, updated_at=%s, category_id=%s, manufacturer_id=%s, subcategory_id=%s WHERE product_partnumber=%s"
			val = (x[1], x[2], ct, x[3], x[4], x[5], x[0])
			mycursor.execute(sql, val)
			mydb.commit()

			count += 1
			txtbox.delete('1.0', END)
			txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
			txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
			txtbox.insert(END, 'Update product: {} - {}%'.format(len(final_product_update), int((count/tot)*100)))

		for x in final_product_spec_update:
			mycursor = mydb.cursor()
			sql = "DELETE FROM api_productspecification WHERE product_id=%s"
			adr = (x[0], )
			mycursor.execute(sql, adr)
			mydb.commit()

			for y in x[1:]:
				sql = "INSERT INTO api_productspecification (value, created_at, product_id, specification_id, updated_at) VALUES (%s, %s, %s, %s, %s)"
				val = (y[1], ct, x[0], y[0], ct)
				mycursor.execute(sql, val)
				mydb.commit()

			count += 1
			txtbox.delete('1.0', END)
			txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
			txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
			txtbox.insert(END, 'Update product: {} - {}%'.format(len(final_product_update), int((count/tot)*100)))
		mycursor.close()

	# DELETE
	if final_product_delete == []:
		txtbox.delete('1.0', END)
		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
		txtbox.insert(END, 'Update product: {} - Done\n'.format(len(final_product_update)))
		txtbox.insert(END, 'Delete product: {}'.format(len(final_product_delete)))
	else:
		count = 0
		tot = len(final_product_delete)
		for x in final_product_delete:
			mycursor = mydb.cursor()
			sql = "DELETE FROM api_productspecification WHERE product_id=%s"
			adr = (x, )
			mycursor.execute(sql, adr)
			mydb.commit()

			mycursor = mydb.cursor()
			sql = "DELETE FROM api_products WHERE id=%s"
			adr = (x, )
			mycursor.execute(sql, adr)
			mydb.commit()

			txtbox.delete('1.0', END)
			txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
			txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
			txtbox.insert(END, 'Update product: {} - {}%'.format(len(final_product_update), int((count/tot)*100)))

			count += 1
			txtbox.delete('1.0', END)
			txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
			txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
			txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
			txtbox.insert(END, 'Update product: {} - Done\n'.format(len(final_product_update)))
			txtbox.insert(END, 'Delete product: {} - {}%'.format(len(final_product_delete), int((count/tot)*100)))
		mycursor.close()
	#**********************************

	########################################
	# conn = psycopg2.connect(
	# 	database = "ded39uu86mkoti",
	# 	user = "ikvynyyaguqmch",
	# 	password = "b0455aaf8d490a0e74eb9a18d97ec8278ae17b4a8b8f5f49685c3ac769ed907d",
	# 	host = "ec2-54-242-43-231.compute-1.amazonaws.com",
	# 	port = "5432")
	# print('connected')

	# # INSERT
	# if final_product_insert == []:
	# 	txtbox.delete('1.0', END)
	# 	txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 	txtbox.insert(END, 'Insert product: {}'.format(len(final_product_insert)))
	# else:
	# 	count = 0
	# 	tot = len(final_product_insert)+len(final_product_spec_insert)
	# 	for x in final_product_insert:
	# 		mycursor = conn.cursor()
	# 		ct = datetime.datetime.now(datetime.timezone.utc)

	# 		sql = "INSERT INTO api_products (id, product_partnumber, image_link, pdf_link, created_at, updated_at, category_id, manufacturer_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	# 		val = (x[0], x[1], x[2], x[3], ct, ct, x[4], x[5], x[6])
	# 		mycursor.execute(sql, val)
	# 		conn.commit()

	# 		count += 1
	# 		txtbox.delete('1.0', END)
	# 		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 		txtbox.insert(END, 'Insert product: {} - {}%'.format(len(final_product_insert), int((count/tot)*100)))

	# 	for x in final_product_spec_insert:
	# 		mycursor = conn.cursor()
	# 		ct = datetime.datetime.now(datetime.timezone.utc)

	# 		sql = "INSERT INTO api_productspecification (value, created_at, updated_at, product_id, specification_id) VALUES (%s, %s, %s, %s, %s)"
	# 		val = (x[1], ct, ct, x[2], x[3])
	# 		mycursor.execute(sql, val)
	# 		conn.commit()

	# 		count += 1
	# 		txtbox.delete('1.0', END)
	# 		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 		txtbox.insert(END, 'Insert product: {} - {}%'.format(len(final_product_insert), int((count/tot)*100)))
	# 	mycursor.close()

	# # UPDATE
	# if final_product_update == []:
	# 	txtbox.delete('1.0', END)
	# 	txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 	txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	# 	txtbox.insert(END, 'Update product: {}'.format(len(final_product_update)))
	# else:
	# 	count = 0
	# 	tot = len(final_product_update)+len(final_product_spec_update)
	# 	for x in final_product_update:
	# 		mycursor = conn.cursor()
	# 		ct = datetime.datetime.now(datetime.timezone.utc)

	# 		sql = "UPDATE api_products SET image_link=%s, pdf_link=%s, updated_at=%s, category_id=%s, manufacturer_id=%s, subcategory_id=%s WHERE product_partnumber=%s"
	# 		val = (x[1], x[2], ct, x[3], x[4], x[5], x[0])
	# 		mycursor.execute(sql, val)
	# 		conn.commit()

	# 		count += 1
	# 		txtbox.delete('1.0', END)
	# 		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 		txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	# 		txtbox.insert(END, 'Update product: {} - {}%'.format(len(final_product_update), int((count/tot)*100)))

	# 	for x in final_product_spec_update:
	# 		mycursor = conn.cursor()
	# 		sql = "DELETE FROM api_productspecification WHERE product_id=%s"
	# 		adr = (x[0], )
	# 		mycursor.execute(sql, adr)
	# 		conn.commit()

	# 		for y in x[1:]:
	# 			sql = "INSERT INTO api_productspecification (value, created_at, product_id, specification_id, updated_at) VALUES (%s, %s, %s, %s, %s)"
	# 			val = (y[1], ct, x[0], y[0], ct)
	# 			mycursor.execute(sql, val)
	# 			conn.commit()

	# 		count += 1
	# 		txtbox.delete('1.0', END)
	# 		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 		txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	# 		txtbox.insert(END, 'Update product: {} - {}%'.format(len(final_product_update), int((count/tot)*100)))
	# 	mycursor.close()

	# # DELETE
	# if final_product_delete == []:
	# 	txtbox.delete('1.0', END)
	# 	txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 	txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	# 	txtbox.insert(END, 'Update product: {} - Done\n'.format(len(final_product_update)))
	# 	txtbox.insert(END, 'Delete product: {}'.format(len(final_product_delete)))
	# else:
	# 	count = 0
	# 	tot = len(final_product_delete)
	# 	for x in final_product_delete:
	# 		mycursor = conn.cursor()
	# 		sql = "DELETE FROM api_productspecification WHERE product_id=%s"
	# 		adr = (x, )
	# 		mycursor.execute(sql, adr)
	# 		conn.commit()

	# 		mycursor = conn.cursor()
	# 		sql = "DELETE FROM api_products WHERE id=%s"
	# 		adr = (x, )
	# 		mycursor.execute(sql, adr)
	# 		conn.commit()

	# 		txtbox.delete('1.0', END)
	# 		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 		txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	# 		txtbox.insert(END, 'Update product: {} - {}%'.format(len(final_product_update), int((count/tot)*100)))

	# 		count += 1
	# 		txtbox.delete('1.0', END)
	# 		txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	# 		txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	# 		txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	# 		txtbox.insert(END, 'Update product: {} - Done\n'.format(len(final_product_update)))
	# 		txtbox.insert(END, 'Delete product: {} - {}%'.format(len(final_product_delete), int((count/tot)*100)))
	# 	mycursor.close()
	########################################
	txtbox.delete('1.0', END)
	txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	txtbox.insert(END, 'Insert product: {} - Done\n'.format(len(final_product_insert)))
	txtbox.insert(END, 'Update product: {} - Done\n'.format(len(final_product_update)))
	txtbox.insert(END, 'Delete product: {} - Done'.format(len(final_product_delete)))
	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	txtbox.insert(END, 'Done.')

	conn.close()
	mydb.close()
	threadStop()

def closeWindow():
	window.quit()
	global thread
	if thread.is_alive():
		thread.terminate()

def main():
	global filename
	filename = askopenfilename()

	#ENTRY
	widget = Frame(window)
	widget.grid(row=0, column=0, sticky=W+E)

	#BUTTON
	global B
	B = Button(widget, text = "Upload now", width=40, command=threadStart)
	B.grid(row=3, column=1, pady=5, padx=5)

	B1 = Button(widget, text = "X", width=4, command=threadStop)
	B1.grid(row=3, column=0, padx=5)

	#DISPLAY
	frame = Frame(window)
	frame.grid(row=1, column=0, columnspan=3, sticky=E+W+N+S)

	window.columnconfigure(0, weight=1)
	window.rowconfigure(1, weight=1)

	frame.rowconfigure(0, weight=1)
	frame.columnconfigure(0, weight=1)

	# Create the textbox
	global txtbox
	txtbox = scrolledtext.ScrolledText(frame, width=15, height=1, font=("Helvetica", 10), background="black", foreground="yellow")
	txtbox.grid(row=0, column=0, sticky=E+W+N+S)
	txtbox.bind("<Key>", lambda e: "break")

	txtbox.insert(END, '({}) File Loaded'.format(filename.split('/')[-1]))
	txtbox.insert(END, '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

	window.protocol("WM_DELETE_WINDOW", closeWindow)
	window.mainloop()

if __name__ == '__main__':
	main()