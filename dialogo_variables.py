# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui', 'dialogo_variables_base.ui'))

RUTA_ARCHIVO_VARIABLES = os.path.join(
    os.path.dirname(__file__), 'data', 'variables.txt')

RUTA_ARCHIVO_VARIABLES_LOCK = os.path.join(
    os.path.dirname(__file__), 'data', 'variables.lock.txt')

siglas = ['Da', 'ko2', 'cs', 'knh3', 'ksnh3', 'alfa_nh3',
	'kdbo', 'ks', 'alfa_no2', 'ksod', 'knt', 'NT', 'kno2', 'kno3',
    'kDQO', 'kTDS', 'A', 'alfa_1', 'miu', 'F', 'kTC', 'teta_TC',
    'kEC', 'teta_EC', 'Jdbw', 'qtex', 'kN', 'kH', 'kOH', 'fdw', 
    'kf', 'kb', 'kv', 'Cg', 'Henry', 'R', 'T', 'alfa_2', 'resp',
    'kPorg', 'kPsed', 'sigma2', 'Ws', 'Rs', 'Rp', 'k', 'den', 'Cp', 
    'teta_DBO', 'teta_NH3', 'teta_NO2', 'teta_DQO', 'teta_NT', 'teta_NO3', 
    'Kw', 'K1', 'K2', 'Vv', 'As', 'CO2S', 'Wrp', 'FrH', 'Diff',
    'As1', 'Jsn', 'sbc', 'Tair', 'Aair', 'eair', 'RL', 'Uw', 'es', 'tfactor']

class VarsDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(VarsDialog, self).__init__(parent)
        self.setupUi(self)
        self.dic = {
            'Da': self.Da, 'ko2': self.ko2, 'cs': self.cs, 
            'knh3': self.knh3, 'ksnh3': self.ksnh3, 'alfa_nh3': self.alfa_nh3 ,
            'kdbo': self.kdbo, 'ks': self.ks, 'alfa_no2': self.alfa_no2, 
            'ksod': self.ksod, 'knt': self.knt, 'NT': self.NT, 'kno2': self.kno2, 
            'kno3': self.kno3, 'kDQO': self.kDQO, 'kTDS': self.kTDS, 'A': self.A,
            'alfa_1': self.alfa_1, 'miu': self.miu, 'F': self.F, 'kTC': self.kTC, 
            'teta_TC': self.teta_TC, 'kEC': self.kEC, 'teta_EC': self.teta_EC, 
            'Jdbw': self.Jdbw, 'qtex': self.qtex, 'kN': self.kN, 'kH': self.kH, 
            'kOH': self.kOH, 'fdw': self.fdw, 'kf': self.kf, 
            'kb': self.kb, 'kv': self.kv, 'Cg': self.Cg, 'Henry': self.Henry, 
            'R': self.R, 'T': self.T, 'alfa_2': self.alfa_2, 'resp': self.resp,
            'kPorg': self.kPorg, 'kPsed': self.kPsed, 'sigma2': self.sigma2, 'Ws': self.Ws, 
            'Rs': self.Rs, 'Rp': self.Rp, 'k': self.k, 'den': self.den, 'Cp': self.Cp,
            'teta_DBO': self.teta_DBO, 'teta_NH3': self.teta_NH3, 'teta_NO2': self.teta_NO2, 
            'teta_DQO': self.teta_DQO, 'teta_NT': self.teta_NT, 'teta_NO3': self.teta_NO3, 
            'Kw': self.Kw, 'K1': self.K1, 'K2': self.K2, 'Vv': self.Vv, 'As': self.As, 
            'CO2S': self.CO2S, 'Wrp': self.Wrp, 'FrH': self.FrH, 'Diff': self.Diff,
            'As1': self.As1 , 'Jsn': self.Jsn , 'sbc': self.sbc , 'Tair': self.Tair , 
            'Aair': self.Aair , 'eair': self.eair , 'RL': self.RL , 'Uw': self.Uw , 'es': self.es,
            'tfactor': self.tfactor }
        
        # Agregar validador
        validator = QtGui.QDoubleValidator()
        for k, e in self.dic.iteritems():
            e.setValidator(validator)

        # Agregar valores iniciales
        valores_iniciales = self.leerVariables()
        for k, v in valores_iniciales.iteritems():
            self.dic[k].setText(v)

        self.pushButtonRestablecer.clicked.connect(self.reset)

    def reset(self):
        values = {}
        with open(RUTA_ARCHIVO_VARIABLES_LOCK, 'r') as file:
            for line in file:
                k, v = line.split()
                values[k] = v

        with open(RUTA_ARCHIVO_VARIABLES, 'w') as file:
            for k, v in values.iteritems():
                file.write("%s %s\n" % (k, str(v)))
                self.dic[k].setText(v)

    def getContaminantes(self):
        '''
            Retorna el diccionario con todos los
            contaminantes y sus valores.
        '''
        cont = {}
        for k, v in self.dic.iteritems():
            cont[k] = float(v.text())
        return cont

    @staticmethod
    def leerVariables():
        '''
            Lee los contaminantes del archivo en el que
            se almacenan.

            :returns: Diccionario cuya clave es el contaminante
            y el valor, en formato string.
        '''
        values = {}
        with open(RUTA_ARCHIVO_VARIABLES, 'r') as file:
            for line in file:
                k, v = line.split()
                values[k] = v
        return values

    def guargarContaminantes(self, cont):
        '''
            En caso de que se haya actualizado algún
            contaminante, se actualiza el archivo.
        '''
        cond = False
        saved = self.leerVariables()

        for k, v in saved.iteritems():
            if v != str(cont[k]):
                cond = True
                break

        if not cond: return 

        with open(RUTA_ARCHIVO_VARIABLES, 'w') as file:
            for k, v in cont.iteritems():
                file.write("%s %s\n" % (k, str(v)))
