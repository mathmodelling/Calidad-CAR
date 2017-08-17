===========================
Agregar recursos al plugin
===========================

********
Iconos
********

Para agregar, o modificar los iconos del plugin, es necesario modificar el archivo *resources.qrc* y agregar el icono en la etíqueta *qrsource*. Ejemplo:

::

    <RCC>
        <qresource prefix="/plugins/CalidadCAR" >
            <file>icons/icon.png</file>
            <file>icons/layers-icon.png</file>
            <file>icons/csv-join-icon-add.png</file>
            <file>icons/add-section-icon.png</file>
            <file>icons/refresh-icon.png</file>
            <file>icons/start-icon.png</file>
        </qresource>
    </RCC>

Como se puede ver en el archivo *resources.qrc*, cada etíqutea <file> contiene la ruta de un icono.

Luego de realizar cualquier cambio en el archivo *resources.qrc* es necesario generar el archivo *resources.py*. Esto se puede hacer con el siguiente comando:

::

    pyrcc4 -o resources.py resources.qrc

Para poder usar la herramienta *pyrcc4* es necesario instalar las herramientas de desarrollador de PyQt4
