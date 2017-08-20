=======================
Componentes gráficos
=======================

Para crear componentes gráficos se realiza el siguiente proceso:

1. Diseñar el componente con el software QtDesigner4.
2. Guardar el diseño del componente en la carpeta ui.
3. Generar el módulo de python del componente a partir del archivo ui.
4. Extender el código python del componente, para agregarle la funcionalidad deseada.

Generar el módulo de python
##############################
Para generar el módulo de python a partir del archivo *.ui* del componente gráfico, es necesario instalar las dependencias de desarrollo de PyQt4 las cuales incluyen la utilidad **pyui4** que se utiliza para generar el código de python de un archivo .ui.

En linux, el siguiente comando realizará el proceso que se acabó de describir.

::

    pyui4 ui/componente.ui -o dialogs/componente.py

Extender el código del componete gráfico
###########################################

Una vez realizado el proceso de generar el código del componente gráfico, el resultado de este es un módulo de python, el cuál contiene una *clase* que representa el componente gráfico que se acabó de crear. Para extender la funcionalidad de este componente, es neceario heredar de la clase del módulo, e implementar la funcionalidad deseada.
