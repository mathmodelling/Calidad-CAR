#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'Efraín Domínguez Calle, PhD - Wilfredo Marimón Bolivar, PhD'
__copyright__ = "Copyright 2017, Mathmodelling"
__credits__ = ["Efraín Domínguez Calle"]
__license__ = "Uso Libre"
__version__ = "1.0"
__maintainer__ = "Efraín Antonio Domínguez Calle"
__email__ = 'edoc@marthmodelling.org, w.marimon@javeriana.edu.co'
__status__ = "En desarrollo"


from builtins import range


#Base Imports
import xlrd
import xlwt
import numpy as np
import datetime
import sys
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt


# Utilities
from util import join
from util import used_vars
from util import read_sheet
from util import save_sheet
from util import save_plot
from util import plot
from util import getTime

from optimize import computeError

import config


def f(array1, array2, array3):
    return array1 * array2 / (array3 + array2)

def _read_config_file(config_file, sheet_names=config.SHEET_NAMES):
    """
    Reads an Excel configuration file with initial and boundary conditions and also time series for sinks and sources
    :param config_file: The path to the excel file
    :type config_file: str
    :param sheet_names: names of the needed sheets
    :type sheet_names: dict
    """

    C = dict()
    wb = xlrd.open_workbook(config_file)

    for name, sheet_name in sheet_names.items():
        C[name] = read_sheet(wb, sheet_name)

    # A estos arreglos se les aplica la misma función f
    arreglos_f = ['SOD', 'SDBO', 'SNH3', 'SNO2', 'SNO3',
                  'SDQO', 'STDS', 'SGyA', 'SEC', 'STC',
                  'SPorg', 'SPdis', 'STSS', 'SSS', 'SALK']

    for arreglo in arreglos_f:
        C[arreglo] = f(C[arreglo][0:, 1:], C['Caudales'][0:, 1:], C['Caudales'][0, 1:])

    C['ST'] = (C['ST'][0:, 1:] + 273)
    C['SpH'] = (10**(-1 * (C['SpH'][0:, 1:]))) * C['Caudales'][0:, 1:] / (C['Caudales'][0, 1:] + C['Caudales'][0:, 1:])

    return C

def fn_advection(vel, co, dtx, ki, kr):
    """
    Advection equation calculator
    :param vel: Velocity vector
    :param co: Initial concentration vector
    :param dtx: dt / dx
    :return: Advection vector
    """

    adv = -((ki[2:] * vel[2:] * co[2:] - ki[1:-1] * vel[1:-1] * co[1:-1]) * dtx +
            (kr[1:-1] * vel[1:-1] * co[1:-1] - kr[0:-2] * vel[0:-2] * co[0:-2]) * dtx)

    return adv

def fn_diffusion(d, co, dtx):
    """
    Diffusion equation calculator
    :param d: Diffusion coefficient
    :param co: Initial concentration
    :param dtx: dt / (dx**2)
    :param dx: Spatial discretization
    :return: Diffusion vector
    """
    dif = 0.5 * (d[2:] * co[2:] - 2 * d[1:-1] * co[1:-1] + d[0:-2] * co[0:-2]) * dtx

    return dif

def fn_reactions(c_T=None, c_OD=None, c_DBO=None, c_NH3=None, c_NO2=None, c_NO3=None, c_DQO=None,
                 c_TDS=None, c_EC=None, c_TC=None, c_GyA=None, c_pH=None, c_Porg=None, c_TSS=None,
                 c_SS=None, c_ALK=None, c_Pdis=None, dt=None, k=None, D=None):
    """
    Reaction equations calculator
    :return: Transport reactions by variable, like a dictionary ("OD", "DBO", "NH3", "NO2", "NO3", "DQO", 'TDS', "EC", "TC", "GyA",
                                                                "Porg", "Pdis", "TSS", "SS")
    """
    p = (c_OD[0:-2]) / ((c_OD[0:-2]) + k['ks'])

    T = (k['Jsn'] + k['sbc'] * ((k['Tair'] + 273) ** 4) * (k['Aair'] + 0.031 * ((k['eair']) ** 0.5)) * (1 - k['RL']) - 0.97 * k['sbc'] * (
        (c_T[0:-2]) ** 4) - 0.47 * (19 + (0.95 * (k['Uw'] ** 2))) * ((c_T[0:-2]) - k['Tair'] - 273.15) - (19 + (0.95 * (k['Uw'] ** 2))) * (
        k['es'] - k['eair'])) * D/ (k['den'] * k['Cp'] * k['As1'])

    OD = (k['Da'] + k['ko2'] * (k['cs'] - c_OD[0:-2]) - k['kdbo'] * c_DBO[0:-2] * p * (
        k['teta_DBO'] ** (c_T[0:-2] - 293.15)) - k['alfa_nh3'] * k['knh3'] * c_NH3[0:-2] * p *
        (k['teta_NH3'] ** (c_T[0:-2] - 293.15)) - k['alfa_no2'] * k['kno2'] * c_NO2[0:-2] * p * (
        k['teta_NO2'] ** (c_T[0:-2] - 293.15)) - k['ksod'] / D) * dt

    DBO = (-k['kdbo'] * c_DBO[0:-2] * p * (k['teta_DBO'] ** (c_T[0:-2] - 293.15))) * dt

    NH3 = (k['knt'] * k['NT'] * (k['teta_NT'] ** (c_T[0:-2] - 293.15)) - k['knh3'] * c_NH3[0:-2] * p * (
        k['teta_NH3'] ** (c_T[0:-2] - 293.15)) + k['ksnh3'] / D - k['F'] * k['alfa_1'] * k['miu'] * k['A']) * dt

    NO2 = (k['knh3'] * c_NH3[0:-2] * p * (k['teta_NH3'] ** (c_T[0:-2] - 293.15)) - k['kno2'] * c_NO2[0:-2] * p * (
        k['teta_NO2'] ** (c_T[0:-2] - 293.15)) + k['kno3'] * c_NO3[0:-2] * (k['teta_NO3'] ** (c_T[0:-2] - 293.15))) * dt

    NO3 = (k['kno2'] * c_NO2[0:-2] * p * (k['teta_NO2'] ** (c_T[0:-2] - 293.15)) - k['kno3'] * c_NO3[0:-2] * (
        k['teta_NO3'] ** (c_T[0:-2] - 293.15)) - (1 - k['F']) * k['alfa_1'] * k['miu'] * k['A']) * dt

    DQO = (-k['kDQO'] * c_DQO[0:-2] * p * (k['teta_DQO'] ** (c_T[0:-2] - 293.15))) * dt

    TDS = (-k['kTDS'] * c_TDS[0:-2]) * dt

    EC = (-k['kEC'] * c_EC[0:-2] * (k['teta_EC'] ** (c_T[0:-2] - 293.15))) * dt

    TC = (-k['kTC'] * c_TC[0:-2] * (k['teta_TC'] ** (c_T[0:-2] - 293.15))) * dt

    GyA = (k['Jdbw'] / D + k['qtex'] / D - (k['kN'] + k['kH'] * c_pH[0:-2] - k['kOH'] * (k['Kw'] / c_pH[0:-2])) *
        k['fdw'] * c_GyA[0:-2] - k['kf'] * c_GyA[0:-2] - k['kb'] * c_GyA[0:-2] - k['kv'] * (
        (k['Cg'] / (k['Henry'] / (k['R'] * c_T[0:-2]))) - k['fdw'] * c_GyA[0:-2])) * dt / (10 * k['tfactor'])

    Porg = (k['alfa_2'] * k['resp'] * k['A'] - k['kPorg'] * c_Porg[0:-2] - k['kPsed'] * c_Porg[0:-2]) * dt

    Pdis = (k['kPorg'] * c_Porg[1:-1] + k['kPsed'] / D - k['sigma2'] * k['miu'] * k['A']) * dt

    TSS = k['qtex'] * (-k['Ws'] * c_TSS[0:-2] / D + k['Rs'] / D + k['Rp'] / D) * dt

    SS = k['qtex'] * (-k['Ws'] * c_SS[0:-2] / D + k['Rs'] / D + k['Rp'] / D) * dt

    ALK = k['Wrp'] + k['Vv'] * k['As'] * (k['CO2S'] - ((c_pH[0:-2]) * (c_pH[0:-2]) / (((c_pH[0:-2]) * (c_pH[0:-2])) +
        k['K1'] * (c_pH[0:-2]) + k['K1'] * k['K2'])) * c_ALK[0:-2])

    pH = ((k['Kw'] / (k['FrH'] * (c_ALK[0:-2])) ** 0.5))

    return dict(T=T, OD=OD, DBO=DBO, NH3=NH3, NO2=NO2, NO3=NO3, DQO=DQO, TDS=TDS, EC=EC, TC=TC, GyA=GyA,
                Porg=Porg, Pdis=Pdis, TSS=TSS, SS=SS, ALK=ALK, pH=pH)


def calidad_explicito(D, dx, Ci, S, v, d, Caudales, k):
    """
    Esta función modela la transición de la concentración del momento t al momento t + dt para todos los
    nodos espaciales de la corriente superficial
    """

    variables = config.VARIABLES

    C = dict()
    Cout = dict()

    for var in variables:
        C["c_{}".format(var)] = Ci["ci_{}".format(var)]

    maxv = abs(np.max(v))
    maxd = abs(np.max(d))

    pe = maxv * dx / maxd
    if (np.abs(pe) >= 3) or (maxd == 0):
        dt = dx / maxv
        d = d * 0
    elif (np.min(np.abs(pe)) >= 0.1) or (maxd == 0):
        dt = 1 / (2 * maxd / (dx ** 2) + (maxv / dx))
    else:
        dt = (dx * dx) / (2 * maxd)
    tfactor = k['tfactor']
    dtini = dt
    dt = dt / tfactor

    #CONSTANTES
    ki = np.where(v > 0, 0, 1)
    kr = np.where(v < 0, 0, 1)

    for var in variables:
        Cout['cout_{}'.format(var)] = C['c_{}'.format(var)]

    # range(int(dtini / dt)) determina el número de nodos temporales necesarios para llegar t + dt de forma estable
    for i in range(int(dtini / dt)):

        caudales = Caudales[0:, 1:] / (Caudales[0, 1:] + Caudales[0:, 1:])

        reactions = fn_reactions(dt=dt, k=k, D=D, **C)

        for var in variables:

            c_Var = 'c_{}'.format(var)
            cout_Var = 'cout_{}'.format(var)
            s_Var = 'S_{}'.format(var)

            adv = fn_advection(v, C[c_Var], (dt / dx), ki, kr)
            diff = fn_diffusion(d, C[c_Var], (dt / dx ** 2))
            reac = reactions[var]

            if var != 'ALK':
                Cout[cout_Var][1:-1] = C[c_Var][1: -1] + adv + diff + reac + (
                    (S[s_Var][1:-1] - C[c_Var][1:-1]) * caudales[1:-1, 1]
                )
            else:
                Cout[cout_Var][1:-1] = C[c_Var][1:-1] + adv + diff + reac + ((S[s_Var][1:-1]) * caudales[1:-1, 1])

            if var == 'T':
                # Se resta diff
                Cout[cout_Var][1:-1] -= diff

        for var in variables:
            C['c_{}'.format(var)] = Cout['cout_{}'.format(var)]
            Cout['cout_{}'.format(var)][-1] = Cout['cout_{}'.format(var)][-2]

    return C, dt

def show_graphics(C, ct, Cout, mcon, salto=3600):

    fig, ax = plt.subplots(5, 3, sharex=True)
    fig.add_subplot("111", frameon=False)
    fig.canvas.set_window_title('Graficas de Tiempo.')

    x_data = ct[1::3600]
    datos = (dato for dato in config.TITULOS_GRAFICAS_PUNTO.items())

    for i in range(5):
        for j in range(3):
            k, v = next(datos)
            plot(ax[i][j], v, [x_data, mcon[k][1::salto, -1]])

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    plt.subplots_adjust(hspace=0.5)
    plt.grid(False)

    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.xlabel(config.X_LABEL_GRAFICAS_TIEMPO, fontsize=15)
    plt.ylabel(config.Y_LABEL_GRAFICAS_ESPACIO['T'], fontsize=15)

    fig.show()

    c_x = C['wd'][:, 0]

    fig2, ax2 = plt.subplots(5, 3, sharex=True)
    fig2.add_subplot(111, frameon=False)
    fig2.canvas.set_window_title('Graficas de espacio.')

    # Graficas en el espacio
    datos = (dato for dato in config.TITLULOS_GRAFICAS_ESPACIO.items())
    for i in range(5):
        for j in range(3):
            k, v = next(datos)
            plot(ax2[i][j], v, [c_x, Cout['c_{}'.format(k)]])

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    plt.subplots_adjust(hspace=0.5)
    plt.grid(False)

    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useOffset=True)

    plt.xlabel(config.X_LABEL_GRAFICAS_ESPACIO, fontsize=15)
    plt.ylabel(config.Y_LABEL_GRAFICAS_ESPACIO['T'], fontsize=15)

    fig2.show()

def save_graphics(C, ct, Cout, mcon, salto=3600):
    x_data = ct[1::3600]

    plt.figure('tmp')

    # Gráficas de tiempo
    for k, titulo in config.TITULOS_GRAFICAS_PUNTO.items():
        save_plot(
            plt,
            titulo,
            config.X_LABEL_GRAFICAS_TIEMPO,
            config.Y_LABEL_GRAFICAS_ESPACIO[k],
            [x_data, mcon[k][1::salto, -1]],
            directorio_salida
        )

    c_x = C['wd'][:, 0]
    # Gráficas de espacio
    for k, titulo in config.TITLULOS_GRAFICAS_ESPACIO.items():
        save_plot(
            plt,
            titulo,
            config.X_LABEL_GRAFICAS_ESPACIO,
            config.Y_LABEL_GRAFICAS_ESPACIO[k],
            [c_x, Cout['c_{}'.format(k)]],
            directorio_salida
        )

def print_state_variables(variables, to_optimize):
    #to_optimize = ['ko2', 'kdbo', 'kDQO']
    print("\tVariables to OPTIMIZE: ")
    for var in to_optimize:
        print( "\t\t{} = {}".format(var, variables[var]) )


def run(archivo_entrada, tiempo, directorio_salida, variables, show, export,tiempoTotal, epochs=1, estabaEntrenando =True):
    start_time = datetime.datetime.now()
    print("The process has started: {}".format(getTime( start_time ) ))
    for epoch in range( 1, epochs+1):
        print("------------------------------------------------------Epoch {}".format( epoch ))

        # Numero de pasos en el tiempo a ejecutar
        nt = tiempo
        ct = (np.arange(1, nt))

        C = _read_config_file(archivo_entrada)

        # Discretizacion en el espacio
        dx = C['wd'][1, 0] - C['wd'][0, 0]

        # velocidad del agua en cada punto de monitoreo
        va = C['wv'][:, 1]
        # coeficiente de difusión en cada punto de monitoreo
        cd = np.zeros(len(va)) + variables['Diff']
        v = np.zeros(len(va)) + np.mean(C['wv'])
        D = np.mean(C['wd'])

        # Condiciones de Frontera
        bc = dict()

        for k, col in config.BC_COLUMNS.items():
            bc[k] = C['bc'][:, col]

        kcondt = 1.92
        bc['T'] = bc['T'] + 273.15
        bc['pH'] = 10 ** (-1 * bc['pH'])

        # Condiciones Iniciales
        Ci = dict()
        for k, col in config.BC_COLUMNS.items():
            Ci['ci_{}'.format(k)] = C['ic'][:, col]

        Ci['ci_T'] = Ci['ci_T'] + 273.15
        Ci['ci_pH'] = 10 ** (-1 * Ci['ci_pH'])

        mcon = dict()
        for var in config.VARIABLES:
            mcon[var] = np.empty((nt, np.size(Ci['ci_{}'.format(var)], axis=0)))
            mcon[var][0, :] = Ci['ci_{}'.format(var)]

        for var in config.VARIABLES:
            C['S{}'.format(var)] = C['S{}'.format(var)][:, 1:]

        Cout = dict()
        #print("Total Iterations = {}".format(nt))
        for i in range(1, nt):
            sys.stdout.write("\r\tDoing iteration {}, {:.2f}% Completed ".format(i, i/nt*100))

            muestra = int(i / 3600)
            for k in config.BC_COLUMNS.keys():
                Ci['ci_{}'.format(k)][0] = bc[k][muestra]

            S = dict()
            for var in config.VARIABLES:
                S['S_{}'.format(var)] = C['S{}'.format(var)][:, muestra]

            #  Evolución de la concentración para t + dt
            Cout, paso_t = calidad_explicito(D, dx, Ci, S, v, cd, C['Caudales'], variables)

            # Se guardan las concentraciones del momento t+dt
            for var in config.VARIABLES:
                mcon[var][i, :] = Cout['c_{}'.format(var)]

            # Actualizar condición inicial
            for var in config.VARIABLES:
                Ci['ci_{}'.format(var)] = Cout['c_{}'.format(var)]

        mconConduct = kcondt * mcon['TDS']
        mcon['T'] = mcon['T'] - 273.15
        mcon['pH'] = (np.log10(mcon['pH'])) * (-1)
        Cout['c_pH'] = (np.log10(Cout['c_pH'])) * (-1)


        #print("Guardando datos de salida...")
        #print( "Shape OD array = {}".format( str(mcon['pH'].shape) ))
        #print( "Shape OD array = {}".format( str(mcon['pH'][0::3600, :].shape) ))
        book = xlwt.Workbook()
        for var in config.VARIABLES:
            """
                take data each 3600 samples mcon[0::3600, :]
            """
            data = mcon[var][0::3600, :]
            data = np.vstack([data, data.mean(axis=0)])
            save_sheet(book, var, data)

        save_sheet(book, 'Conduct', mconConduct[0::3600, :])

        used_vars(book, variables)
        name = join(directorio_salida, "Resultados.xlsx")
        book.save(name)
        """
            Compute error
        """
        errores, types, sign_dependency, to_optimize = computeError(name)
        """
            Here update the values according the error, {gradiente descendente}
        """

        learning_rate = 1
        for var in to_optimize:
            variables[var] += types[var]*errores[var]*variables[var]*learning_rate*sign_dependency[var]*-1

        print_state_variables( variables, to_optimize)


    end_time = datetime.datetime.now()
    print("\nThe process has finished at: {}".format(getTime( end_time ) ))
    elapsed_time = end_time - start_time
    elapsed_time = str(datetime.timedelta(seconds=elapsed_time.total_seconds()))
    print("Total Time: {}".format(elapsed_time))
    if( estabaEntrenando ):
        print("Final Run: ")
        run(archivo_entrada, tiempoTotal, directorio_salida, variables, show, export,tiempoTotal, epochs=3, estabaEntrenando=False)
    else:
        book = xlwt.Workbook()
        used_vars(book, variables)
        name = "FOptimize/Variables.xlsx"
        book.save(name)
        print("El proceso ha finalizado.")


def cargar_variables():
    data = pd.read_excel("FOptimize/Variables.xlsx")
    variables = dict()
    for row  in data.iterrows():
        name = row[1]["variable"]
        value = row[1]["valor"]
        variables[name] = value
    return variables


if __name__ == '__main__':
    archivo_entrada = 'Prueba_CAR.xls'
    horasTraining = 2
    horasReal = 24
    tiempoTraining = 60 * 60 * horasTraining
    tiempoTotal = 60 * 60 * horasReal
    directorio_salida = './salida/'
    show = False
    export = False

    variables = cargar_variables()
    """
    variables = {'Da': 1.6296e-07, 'ko2': 0.0002787, 'cs': 8.0, 'knh3': 5.787e-05, 'ksnh3': 1.15741e-06,
        'alfa_nh3': 2.0, 'kdbo': 1.1574e-06, 'ks': 0.4, 'alfa_no2': 1.1, 'ksod': 1.15e-06,
        'knt': 2.3148e-06, 'NT': 0.5, 'kno2': 1.1574e-05, 'kno3': 1.1574e-06, 'kDQO': 1.1574e-06,
        'kTDS': 2e-08, 'A': 0.001, 'alfa_1': 0.175, 'miu': 2.31481e-05, 'F': 0.1, 'kTC': 2.31481e-06,
        'teta_TC': 0.9, 'kEC': 6.31481e-06, 'teta_EC': 0.8, 'Jdbw': 4.62963e-08, 'qtex': 3.47222e-05,
        'kN': 1.1574e-07, 'kH': 1.1574e-05, 'kOH': 8.64e-10, 'fdw': 0.5, 'kf': 1.1574e-07,
        'kb': 1.1574e-08, 'kv': 1.1574e-08, 'Cg': 1e-05, 'Henry': 0.001, 'R': 8.205746e-05,'T': 295.15,
        'alfa_2': 0.5, 'resp': 0.25, 'kPorg': 1.1574e-06, 'kPsed': 1.574e-06, 'sigma2': 8.587e-05,
        'Ws': 0.05, 'Rs': 0.1, 'Rp': 0.1, 'k': 0.58, 'den': 997.3, 'Cp': 4148.1, 'teta_DBO': 1.01,
        'teta_NH3': 1.01, 'teta_NO2': 1.01, 'teta_DQO': 1.01, 'teta_NT': 1.01, 'teta_NO3': 1.01,
        'Kw': 1e-14, 'K1': 4.5e-07, 'K2': 4.7e-11, 'Vv': 5.787e-06, 'As': 1.0, 'CO2S': 1.23e-05,
        'Wrp': 1.808e-09, 'FrH': 0.0172, 'Diff': 5.0, 'As1': 1.0, 'Jsn': 145.0, 'sbc': 5.67e-08,
        'Tair': 17.0, 'Aair': 0.6, 'eair': 14.3, 'RL': 0.03, 'Uw': 3.0, 'es': 11.5, 'tfactor': 1.0}
    """

    run(archivo_entrada, tiempoTraining, directorio_salida, variables, show, export, tiempoTotal)
