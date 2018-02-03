Manual de usuario
==================

Calidad-CAR es una herramienta para modelar matemáticamente la calidad del agua en los ríos. Esta herramienta asume que el usuario tiene los resultados del modelado del movimiento del agua con la herramienta Hec-Ras.

Una vez instalado el plugin CalidadCAR, el usuario podrá ver la siguiente barra de herramientas:

.. image:: images/barra_herramientas.png

La cual contiene los siguientes procedimientos que el usuario podrá realizar:

1. `Cargar fondos`_.
2. `Crear el archivo de entrada`_.
3. `Cálcular`_.
4. `Limpiar`_.
5. `Configurar Variables`_.


*****************
Cargar fondos
*****************

Con esta acción el usuario puede cargar las capas que contienen la información necesaria para que se pueda aplicar el modelo matemático.
Para poder realizar esta operación el usuario tendrá que hacer click en el icono resaltado que se ve en la siguiente imagen.

.. image:: images/accion_cargar_fondos.png

La cual desplegará el siguiente dialogo en el que el usuario podrá buscar los diferentes archivos en su sistema de archivos, para cargar las capas.

.. image:: images/cargar_fondos_dialogo.png

Una vez seleccionadas todas las capas que el usuario deseé cargar, se desplegarán los diálogos correspondientes para solicitar el sistema de coordenadas de cada una de las capas que se van a cargar.

.. image:: images/cargar_fondo_crs.png

Una vez seleccionado el sistema de coordenadas de las capas que se van a cargar, estas se podrán visualizar en el canvas de QGIS, como se ve en la siguiente imagen, para visualizar directamente la capa de secciones, el usuario podrá hacer click en el icono resaltado en la siguiente imagen:

.. image:: images/enfocar_capa_secciones.png

En la siguiente imagen se puede ver el canvas de QGIS una vez el usuario ha realizado un acercamiento a la capa de secciones:

.. image:: images/capa_zoom.png

*****************************
Crear el archivo de entrada
*****************************

Este procedimiento consiste en crear un archivo de Excel (.xls) con una plantilla determinada, en el cuál el usuario podrá ingresar la información necesaria para poder realizar el modelado matemático de la información.

El usuario podrá realizar este procedimiento haciendo click en el icono resaltado en la siguiente imagen:

.. image:: images/accion_agregar_csv.png

En la siguiente imagen se puede ver el dialogo que le pedirá al usuario la información necesaria para generar el archivo de Excel.

.. image:: images/dialogo_cargar_imagen.png

.. note:: El dato del tiempo, y la ruta del archivo que se va a crear son los únicos datos requeridos en el diálogo de Crear el archivo de entrada.

.. note:: Este proceso se puede realizar únicamente si se ha cargado la capa de ejes y la capa de secciones.


**************
Cálcular
**************

Una vez el usuario tiene el archivo de Excel con el formato correcto, y con la información, el usuario podrá realizar este proceso haciendo click en el icono resaltado en la siguiente imagen:

.. image:: images/accion_calcular.png

En este diálogo el usuario tiene que buscar el archivo de Excel que contiene la información, seleccionar la carpeta en la que quiere que se guarden los archivos de salida, y por lo menos una de las dos opciones de salida.

.. image:: images/dialogo_cargar_archivo.png

Si el usuario quiere obtener información del proceso, podrá abrir el interprete de python haciendo click en el icono que se ve a continuación.

.. image:: images/accion_python.png

Una vez terminado el proceso, la salida será de acuerdo a lo que selecciono el usuario. Si selecciono la opción de **Abrir diálogo con las gráficas de salida**, se abrirán dos ventanas con las gráficas correspondientes. Y si selecciono **Exportar gráficas de salida**, estas se guardarán en la carpeta de salida que selecciono el usuario.

**************
Limpiar
**************

Al hacer click en el botón resaltado en la siguiente imagen el usuario limpiara el espacio de trabajo, cerrando las capas cargadas, en caso que deseé realizar el mismo proceso con capas diferentes.

.. image:: images/accion_limpiar.png

***********************
Configurar Variables
***********************

Haciendo click en el icono que se ve en la siguiente imagén el usuario podrá cambiar el valor de algunas de las variables necesarias para aplicar el modélo matemático.

.. image:: images/accion_vars.png

Tabla de Variables:

+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
| Símbolo    | Descripción                                                                                                    | Unidades         | Rango                 |
+============+================================================================================================================+==================+=======================+
|k           |Conductividad térmica del agua                                                                                  | J / (s * m * K)  | 0.580 - 0.615         |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Cp          |Capacidad calorífica del agua                                                                                   | J / (kg * K)     | 4170 - 4190           |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|p           |Densidad del agua                                                                                               | kg / m3          | 999.700 – 995.650     |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Cs          |Concentración de saturación de oxígeno a la temperatura del sistema                                             | mg / L           | 7 - 12                |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kDBO        |Constante de degradación de DBO                                                                                 |1 / día           | 0.02 – 0.5            |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|θDBO        |Coeficientes de Arrhenius para el ajuste de temperatura de la reacción de DBO                                   | -                | 1.02 – 1.09           |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ks          |Constante de media saturación de oxígeno disuelto requerida para la oxidación de la demanda química de oxígeno  |mg / L            | 0.1 - 1.5             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|KNH3        |Constante de reacción la transformación de amonio a nitrito                                                     |1/s               | 1 x 10-6 – 1.2 x 10-5 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|KNO2        |Constante de reacción la transformación de nitrito a nitrato                                                    |1/s               | 2 x 10-6 – 2.4 x 10-5 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|αNH3        |Consumos de oxígeno para la transformación de amonio a nitrito                                                  |mg O2/mg N        | 2.0 – 4.0             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|αNO2        |Consumo de oxígeno para la transformación de nitrito a nitrato                                                  |mg O2/mg N        | 1.0 - 1.14            |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ΘNH3        |Coeficientes de Arrhenius para el ajuste de temperatura de la reacción de amonio                                | -                | 1.0 – 1.1             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ΘNO2        |Coeficientes de Arrhenius para el ajuste de temperatura de la reacción de nitritos                              | -                | 1.0 – 1.1             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ΘNO3        |Coeficientes de Arrhenius para el ajuste de temperatura de la reacción de nitratos                              | -                | 1.0 – 1.1             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kSOD        |Cantidad de oxígeno necesitada por los sedimentos inminentes en el área de la unidad del fondo del río          | mg * m / (L * s) | 8 x 10-7 - 5 x 10-5   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Da          |Variación neta de oxígeno disuelto debido a la actividad de las algas                                           | mg / L * s       | 1 x 10-9 - 1 x 10-4   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ko2         |Coeficiente de re-aireación                                                                                     | 1 / s            | 4 x 10-6 - 2 x 10-5   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|KDQO        |Constante de degradación de DQO                                                                                 | 1 / s            | 1 x 10-6 - 3 x 10-6   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ΘDQO        |Coeficientes de Arrhenius para el ajuste de temperatura de la reacción de DQO                                   | -                | 1.0 – 1.5             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|αA          |Fracción de biomasa de las algas expresada en forma de nitrógeno                                                | gN / gC          | 0.175                 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|γ           |Tasa de respiración de las algas                                                                                | -                | 0.1 - 0.5             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kNT         |Transformación de nitrógeno orgánico a amonio                                                                   |1/día             | 0.05 - 0.5            |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kSNT        |Tasa de sedimentación de nitrógeno orgánico                                                                     |1/día             | 0.1 – 0.3             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Yresp       |                                                                                                                |-                 | 0.01 – 0.1            |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kNO3        |Constante de reacción la transformación de desnitrificación                                                     |1/s               | 1 x 10-7 - 2 x 10-6   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ϑ           |Fracción de fosforo en las algas                                                                                |gP / gC           | 0.0167                |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kP-Org      |Transformación de fosforo orgánico                                                                              |1/s               | 5 x 10-8 – 2.5 x 10-6 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kP-sed      |Tasa de sedimentación de Fosforo                                                                                |1/s               | 1 x 10-7 – 2.5 x 10-6 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ℵ           |Cantidad neta de fósforo disuelto debido a la actividad de algas y bentos                                       |gP/s              | 1 x 10-7 – 2.5 x 10-6 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kE.coli     |Tasa de decaimiento e coli                                                                                      |1/s               | 1 x 10-7 – 1.2 x 10-6 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ΘE.coli     |Factor de corrección de temperatura                                                                             | -                | 0.9 – 1.1             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|kTC         |Tasa de decaimiento Coliformes totales                                                                          | 1 / s            | 1 x 10-7 – 1.2 x 10-6 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|ΘTC         |Factor de corrección de temperatura                                                                             | -                | 0.9 – 1.1             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|fdw         |Fracción disuelta de grasas y aceites en la columna de agua                                                     | -                | 0 – 1                 |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Jdbw        |Flujo de difusión vertical entre la columna de agua y la capa de sedimentos                                     | mg·m/(L·s)       | 1 x 10-7 – 1 x 10-3   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|qt,ex       |Tasa de intercambio total del contaminante debido a la erosión de sedimentos y deposición                       | mg·m/(L·s)       | 3 x 10-6 – 1 x 10-3   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|KN          |Constante de reacción de hidrolisis neutra                                                                      | 1 / s            | (0.1 – 1000) x 10-6   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|KH          |Constante de reacción de hidrolisis catalizada por ácidos                                                       | L/mol·s          | (1 – 1000) x 10-4     |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|KOH         |Constante de reacción de hidrolisis catalizada por base                                                         | L/mol·s          | (1 – 100) x 10-3      |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Kf          |Constante de fotolisis                                                                                          | 1 / día          | 1 x 10-8 – 2 x 10-5   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Kb          |Constante de biodegradación                                                                                     | 1 / día          | 1 x 10-8 – 2 x 10-5   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Kv          |Constante de volatilización                                                                                     | 1 / día          | 1 x 10-8 – 2 x 10-5   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|H           |Constante de Henry                                                                                              | atm m3/mol       | 0.0005 – 0.01         |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|R           |Constante de los gases                                                                                          | atm·m3/mol·K     | 8.205746 x 10-5       |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Cg          |Concentración en la fase gaseosa de las grasas y aceites                                                        | mg /L            | (0.1 – 10) x 10-5     |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Kbas        |Constante de reacción ácido carbónico                                                                           |                  | 2.1 x 10-4            |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Kw          |Constante de equilibrio del agua                                                                                |                  | 1 x 10-14             |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|PCO2        |Presión parcial de saturación del dióxido en la atmosfera                                                       | atm              | 0.00039               |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|aco         |Factor de conversión estequiométrico| mol CO2/gO2                                                               |                  | 0.03125               |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|vv          |Coeficiente de trasferencia por volatilización                                                                  | m / s            | 1 x 10-6 - 1 x 10-4   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|As          |Área superficial volumétrica de interface aire-agua                                                             | m2 / m3          | -                     |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|CO2S        |Concentración de saturación de dióxido de carbono en agua                                                       | mol / L          | 1 x 10-5 - 5 x 10-5   |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|Wrp         |Carga neta de carbón debido a efectos de fotosíntesis y respiración                                             | mol / s          | 1 x 10-10 - 2 x 10-9  |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+
|FrH         |Fracción de Hidrógenos respecto a alcalinidad                                                                   | -                | 0.005 – 0.1           |
+------------+----------------------------------------------------------------------------------------------------------------+------------------+-----------------------+

.. note:: El plugin CalidadCAR viene con valores por defecto para todas las variables, y una vez el usuario cambie alguno de estos valores quedará guardado para futuros usos.

.. _enlace: https://drive.google.com/file/d/0B-rl9rYMVpHpaUh6X1FfLThxYkU/view?usp=sharing
.. _vídeo: https://www.youtube.com/watch?v=5JpgidErg-E
