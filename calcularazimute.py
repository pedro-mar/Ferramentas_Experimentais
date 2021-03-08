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
from PyQt5.QtCore import QVariant
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
                       QgsAbstractFeatureSource,
                       QgsExpression,
                       QgsVectorLayer,
                       QgsField,
                       QgsExpressionContext,
                       QgsExpressionContextScope,
                       QgsAuxiliaryStorage,
                       QgsPropertyDefinition,
                       QgsFeature
                       )
from qgis import processing
from qgis.utils import iface
class CalcularAzimute(QgsProcessingAlgorithm):

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CalcularAzimute()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'calcula_azimute'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Calcula Azimute')

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
        return self.tr("O algoritmo calcula o angulo de uma feição em relação ao norte")
    
    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        
        '''
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT',
                self.tr('Camada selecionada:')
            )
        )
        '''
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
      
        feedback.setProgressText('Calculando azimute...')
        layer=iface.activeLayer()
        field = QgsField( 'id', QVariant.Double )

        cal=QgsAuxiliaryStorage()
        auxlyr=cal.createAuxiliaryLayer(field,layer)
        layer.setAuxiliaryLayer(auxlyr)
        auxLayer = layer.auxiliaryLayer()
        vdef=QgsPropertyDefinition("azim", 
        1, 
        "azimute", 
        "calcula angulo azimute",
        "angulo") 
        auxLayer.addAuxiliaryField(vdef)
        auxFields = auxLayer.fields()
        features=layer.getFeatures()
        for feature in features:
            geom=feature.geometry()
            ombb=geom.orientedMinimumBoundingBox()
            auxFeature = QgsFeature(auxFields)
            auxFeature['ASPK']= feature['id']
            angazim=ombb[2]
            if ombb[4]<ombb[3]:
                angazim=ombb[2]-90
                if angazim<0:
                    angazim=ombb[2]+90
            auxFeature['angulo_azim'] = angazim
            '''
            auxFeature['lado_lar'] = ombb[3]*1000
            auxFeature['lado_alt'] = ombb[4]*1000
            auxFeature['ver_boll'] = invertido
            '''
            auxLayer.addFeature(auxFeature)

        return{}
  