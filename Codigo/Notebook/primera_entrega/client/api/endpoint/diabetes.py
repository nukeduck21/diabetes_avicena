from google.cloud import bigquery
from time import time
import pandas as pd
import numpy as np
from sklearn.linear_model  import RidgeCV
from scipy.stats import zscore
# import plotly.express as px
import joblib

from api.restplus import api
import logging
from flask_restplus import Resource
from flask import request
from api.serializers import Diabetes_gcp_arguments
from api.utils import *
import traceback

# import plotly.io as io
import base64

log = logging.getLogger(__name__)
ns = api.namespace('Predicción Diabetes', description='Arboles de decisión', path='/prediccion')

@ns.route('/ping')
@api.response(200, 'resultado validacion')
class Predecir(Resource):
    
    def get(self):
        return {"status": "healthy"}
    
@ns.route('/predecir')
@api.response(200, 'resultado validacion')
class ejecutar_data(Resource):

    @api.expect(Diabetes_gcp_arguments)
    def post(self):
        try:
            data = request.json

            print(f'Informacion suministrada: {data}') 

            ciudad = int(data['instances'][0]["Ciudad"])
            edad = int(data['instances'][0]["Edad"])
            genero = int(data['instances'][0]["Genero"])
            nivel_academico_paciente = int(data['instances'][0]["Nivel_Academico"])
            compania = int(data['instances'][0]["Compañia"])
            # raza_paciente = int(data['instances'][0]["Raza"])
            peso = float(data['instances'][0]["Peso"])
            talla = float(data['instances'][0]["Talla"])
            imc = peso/(talla**2)
            perimetro_abdominal = float(data['instances'][0]["Perimetro_Abdominal"])
            Glicemia = float(data['instances'][0]["Glicemia"])
            HbA1C = data['instances'][0]["HbA1c"]
            HDL = int(float(data['instances'][0]["HDL"]))
            LDL = str(data['instances'][0]["LDL"])
            trigliceridos = int(data['instances'][0]["Trigliceridos"])
            med_hipertension = int(data['instances'][0]["Med_Hipertension"])
            familiar_dm = int(data['instances'][0]["Familiar_con_DM"])
            ant_cardiovascular = int(data['instances'][0]["Ant_Cardiovascular"])
            acantosis_nigricans = int(data['instances'][0]["Acantosis_Nigricans"])
            hace_ejercicio = int(data['instances'][0]["Ejercicio"])

            if HbA1C != 'No Aplica':
                variables = np.array([edad,genero,nivel_academico_paciente,compania,imc, Glicemia,HDL, LDL, trigliceridos, med_hipertension,familiar_dm, ant_cardiovascular,  acantosis_nigricans,perimetro_abdominal,hace_ejercicio,int(HbA1C)]).reshape(1, -1)
                print(variables)
                model = load_from_gcs(f'model_with_hba1c_{ciudad}.pkl')  #joblib.load('api/endpoint/model_with_hba1c_11001.pkl')
            else:
                variables = np.array([edad,genero,nivel_academico_paciente,compania,imc, Glicemia,HDL, LDL, trigliceridos, med_hipertension,familiar_dm, ant_cardiovascular,  acantosis_nigricans,perimetro_abdominal,hace_ejercicio]).reshape(1, -1)
                print(variables)
                model = load_from_gcs(f'model_without_hba1c_{ciudad}.pkl') #joblib.load('api/endpoint/model_without_hba1c_11001.pkl') #load_from_gcs("co-keralty-models",f'portafolio/ads/toma_decision/costo_medico/tasa_de_uso/{prestacion}_{ciudad}_{sexo}.pkl') #joblib.load(f'./models/{prestacion}_{ciudad}_{sexo}.pkl')
            prediction = model.predict(variables)

            output = {
                'prediction tasa de uso': prediction[0]/22
            }  
            
            return { "predictions": [output]}

        except Exception as err:
            print(traceback.format_exc())
            return {'message': f'No se ha podido realizar la consolidaciond de la data','error' : f'{err}'}, 400