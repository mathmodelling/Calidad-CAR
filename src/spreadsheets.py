# -*- coding: utf-8 -*-

'''
	Módulo encargado de crear hojas de
	cálculo con una plantilla determinada.
'''
import xlrd
import xlwt

BOLD_FONT_XLWT = xlwt.Style.easyxf('font: bold on;')
CONTAMINANTS = ['OD', 'DBO', 'NH4', 'NO2', 'NO3', 'TDS', 'GyA',
	'DQO', 'Porg', 'Pdis', 'EC', 'TC', 'T', 'TSS', 'SS', 'pH', 'ALK']

COLS_CONTAMINANTS = ['OD', 'DBO', 'NH4', 'NO2', 'NO3', 'TDS', 'GyA',
	'Condt', 'DQO', 'Porg', 'Pdis', 'EC', 'TC', 'T', 'TSS', 'SS', 'pH', 'ALK']

CONTAMINANTS_UNITS = ['mg/l', 'mg/l', 'mg/l','mg/l', 'mg/l', 'mg/l', 'mg/l' ,
	'mg/l', 'mg/l', 'mg/l', 'NMP','NMP', u'c°', 'mg/l', 'mg/l' ,'unidades de pH' ,'mg/l']

def create_description_sheet(workbook):
	'''
		Crear hoja de descripción:
	'''

	sheet = workbook.add_sheet(u'Descripción')

	sheet.col(0).width = 256*20
	sheet.col(1).width = 256*20
	sheet.col(2).width = 256*100

	sheet.write(0, 0, 'Nombre de la hoja', BOLD_FONT_XLWT)
	sheet.write(0, 1, 'Unidad de los datos', BOLD_FONT_XLWT)
	sheet.write(0, 2, u'Descripción de la hoja', BOLD_FONT_XLWT)

	# Hoja WD
	sheet.write(1, 0, 'WD')
	sheet.write(1, 1, 'm')
	sheet.write(1, 2, 'Valor de profundidad del agua (Water Depth)')	
	# Hoja SL
	sheet.write(2, 0, 'SL')
	sheet.write(2, 1, '-')
	sheet.write(2, 2, 'Valor de la pendiente (Slope)')	
	# Hoja WV
	sheet.write(3, 0, 'WV')
	sheet.write(3, 1, 'm/s')
	sheet.write(3, 2, 'Valor de la velocidad del agua (Water Velocity)')	
	# Hoja BC
	sheet.write(4, 0, 'BC')
	sheet.write(4, 1, '-')
	sheet.write(4, 2, 'Valores de la Condicion de Frontera (Boundary Conditions)')	
	# Hoja IC
	sheet.write(5, 0, 'IC')
	sheet.write(5, 1, '-')
	sheet.write(5, 2, 'Valores de la Condicion Inicial (Initial Conditions)')
	# Hoja Caudales
	sheet.write(6, 0, 'Caudales')
	sheet.write(6, 1, 'm3/s')
	sheet.write(6, 2, 'Hoja de Caudales')	

	cont = 7
	# Hojas de Sinks and Sources
	for i in range(len(CONTAMINANTS)):
		sheet.write(cont, 0, 'S'+CONTAMINANTS[i])
		sheet.write(cont, 1, CONTAMINANTS_UNITS[i])
		sheet.write(cont, 2, 'Valores de fuentes y sumideros ' + CONTAMINANTS[i])
		cont += 1

def create_sheet_dt(workbook, name, distances, hours, initial_value=None):
	'''
		Crea una hoja en el libro de excel distancia / tiempo.

		:param workbook: Libro de Excel en el que se va a crear
		la hoja.
		:type workbook: xlwt.Workbook

		:param name: Nombre de la hoja.
		:type name: str

		:param distances: Lista de distancias.
		:type distances: list
		
		:param hours: Límite de tiempo en horas.
		:type hours int

		:param initial_value: Valor inicial con el que llenar la hoja

	'''
	sheet = workbook.add_sheet(name)
	sheet.write(0, 0, 'L', BOLD_FONT_XLWT)

	# Crear columna de distancias
	for i in xrange(len(distances)):
		sheet.write(i + 1, 0, distances[i], BOLD_FONT_XLWT)

	# Crear la fila de tiempo
	for i in xrange(0,  hours + 1):
		sheet.write(0, i + 1, 3600 * i, BOLD_FONT_XLWT)

	if initial_value is not None:
		rows = len(distances)
		cols = hours + 1

		for i in xrange(1, rows + 1):
			for j in xrange(1, cols + 1):
				sheet.write(i, j, initial_value)

def create_sheet_td(workbook, name, distances, hours, initial_value=None):
	'''
		Crea una hoja el el libro de excel tiempo / distancia.

		:param workbook: Libro de Excel en el que se va a crear
		la hoja.
		:type workbook: xlwt.Workbook

		:param name: Nombre de la hoja.
		:type name: str

		:param distances: Lista de distancias.
		:type distances: list
		
		:param hours: Límite de tiempo en horas.
		:type hours int

		:param initial_value: Valor inicial con el que llenar la hoja

	'''
	sheet = workbook.add_sheet(name)
	sheet.write(0, 0, 'T', BOLD_FONT_XLWT)

	# Crear fila de distancias
	for i in xrange(len(distances)):
		sheet.write(0, i + 1, distances[i], BOLD_FONT_XLWT)

	# Crear la columna de tiempo
	for i in xrange(0,  hours + 1):
		sheet.write(i + 1, 0, 3600 * i, BOLD_FONT_XLWT)

	if initial_value is not None:
		rows = hours + 1
		cols = len(distances)

		for i in xrange(1, rows + 1):
			for j in xrange(1, cols + 1):
				sheet.write(i, j, initial_value)

def create_sheet_dc(workbook, name, distances, initial_value=None):
	'''
		Crea una hoja el el libro de excel distancia / contaminante.

		:param workbook: Libro de Excel en el que se va a crear
		la hoja.
		:type workbook: xlwt.Workbook

		:param name: Nombre de la hoja.
		:type name: str

		:param distances: Lista de distancias.
		:type distances: list

		:param initial_value: Valor inicial con el que llenar la hoja

	'''
	sheet = workbook.add_sheet(name)
	sheet.write(0, 0, 'L', BOLD_FONT_XLWT)
	
	# Crear fila de distancias
	for i in xrange(len(distances)):
		sheet.write(i + 1, 0, distances[i], BOLD_FONT_XLWT)

	# Crear la columna de contaminantes
	for i in xrange(len(COLS_CONTAMINANTS)):
		sheet.write(0, i + 1, COLS_CONTAMINANTS[i], BOLD_FONT_XLWT)
	
	if initial_value is not None:
		rows = len(distances)
		cols = len(COLS_CONTAMINANTS)

		for i in xrange(1, rows + 1):
			for j in xrange(1, cols + 1):
				sheet.write(i, j, initial_value)

def create_sheet_tc(workbook, name, hours, initial_value=None):
	'''
		Crea una hoja el el libro de excel tiempo / contaminante.

		:param workbook: Libro de Excel en el que se va a crear
		la hoja.
		:type workbook: openpyxl.Workbook

		:param name: Nombre de la hoja.
		:type name: str
		
		:param hours: Límite de tiempo en horas.
		:type hours int

		:param initial_value: Valor inicial con el que llenar la hoja

	'''
	sheet = workbook.add_sheet(name)
	sheet.write(0, 0, 'T', BOLD_FONT_XLWT)

	# Crear la fila del tiempo
	for i in xrange(0,  hours + 1):
		sheet.write(i + 1, 0, 3600 * i, BOLD_FONT_XLWT)

	# Crear la columna de contaminantes
	for i in xrange(len(COLS_CONTAMINANTS)):
		sheet.write(0, i + 1, COLS_CONTAMINANTS[i], BOLD_FONT_XLWT)

	if initial_value is not None:
		rows = hours + 1
		cols = len(COLS_CONTAMINANTS)

		for i in xrange(1, rows + 1):
			for j in xrange(1, cols + 1):
				sheet.write(i, j, initial_value)

def create_book(path, distances, hours, wd=None, sl=None):
	"""
		Crea archivo xlsx con el formato que se necesita

		:param path: Ruta del archivo que se va a crear
		:type path: str

		:param distances: Lista de distancias que se va usar
		:type distances: list

		:param hours: Límite de tiempo en hotas
		:type hours: int

		:param wd: Valor por defecto de wd
		:type wd: Decimal

		:param sl: Valor por defecto de sl
		:tpye sl: Decimal

	"""
	book = xlwt.Workbook()

	# Crear hoja WD
	create_sheet_dt(book, 'WD', distances, hours, wd)
	# Crear hoja SL
	create_sheet_dt(book, 'SL', distances, hours, sl)
	# Crear hoja WV
	create_sheet_dt(book, 'WV', distances, hours)
	# Crear hoja BC
	create_sheet_tc(book, 'BC', hours)
	# Crear hoja IC
	create_sheet_dc(book, 'IC', distances)

	# Crear hoja de Caudales
	create_sheet_dt(book, 'Caudales', distances, hours, 0)

	# Crear hojas de Sinks and Sources
	for contaminante in CONTAMINANTS:
		create_sheet_dt(book, 'S'+contaminante, distances, hours, 0.0)

	create_description_sheet(book)
	book.save(path)

	return book

class Error(Exception):
	def __init__(self, name, r, c):
		self.name = name
		self.r = r
		self.c = c
	def __str__(self):
		return "NaN : %s (%d, %d)" % (
			self.name,
			self.r,
			self.c)

class ErrorRow(Exception):
	def __init__(self, name, r, v):
		self.name = name
		self.r = r
		self.v = v
	def __str__(self):
		return "Error: La hoja %s no puede contener el valor %d en la fila %d" % (
			self.name,
			self.v,
			self.r)

def verify_sheet(sheet):
	"""Verifica que una hoja de cálculo no tenga celdas vacias."""
	rows, cols = sheet.nrows, sheet.ncols

	for i in xrange(1, rows):
		for j in xrange(1, cols):

			try:
				float(sheet.cell_value(i, j))
				continue
			except:
				raise Error(sheet.name, i + 1, j + 1)

def verify_sheet_row(sheet, row, value):
	"""Verifica que la hoja de cálculo no tenga el valor indicado en la fila indicada."""
	cols = sheet.ncols

	for j in xrange(1, cols):
		if int(sheet.cell_value(row, j)) == 0:
			raise ErrorRow(sheet.name, row, value)

def verify_book(workbook):
	"""Verifica que no exitan celdas vacias en todas las hojas del libro de excel."""
	# Verificar hoja WD
	verify_sheet(workbook.sheet_by_name(u'WD'))
	# Verificar hoja SL
	verify_sheet(workbook.sheet_by_name(u'SL'))
	# Verificar hoja WV
	verify_sheet(workbook.sheet_by_name(u'WV'))
	# Verificar hoja BC
	verify_sheet(workbook.sheet_by_name(u'BC'))
	# Verificar hoja IC
	verify_sheet(workbook.sheet_by_name(u'IC'))

	# Verificar hojas de Sinks and Sources
	for contaminante in CONTAMINANTS:
		# print 'S' + contaminante
		verify_sheet(workbook.sheet_by_name("S" + contaminante))

	verify_sheet(workbook.sheet_by_name(u'Caudales'))
	# Verifica que la primera linea no contenga 0's
	verify_sheet_row(workbook.sheet_by_name(u'Caudales'), 1, 0)

	# Obtener el tiempo
	sheet = workbook.sheet_by_name('WD')
	cols = sheet.ncols
	val = None
	try:
		val = int(sheet.cell_value(0, cols - 1))
	except:
		raise Error(sheet.name, 1, j + 1)

	return val


def load_book(path):
	# return openpyxl.load_workbook(path)
	return xlrd.open_workbook(path)


if __name__ == '__main__':
	d = [x for x in range(5)]
	# d = [0.00, 4.82, 9.63, 14.45, 19.26, 24.08,	28.89, 33.71, 38.52,
	# 	43.34, 48.15, 52.97, 57.78,	62.60, 67.41, 72.23, 77.04, 81.86,
	# 	86.67, 91.49, 96.30, 101.12, 105.93, 110.75, 115.56, 120.38, 
	# 	125.19, 130.01,	134.82,	139.64,	144.45,	149.27,	154.08,	158.90]
	# book = create_book("sample3.xls", d, 4, 1.0, 0.35)
	book = load_book("sample3.xlsx")
	print verify_book(book)
	



