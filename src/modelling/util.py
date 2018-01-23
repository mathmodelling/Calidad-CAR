import xlwt
from os import path

BOLD_FONT_XLWT = xlwt.Style.easyxf('font: bold on;')

def join(folder, name):
	return path.join(folder, name)

def used_vars(book, variables):
	sheet = book.add_sheet('Variables Usadas')

	sheet.write(0, 0, 'Variables Usadas', BOLD_FONT_XLWT)
	idx = 1

	for k, v in variables.iteritems():
		sheet.write(idx, 0, k, BOLD_FONT_XLWT)
		sheet.write(idx, 1, v)

		idx += 1
