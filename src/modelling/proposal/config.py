
VARIABLES = ['T', 'OD', 'DBO', 'NH3', 'NO2', 'NO3', 'DQO', 'TDS', 'EC', 'TC',
             'GyA', 'Porg', 'Pdis', 'pH', 'ALK', 'SS', 'TSS']

SHEET_NAMES = dict(
    wd='WD',
    sl='SL',
    wv='WV',
    bc='BC',
    ic='IC',
    ST='ST',
    SOD='SOD',
    SDBO='SDBO',
    SNH3='SNH4',
    SNO2='SNO2',
    SNO3='SNO3',
    STDS='STDS',
    SGyA='SGyA',
    SDQO='SDQO',
    SPdis='SPdis',
    SPorg='SPorg',
    SEC='SEC',
    STC='STC',
    STSS='STSS',
    SSS='SSS',
    SpH='SpH',
    SALK='SALK',
    Caudales='Caudales'
)

TITULOS_GRAFICAS_PUNTO = dict(
    T='Evalucion T en punto final',
    OD='Evalucion OD en punto final',
    DBO='Evalucion DBO en punto final',
    NH3='Evalucion NH3 en punto final',
    NO2='Evalucion NO2 en punto final',
    NO3='Evalucion NO3 en punto final',
    DQO='Evalucion DQO en punto final',
    TDS='Evalucion TDS en punto final',
    EC='Evalucion EC en punto final',
    TC='Evalucion TC en punto final',
    GyA='Evalucion Grasas y Aceites en punto final',
    Porg='Evalucion P org en punto final',
    Pdis='Evalucion P disuelto en punto final',
    pH='Evalucion del pH en punto final',
    ALK='Evalucion Alcanilidad en punto final',
)

TITLULOS_GRAFICAS_ESPACIO = dict(
    T='Evalucion T en el espacio',
    OD='Evalucion OD en el espacio',
    DBO='Evalucion DBO en el espacio',
    NH3='Evalucion NH3 en el espacio',
    NO2='Evalucion NO2 en el espacio',
    NO3='Evalucion NO3 en el espacio',
    DQO='Evalucion DQO en el espacio',
    TDS='Evalucion TDS en el espacio',
    EC='Evalucion EC en el espacio',
    TC='Evalucion TC en el espacio',
    GyA='Evalucion Grasas y Aceites en el espacio',
    Porg='Evalucion P organico en el espacio',
    Pdis='Evalucion P disuelto en el espacio',
    pH='Evalucion del pH en espacio',
    ALK='Evalucion Alcanilidad en espacio',
)

X_LABEL_GRAFICAS_ESPACIO = 'Distancia(m)'
Y_LABEL_GRAFICAS_ESPACIO = dict(
    T='Concentracion (mg/L)',
    OD='Concentracion (mg/L)',
    DBO='Concentracion (mg/L)',
    NH3='Concentracion (mg/L)',
    NO2='Concentracion (mg/L)',
    NO3='Concentracion (mg/L)',
    DQO='Concentracion (mg/L)',
    TDS='Concentracion (mg/L)',
    EC='Concentracion (mg/L)',
    TC='Concentracion (mg/L)',
    GyA='Concentracion (mg/L)',
    Porg='Concentracion (mg/L)',
    Pdis='Concentracion (mg/L)',
    pH='pH',
    ALK='CaCO3',
)

X_LABEL_GRAFICAS_TIEMPO = 'Tiempo(s)'

BC_COLUMNS = dict(
    T=14,
    OD=1,
    DBO=2,
    NH3=3,
    NO2=4,
    NO3=5,
    DQO=9,
    TDS=6,
    EC=12,
    TC=13,
    GyA=7,
    Porg=10,
    Pdis=11,
    TSS=15,
    SS=16,
    pH=17,
    ALK=18
)
