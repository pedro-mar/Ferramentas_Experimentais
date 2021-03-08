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
                       QgsVectorLayer,
                       QgsFeature
                       )
from qgis import processing
import os
from shutil import *
import datetime
import subprocess
import shutil
class ExportarParaShapefile (QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.


    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExportarParaShapefile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'exportar_para_shapefile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Exportar para Shapefile')

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
        return self.tr("O algoritmo exporta camadas de um projeto para o formato shapefile ")
    # -*- coding: utf-8 -*-



    def copyfileobj_example(source, dest, buffer_size=1024*1024):
        """      
        Copy a file from source to dest. source and dest
        must be file-like objects, i.e. any object with a read or
        write method, like for example StringIO.
        """
        while True:
            copy_buffer = source.read(buffer_size)
            if not copy_buffer:
                break
            dest.write(copy_buffer)
            
    def copyfile_example(source, dest):
        # Beware, this example does not handle any edge cases!
        with open(source, 'rb', encoding='utf-8') as src, open(dest, 'wb', encoding='utf-8') as dst:
            copyfileobj_example(src, dst)


            #print(destfile)
            

        
    def copyPasteLayer(self, sourceLayer, destLayer, folder):  
        if os.path.exists(folder+destLayer+'.shp'):
           # print('Camada copiada:' + destLayer+'.shp')
            # Copying features
            sourceLYR = QgsProject.instance().mapLayersByName(sourceLayer)[0]
            #destLYR = QgsProject.instance().mapLayersByName(destLayer)[0]
            destLYR_path = folder + sourceLayer + '.shp'
            destLYR = QgsVectorLayer(destLYR_path,destLayer,'ogr')    
           # destLYR.setProviderEncoding('utf8')
            #destLYR.dataProvider().setEncoding('utf8')
            destLYR_fields = destLYR.fields()
            fields_to_copy = destLYR_fields.names() 
            if 'FCODE' in fields_to_copy:
                fields_to_copy.remove('FCODE')
            newfeature_list  = []
            
            
            for count, feature_tocopy in enumerate(sourceLYR.getFeatures()):
                new_feature =  QgsFeature()
                new_feature.setFields(destLYR_fields)
                new_feature.setGeometry(feature_tocopy.geometry())
                for field_name in fields_to_copy:
                    new_feature[field_name] = feature_tocopy[field_name.lower()]
                new_feature['FCODE'] = destLayer[1:]
                newfeature_list.append(new_feature)
            
            
            destLYR.startEditing()
            data_provider = destLYR.dataProvider()
           # destLYR.setProviderEncoding('utf8')
           # data_provider.setEncoding('utf8')
            data_provider.addFeatures(newfeature_list)
            destLYR.commitChanges()

    def copyingLayerFiles(self, destLayer,dest_folder,origin_folder):
        
        extensions = ['.dbf','.prj', '.shx']

        for extension in extensions:
            sourcefile = origin_folder + destLayer + extension
            destfile = dest_folder + destLayer + extension
            if os.path.exists(sourcefile):
                copyfile(sourcefile,destfile)

    def convertUTF8(self, destLayer, nome,dest_folder, origin):
        extensions = ['.shp']
        for extension in extensions:
            inputFile = origin + destLayer + extension
            outputFile = dest_folder + destLayer + extension
            if os.path.exists(inputFile):
                command = ['ogr2ogr' ,outputFile, inputFile ,'-lco','ENCODING=UTF-8']
                # subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
                subprocess.call(command, shell=True)


    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
    
    
    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

    # Creating the folder
        base_folder = 'C:\\Users\\pedromartins\\Missoes\\003\\exporttest\\' #destino
        nome = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dest_folder = base_folder + nome + '\\'
        os.makedirs(dest_folder)

        camadas_mgcp = []

        for key, layer in QgsProject.instance().mapLayers().items():
            camadas_mgcp.append(layer)

        camadas_mgcp = [camada_mgcp.name() for camada_mgcp in camadas_mgcp]
        #print(camadas_mgcp)
        # Copiando os dados

        origin_folder = 'C:\\Users\\pedromartins\\Missoes\\003\\MGCP_4_4_SHP_To_BRA\\' # pasta dos shp exemplo

        for camada_mgcp_db in camadas_mgcp:
            camada_mgcp_shp = camada_mgcp_db.upper()
            feedback.setProgressText('Atribuindo...' + camada_mgcp_shp)
            #self.copyingLayerFiles(camada_mgcp_shp, dest_folder, origin_folder)
            #feedback.setProgressText('Copiado')
            self.convertUTF8(camada_mgcp_shp,nome, dest_folder, origin_folder)
            feedback.setProgressText('Convertido')
            self.copyPasteLayer(camada_mgcp_db,camada_mgcp_shp, dest_folder)
            #feedback.setProgressText('Fim da iteracao')
        #print('Exportação de dados completa.')
        
        feedback.setProgressText('Executado')


        return {}
