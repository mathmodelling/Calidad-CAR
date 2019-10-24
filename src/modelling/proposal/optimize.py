#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

OBJETIVE_FILE = "./FOptimize/Objetivo.xlsx"
DEPENDENCY_FILE = "./FOptimize/Dependencias.xlsx"


"""
 Variables to change ko2, kdbo, kDQO
 Dependency relation
          add    substract
 OD = { +ko2, -kdbo  }

         substract
 DBO =  {-kdbo, }

         substract
 DQO =  {-kDQO}
"""
def read_objetive_values():
    data = pd.read_excel(OBJETIVE_FILE, index_col=None)
    return data

def read_dependency_values():
    data = pd.read_excel(DEPENDENCY_FILE)
    OBJETIVOS_A_OPTIMIZAR = data["Name"].astype(str).tolist()
    DEPENDENCIAS = list(data)[1:]
    DEPENDENCIAS = [str(x) for x in DEPENDENCIAS]

    dependencyi = dict()
    sign_dependency = dict()
    objetivos = []
    to_optimize = []
    for dependencia in DEPENDENCIAS:
        for objetivo in range(0, len(OBJETIVOS_A_OPTIMIZAR)):
            val = data[dependencia][objetivo]
            if( "x" in str(val) ): continue
            name = OBJETIVOS_A_OPTIMIZAR[objetivo]
            if( name not in objetivos): objetivos.append( name)
            if( dependencia not in to_optimize): to_optimize.append( dependencia)
            if( dependencia in sign_dependency.keys()): sign_dependency[dependencia] += val
            else: sign_dependency[dependencia] = val
            if( name in dependencyi.keys()): dependencyi[name].append( dependencia)
            else: dependencyi[name]=[dependencia]
    return objetivos, dependencyi, sign_dependency, to_optimize

"""
    This function compute error, base on the variables to OPTIMIZE:
"""
def computeError( nameExcelResults ):
    #SHEETS_NAME = ['T','OD','DBO','NH3','NO2','NO3','DQO','TDS','EC','TC','GyA','Conduct','Porg','Pdis','TSS','SS','pH','ALK']
    #SHEETS_NAME = ['OD', 'DBO', 'DQO']
    #dependencyi = {'OD':'ko2',  'DBO':'kdbo',  'DQO':'kDQO'}
    #sign_dependency = {'ko2':1,  'kdbo':-1,  'kDQO':-1}

    SHEETS_NAME, dependencyi, sign_dependency, to_optimize = read_dependency_values()

    objetiveData = read_objetive_values()
    types = dict()
    errores = dict()
    print("\n Errors: ")
    def pow2( a ): return a * a
    errorTotal = 0
    for sheet in SHEETS_NAME:
        errorLocal = 0
        data = pd.read_excel(nameExcelResults, index_col=0, sheet_name=sheet)
        rows, cols = data.shape
        diff = 0
        for i in range( cols):
            meanReal = data[ i ].mean(skipna=True)
            expected = objetiveData[sheet].iloc[i]
            #print( meanReal, expected)
            diff += meanReal - expected
            errorLocal = abs( pow2(meanReal-expected) )
        errorLocal /= cols
        for var in dependencyi.keys():
            for aux in dependencyi[var]:
                if( aux in errores.keys()): errores[aux] += errorLocal
                else: errores[aux] = errorLocal
                if( errores[aux] != 0):
                    errores[aux] = errores[aux]// errores[aux]
                errorTotal+= errorLocal
                if diff == 0: type = 0
                elif diff < 0: type = -1
                else:  type = 1
                types[aux] =type
        print("\t{} MSE = {}, Type = {} ".format(sheet, errorLocal, type))
    errorTotal /= len(SHEETS_NAME)
    print("\tMSE TOTAL = {}".format(errorTotal))
    return errores, types, sign_dependency, to_optimize


def testEnd():
    computeError("./salida/Resultados24Horas.xls")

if __name__ == "__main__":
    testEnd();
