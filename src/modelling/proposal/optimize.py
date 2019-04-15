#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

OBJETIVE_FILE = "./salida/Objetivo.xlsx"


"""
 Variables to change ko2, kdbo, kDQO
 Dependency relation
 c_OD = { +ko2,-kdbo  }
 DBO =  {-kdbo, }
 DQ0 =  {kDQO}
"""
def read_objetive_values():
    data = pd.read_excel(OBJETIVE_FILE, index_col=None)
    return data

def computeError( nameExcelResults ):
    SHEETS_NAME = ['T','OD','DBO','NH3','NO2','NO3','DQO','TDS','EC','TC','GyA','Conduct','Porg','Pdis','TSS','SS','pH','ALK']
    n = len(SHEETS_NAME)
    objetiveData = read_objetive_values()
    def pow2( a ): return a * a
    errorTotal = 0
    for sheet in SHEETS_NAME:
        errorLocal = 0
        data = pd.read_excel(nameExcelResults, index_col=0, sheet_name=sheet)
        rows, cols = data.shape
        for i in range( cols):
            meanReal = data[ i ].mean()
            expected = objetiveData[sheet].iloc[i]
            #print( meanReal, expected)
            errorLocal = abs( pow2(meanReal-expected) )
        errorLocal /= cols
        errorTotal+= errorLocal
        print("{} MSE = {}".format(sheet, errorLocal))
    errorTotal /= n
    print("MSE TOTAL = {}".format(errorTotal))
    return errorTotal


def testEnd():
    computeError("./salida/Resultados24Horas.xls")

if __name__ == "__main__":
    testEnd()
