# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginTeste
                                 A QGIS plugin
 Plugin para add procssings teste
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-02
        copyright            : (C) 2021 by Pedro Martins
        email                : pedromartins.souza@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Pedro Martins'
__date__ = '2021-03-02'
__copyright__ = '(C) 2021 by Pedro Martins'


def classFactory(iface):  # pylint: disable=invalid-name
    """Load PluginTeste class from file PluginTeste.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .plugin_alg import PluginAlg
    return PluginAlg()