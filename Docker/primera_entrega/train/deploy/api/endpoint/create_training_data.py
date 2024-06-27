import argparse
from api.endpoint.utils import *
from api.endpoint.params import *
import logging
from api.restplus import api
from api.serializers import create_data_GCP
from flask_restplus import Resource
from flask import request
from time import time

log = logging.getLogger(__name__)
ns = api.namespace(
    "Creacion data Diabetes",
    description="Sección para la extracción y consolidacion de la información de diabetes de Avicena en el repositorio",
    path="/creacion_data_diabetes",
)

@ns.route("/ping")
@api.response(200, "resultado validacion")
class Predecir(Resource):
    def get(self):
        return {"status": "healthy"}
    
@ns.route("/crear_data")
@api.response(200, "resultado validacion")
class ejecutar(Resource):
    def create_data(self):
        """
        Ejecuta el modelo de diabetes utilizando los datos del archivo CSV especificado y guarda el modelo en un archivo pickle.

        Argumentos:
            csv_file (str): Nombre del archivo CSV que contiene los datos de entrada.
            pkl_file (str): Nombre del archivo pickle de salida para guardar el modelo entrenado.
        """

        nombre_tabla_examenes = 'examenes_por_usuarios'

        parametros_creacion = {"destination":proyecto+"."+dataset+"."+nombre_tabla_examenes,
                            "description":"Tabla con los resultados de los examenes mas recientes para cada paciente",
                            "partition_field":'',
                            "clustering_fields":['numero_identificacion_paciente']}
        
        print(f'Creando la tabla: {parametros_creacion["destination"]}')
        
        create_table_bq(client=client_bq,query=SQL_examenes,project_id=proyecto,dataset_id=dataset,table_name=nombre_tabla_examenes,replace=True,**parametros_creacion)
        
        nombre_tabla_compania = 'compania_x_usuarios'

        parametros_creacion = {"destination":proyecto+"."+dataset+"."+nombre_tabla_compania,
                            "description":"Tabla con las compañias para cada paciente",
                            "partition_field":'',
                            "clustering_fields":['numero_identificacion_paciente']}
        
        # Creacion de la tabla

        print(f'Creando la tabla: {parametros_creacion["destination"]}')

        create_table_bq(client=client_bq,query=SQL_compania,project_id=proyecto,dataset_id=dataset,table_name=nombre_tabla_compania,replace=True,**parametros_creacion)

        # Parametros de subida

        nombre_tabla_antecedentes = 'antecedentes_x_usuario'

        parametros_creacion = {"destination":proyecto+"."+dataset+"."+nombre_tabla_antecedentes,
                            "description":"Tabla con los antecedentes para cada paciente",
                            "partition_field":'',
                            "clustering_fields":['numero_identificacion_paciente']}
        
        # Creacion de la tabla

        print(f'Creando la tabla: {parametros_creacion["destination"]}')

        create_table_bq(client=client_bq,query=SQL_antecedentes,project_id=proyecto,dataset_id=dataset,table_name=nombre_tabla_antecedentes,replace=True,**parametros_creacion)
        
        # Parametros de subida

        nombre_tabla_perimetros = 'perimetros_x_usuarios'

        parametros_creacion = {"destination":proyecto+"."+dataset+"."+nombre_tabla_perimetros,
                            "description":"Tabla con los antecedentes para cada paciente",
                            "partition_field":'',
                            "clustering_fields":['numero_identificacion_paciente']}
        
        print(f'Creando la tabla: {parametros_creacion["destination"]}')

        # Creacion de la tabla

        create_table_bq(client=client_bq,query=SQL_perimetros,project_id=proyecto,dataset_id=dataset,table_name=nombre_tabla_perimetros,replace=True,**parametros_creacion)

        # Parametros de subida

        nombre_tabla_ejercico = 'actividadFisica_x_usuarios'

        parametros_creacion = {"destination":proyecto+"."+dataset+"."+nombre_tabla_ejercico,
                            "description":"Tabla con los antecedentes para cada paciente",
                            "partition_field":'',
                            "clustering_fields":['FOLIO']}

        # Creacion de la tabla

        print(f'Creando la tabla: {parametros_creacion["destination"]}')

        create_table_bq(client=client_bq,query=SQL_ejercicio,project_id=proyecto,dataset_id=dataset,table_name=nombre_tabla_ejercico,replace=True,**parametros_creacion)

        # Parametros de subida

        nombre_tabla_diabetes = 'diabetes'

        parametros_creacion = {"destination":proyecto+"."+dataset+"."+nombre_tabla_diabetes,
                            "description":"Tabla con los datos consolidados para el entrenamiento del modelo de diabetes",
                            "partition_field":'',
                            "clustering_fields":['numero_identificacion_paciente']}
        
        # Creacion de la tabla

        print(f'Creando la tabla: {parametros_creacion["destination"]}')

        create_table_bq(client=client_bq,query=SQL_diabetes,project_id=proyecto,dataset_id=dataset,table_name=nombre_tabla_diabetes,replace=True,**parametros_creacion)


    @api.expect(create_data_GCP)
    def post(self):
        data = request.json

        parametro = data["instances"][0]["Crear"]

        if parametro == 'Si':
            time_i = time()
            self.create_data()
            return {"predictions": f'Data creada exitosamente en el dataset {proyecto+"."+dataset} demorandose: {time() - time_i} segundos'}
        else:
            return {"predictions": f'No se creo la data'}

        