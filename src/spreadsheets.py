# -*- coding: utf-8 -*-

'''
	Módulo encargado de crear hojas de
	cálculo con una plantilla determinada.
'''
import xlrd
import xlwt

BOLD_FONT_XLWT = xlwt.Style.easyxf('font: bold on;')
CONTAMINANTS = ['OD', 'DBO', 'NH4', 'NO2', 'NO3', 'TDS', 'GyA', 'Condt',
	'DQO', 'Porg', 'Pdis', 'EC', 'TC', 'T', 'PH', 'TSS', 'SS']

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
	sheet.write(0, 0, 'L', BOLD_FONT_XLWT)

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
	for i in xrange(len(CONTAMINANTS)):
		sheet.write(0, i + 1, CONTAMINANTS[i], BOLD_FONT_XLWT)
	
	if initial_value is not None:
		rows = len(distances)
		cols = len(CONTAMINANTS)

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
	sheet.write(0, 0, 'L', BOLD_FONT_XLWT)

	# Crear la fila del tiempo
	for i in xrange(0,  hours + 1):
		sheet.write(i + 1, 0, 3600 * i, BOLD_FONT_XLWT)

	# Crear la columna de contaminantes
	for i in xrange(len(CONTAMINANTS)):
		sheet.write(0, i + 1, CONTAMINANTS[i], BOLD_FONT_XLWT)

	if initial_value is not None:
		rows = hours + 1
		cols = len(CONTAMINANTS)

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

	# Crear hojas de Sinks and Sources
	for contaminante in CONTAMINANTS:
		create_sheet_dt(book, 'S'+contaminante, distances, hours, 0.0)

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

def verify_sheet(sheet):
	"""Verifica que una hoja de cálculo no tenga celdas vacias."""
	rows = sheet.nrows
	cols = sheet.ncols

	for i in xrange(1, rows ):
		for j in xrange(1, cols):

			try:
				float(sheet.cell_value(i, j))
				continue
			except:
				raise Error(sheet.name, i + 1, j + 1)

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
		verify_sheet(workbook.sheet_by_name("S" + contaminante))

def load_book(path):
	# return openpyxl.load_workbook(path)
	return xlrd.open_workbook(path)


if __name__ == '__main__':
	# d = [0.00, 4.82, 9.63, 14.45, 19.26, 24.08,	28.89, 33.71, 38.52,
	# 	43.34, 48.15, 52.97, 57.78,	62.60, 67.41, 72.23, 77.04, 81.86,
	# 	86.67, 91.49, 96.30, 101.12, 105.93, 110.75, 115.56, 120.38, 
	# 	125.19, 130.01,	134.82,	139.64,	144.45,	149.27,	154.08,	158.90]
	# book = create_book("sample3.xls", d, 24, 1.0, 0.35)
	book = load_book("sample2.xlsx")
	verify_book(book)
	



