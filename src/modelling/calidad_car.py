# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import str
from builtins import range
import numpy as np
import time
import datetime as dtm
import matplotlib.pyplot as plt

__author__ = 'Profesor Efraín Domínguez Calle, PhD.'
__copyright__ = "Copyright 2017, Mathmodelling"
__credits__ = ["Efraín Domínguez Calle"]
__license__ = "Uso Libre"
__version__ = "0.0"
__maintainer__ = "Efraín Antonio Domínguez Calle"
__email__ = 'edoc@marthmodelling.org'
__status__ = "En desarrollo"

# Modelo unidimensional para la simulación de migración de contaminantes en corrientes superficiales
# Versión del código: 0.0 - Julio del 2017
# Se debe usar en la interfase gráfica del sistema de modelación Calidad-Car pero también se puede usar de
# forma independiente...


def calidad_explicito(ci, v, d):
    """
    Esta función modela la transición de la concentración del momento t al momento t + dt para todos los 
    nodos espaciales de la corriente superficial
    
    :param ci: matrix (bidimensional) de concentración inicial en el canal y su respectiva distancia x la concentración 
    va en g/m3, la distancia en metros
    :param v: vector de velocidad promedio del agua en m/s, tiene las velocidades promedio para cada sección
     y para cada momento de tiempo
    :param d: vector de coeficiente de difusión
    :return: c, dt: la concentración del contaminante en todos los nodos x para el momento de tiempo t + dt y el valor 
    de dt que cumple la condición de estabilidad de Courant o CFL
    
    """
    # dx - paso de cálculo longitudinal en metros, se supone dx = constante
    dx = ci[1, 0] - ci[0, 0]
    # dx = ci[1:, 0] - ci[0:-1, 0]
    c = ci[:, 1]
    maxv = abs(np.max(v))
    maxd = abs(np.max(d))
    pe = maxv * dx / maxd
    if (np.min(np.abs(pe)) >= 3) or (maxd == 0):
        dt = dx / maxv
        d = d * 0
        # fix_print_with_import
        print("Se desconectó la Difusión, el número de peclet es: %s. Courant es igual a: %s. El paso en el " \
              "tiempo es de: %s segundos" % (round(pe, 2), str(maxv * (dt / dx)), dt))
    else:
        dt = (dx * dx) / (2 * maxd)
        # fix_print_with_import
        print('Se calcula advección y difusión, el número de peclet es: %s. Courant es igual a: %s. El paso en el ' \
              'tiempo es de: %s segundos' % (round(pe, 2), str(maxv * (dt / dx)), dt))

    # tfactor es un factor multiplicador del numero de nodos en el tiempo para llegar de t a t + dt, tfactor >= 1,
    # se recomienda aumentarlo de 10 en 10 {10, 100, 1000, 10000... }
    tfactor = 1.0
    # Se guarda el dt inicial como dtini
    dtini = dt
    # Se ajusta el dt según tfactor, dt se hace más pequeño tfactor-veces
    dt = dt / tfactor
    ki = np.where(v > 0, 0, 1)
    kr = np.where(v < 0, 0, 1)
    # range(int(dtini / dt)) determina el número de nodos temporales necesarios para llegar t + dt de forma estable
    for i in range(int(dtini / dt)):
        cout = np.zeros(len(c))
        cout[0] = c[0]
        cout[-1] = c[-1]
        adv = -((ki[2:] * v[2:] * c[2:] - ki[1:-1] * v[1:-1] * c[1:-1]) * (dt / dx) +
                (kr[1:-1] * v[1:-1] * c[1:-1] - kr[0:-2] * v[0:-2] * c[0:-2]) * (dt / dx))
        dif = 0.5 * (d[2:] * c[2:] - 2 * d[1:-1] * c[1:-1] + d[0:-2] * c[0:-2]) * (dt / dx ** 2)
        cout[1:-1] = c[1:-1] + adv + dif
        c = cout
    return c, dt


def ejemplo_de_uso_00():
    """
    Ejemplo 0.0: 
    Un canal de l = 100 metros de largo con puntos de monitoreo cada dx=10. La velocidad medida en los puntos de 
    monitoreo v = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], el coeficiente de difusión es d = [1.5, 1.5, 1.5, 
    1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]. la concentración inicial es [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    :return: None
    
    """
    # Numero de pasos en el teimpo a ejecutar
    nt = 20
    # Número de nodos espaciales
    nx = 10
    # Condición inicial
    c_i = np.array([[0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T
    # Condición de frontera
    c_f = np.arange(0.0, nt + 1.0)
    amplitud, fase, frecuencia, z = 1.0, 0.0, 0.35, 1.0
    c_f = amplitud * np.sin(frecuencia * c_f + fase) + z
    # velocidad del agua en cada punto de monitoreo
    va = np.zeros(10) + 0.5
    # coeficiente de difusión en cada punto de monitoreo
    cd = np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])
    mcon = np.empty((nt + 1, np.size(c_i, axis=0)))
    # Asignación de condición inicial
    mcon[0, :] = c_i[:, 1]
    for i in range(1, nt):
        # Asignación de condición de frontera. Se hace cambiando primer valor de c_i
        c_i[0, 1] = c_f[i]
        # Evolución de la concentración para t + dt
        con, t_step = calidad_explicito(c_i, va, cd)
        # Se guardan las concentraciones del momento t+dt
        mcon[i, :] = con
        # Actualizar condición inicial
        c_i[:, 1] = con
    return mcon, t_step


def grafica(cs, dt, dx, flag=0, scol=0, srow=0, hi=time.strftime("%d/%b/%Y %H:%M:%S", time.localtime())):
    """
    Esta función grafica la evolucipon de la concentración  en una sección del tramo de modelación
    :type scol: int
    :param cs: Es el arreglo resultado de la modelación desde el momento inicial 't' hasta el momento 't+nt*dt'. 
    Las filas representan tiempo, las columnas el espacio. nt es el número de filas
    :param hi: Es la hora inicial de referencia para la modelación, ejemplo '20/08/2017 12:30:00'
    :param dt: Es el paso de calculo en el tiempo
    :param dx: Es el paso de calculo en el espacio
    :param flag: establece ploteo por tiempo flag = 0 o por espacio flag = 1
    :param scol: es un entero que establece el momento de tiempo a plotear (selected by column)
    :param srow: es un entero que establece la sección del río a plotear (selected by row)
    :return: None
    """
    ncols = np.size(cs, axis=1)
    nrows = np.size(cs, axis=0)
    # fix_print_with_import
    print('nrows: %s, ncols: %s, cs.shape: %s ' % (nrows, ncols, cs.shape))
    # Convertir hora inicial de referencia -hi- en tiempo estructurado con tupla de 9 elementos
    # fix_print_with_import
    print('hi:', hi)
    hi_structime = time.strptime(hi, "%d/%b/%Y %H:%M:%S")
    # Convertir el tiempo estructurado en segundos desde la epoca 12:00am, January 1, 1970(epoch)
    hi_secs = time.mktime(hi_structime)
    # fix_print_with_import
    print('hi_secs:', hi_secs)
    # fechas = pd.date_range(hi, periods=nrows, freq=str(int(dt)) + 'S')
    tiempo = dt * nrows - dt
    fechas = [dtm.datetime.fromtimestamp(i) for i in np.arange(hi_secs, hi_secs + tiempo + dt, dt)]

    # absc - abscisado
    absc = np.arange(0, ncols * dx, dx)
    # print 'fechas:', fechas.shape, 'abscisas:', absc.shape
    # df = pd.DataFrame(cs, index=fechas, columns=absc)
    if flag == 0:
        # df[scol].plot()
        plt.plot(fechas, cs[:, 7], 'k-.')
        plt.title(u'Distancia:' + str(scol))
        plt.xlabel(u'Tiempo, $[s]$')
        plt.ylabel(u'Concentración, $[g/m^3]$')
    else:
        # df.iloc[srow].plot()
        plt.plot(absc, cs[srow, :])
        plt.title(u"Momento de tiempo - " + str(srow))
        plt.xlabel(u"Distancia en metros")
        plt.ylabel(u'Concentración, $[g/m^3]$')
    plt.show()
    return


if __name__ == "__main__":
    # Número de nodos temporales
    paso_x = 10
    np.set_printoptions(precision=2)
    inicio = dtm.datetime.fromtimestamp(time.time())
    # fix_print_with_import
    print('Estoy comenzando a las ', inicio.strftime('%Y-%m-%d %H:%M:%S'))
    sol, paso_t = ejemplo_de_uso_00()
    hora_inicial = '20/08/2017 12:30:00'
    # fix_print_with_import
    print(grafica(sol, paso_t, paso_x, srow=11, scol=80, flag=1))
    final = dtm.datetime.fromtimestamp(time.time())
    # fix_print_with_import
    print('Termine a las %s ', final.strftime('%Y-%m-%d %H:%M:%S'))
    # fix_print_with_import
    print('Gasté: ', final - inicio)
