import warnings

warnings.simplefilter('ignore')

import numpy as np

from api.utils import predict_custom_trained_model_sample
from api.serializers import Diabetes_GCP
from api.restplus import api
import logging
from flask_restplus import Resource
from flask import request

log = logging.getLogger(__name__)
ns = api.namespace('Predicción Diabetes', description='Arboles de decisión', path='/prediccion_diabetes')

@ns.route('/ping')
@api.response(200, 'resultado validacion')
class Predecir(Resource):
    
    def get(self):
        return {"status": "healthy"}
    
@ns.route('/predecir')
@api.response(200, 'resultado validacion')
class Ejecutar(Resource):

    # parametros de carga de endpoint de GCP
    project_id = "476800759991"
    endpoint_predict = "38781974134915072"

    @api.expect(Diabetes_GCP)
    def post(self):

        data = request.json

        embarazos = int(data['instances'][0]['embarazos'])
        glucosa = int(data['instances'][0]['glucosa'])
        presion_sanguinea = int(data['instances'][0]['Presión arterial'])
        grosor_piel= int(data['instances'][0]['Grosor de la piel'])
        insulina= int(data['instances'][0]['Insulina'])
        imc= float(data['instances'][0]['IMC'])
        dpf= float(data['instances'][0]['DiabetesPedigreeFunction'])
        edad= int(data['instances'][0]['Edad'])
        
        filename = str(data['instances'][0]['Nombre del modelo'])

        payload = {
            "embarazos": embarazos,
            "glucosa": glucosa,
            "Presión arterial": presion_sanguinea,
            "Grosor de la piel": grosor_piel,
            "Insulina": insulina,
            "IMC": imc,
            "DiabetesPedigreeFunction": dpf,
            "Edad": edad,
            "Nombre del modelo": filename,
        }

        data = np.array([[embarazos, glucosa, presion_sanguinea, grosor_piel, insulina, imc, dpf, edad]])

        my_prediction = predict_custom_trained_model_sample(
                project=self.project_id,
                endpoint_id=self.endpoint_predict,
                location="us-east1",
                instances=payload,
            )

        if str(int(my_prediction)) == '0':
            var_to_return = 'Wow! Que bien! NEGATIVO para diabetes.'
        else:
            var_to_return = 'Opps! POSITIVO para diabetes.'
        output = {'prediccion_modelo': var_to_return} 

        return { "predictions": [output]}