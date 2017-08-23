# -*- coding: utf-8 -*-

from PyQt4.QtGui import QColor
from qgis.core import ( QgsMapLayerRegistry,
                        QgsVectorLayer,
                        QgsRasterLayer)

def get_layer(layer_name):
    """ Busca una capa por nombre en el registro de capas de qgis.

    :param layer_name: Nombre de la capa a buscar.
    :type layer_name: str

    :returns: La primera capa cuyo nombre coincida con layer_name, en caso de que no exista se retorna None.
    :rtype: QgsMapLayer
    """
    try:
        return QgsMapLayerRegistry.instance().mapLayersByName(layer_name)[0]
    except IndexError:
        return None

def remove_layers(layers):
    """ Elimina capas del registro de capas de qgis.

    :param layers: Capas que se van a eliminar.
    :type layer_name: Lista QgsMapLayers
    """
    for layer in layers:
        QgsMapLayerRegistry.instance().removeMapLayer(layer)

def add_layers(layers):
    """ Agrega capas al registro de capas de qgis.

    :param layers: Capas que se van a agregar.
    :type layer_name: Lista QgsMapLayers
    """
    for layer in layers:
        QgsMapLayerRegistry.instance().addMapLayer(layer)

def load_raster_layer(path, name):
    """Carga una capa rasterizada.

    :param path: Ruta de la capa que se va a cargar.
    :type path: str

    :param name: Nombre de la capa que se va a cargar, este nombre será el identificador de la capa.

    :returns: Capa rasterizada en caso de que sea valida, de lo contrario se retorna None.
    :rtype: QgsRasterLayer
    """
    rlayer = QgsRasterLayer(path, name)
    if not rlayer.isValid():
        return None
    return rlayer

def load_vector_layer(path, name, color = (0, 0 , 0)):
    """Carga una capa vectorizada.

    :param path: Ruta de la capa que se va a cargar.
    :type path: str

    :param name: Nombre de la capa que se va a cargar, este nombre será el identificador de la capa.

    :param color: Color que se la va a asignar a la capa
    :type color: Tupla de 3 elementos r, g, b

    :returns: Capa vectorizada en caso de que sea valida, de lo contrario se retorna None
    :rtype: QgsVectorLayer
    """
    layer = QgsVectorLayer(path, name, 'ogr')

    if not layer.isValid():
        return None

    # Cambiar el color del layer
    r, g, b = color
    symbol_layer = layer.rendererV2().symbols()[0].symbolLayer(0)
    symbol_layer.setColor(QColor(r, g, b))

    return layer
