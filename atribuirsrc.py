# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
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
                       QgsProcessingParameterCrs,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterBoolean
                       )
from qgis import processing

class AtribuirSRC(QgsProcessingAlgorithm):

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AtribuirSRC()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'atribui_src'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Atribuir SRC')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Missoes')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'missoes'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("O algoritmo atribui um SRC definido pelo usuario a camadas cujo SRC nao estava definido")
    
    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterCrs(
                'INPUT',
                self.tr('SRC padrao')
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                'InpLayers',
                self.tr('Selecionar camadas'),
                QgsProcessing.TypeMapLayer
            )
        )
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                'checkbox',
                self.tr('Atribuir SRC para camadas com SRC invalido'),
                QgsProcessing.TypeMapLayer
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(
            parameters,
            'INPUT',
            context
        )
        feedback.setProgressText('Atruibuindo SRC...')
        crsinput = parameters['INPUT']
       # Layers=self.parameterAsLayerList(parameters, 'InpLayers', context)
        #Layers=self.parameterAsMapLayer['InpLayers']
        Layers=self.parameterAsLayerList(parameters,'InpLayers', context)
        srcinvalido=self.parameterAsBool(parameters,'checkbox', context)
        '''
       # Layers.setCrs(crsinput)
        for layer in QgsProject.instance().mapLayers().values():
            for itens in Layers:
                #print("short name " + layer.shortName())
                print("name "+layer.name())
                print("itens " +itens.sourceName())
                if layer.name() == itens:
           # crs=layer.crs()
           # if not crs.isValid():
                    layer.setCrs(crsinput)
        '''
        for layer in Layers:
            layer.setCrs(crsinput)
        if srcinvalido:
            for layer in QgsProject.instance().mapLayers().values():
                crs=layer.crs()
                if not crs.isValid():
                    layer.setCrs(crsinput)
        return{}
  