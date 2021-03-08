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
"""

__author__ = 'Pedro Martins'
__date__ = '2021-03-02'
__copyright__ = '(C) 2021 by Pedro Martins'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from qgis.core import(QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProject,
                       QgsMapLayer,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform,
                       QgsProject,
                       QgsPointXY,
                       QgsAbstractFeatureSource,
                       QgsExpression,
                       QgsVectorLayer,
                       QgsField,
                       QgsExpressionContext,
                       QgsExpressionContextScope,
                       QgsAuxiliaryStorage,
                       QgsPropertyDefinition,
                       QgsFeature,
                       QgsApplication
                       )
from .provider import Provider
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
#from qgis import processing
from qgis.utils import iface
#cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
'''
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from pathlib import Path
'''

class PluginAlg(object):

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
