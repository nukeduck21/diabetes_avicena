import argparse
from api.endpoint.utils import *
from api.endpoint.params import *
from api.endpoint.diabetes_masterClass import *
import logging
from api.restplus import api
from api.serializers import Diabetes_train_GCP
from flask_restplus import Resource
from flask import request
from time import time
import joblib



log = logging.getLogger(__name__)
ns = api.namespace(
    "Entrenamiento Diabetes",
    description="Sección para el entrenamiento de diabetes de Avicena traido desde el repositorio",
    path="/entrenamiento_diabetes",
)

@ns.route("/ping")
@api.response(200, "resultado validacion")
class Predecir(Resource):
    def get(self):
        return {"status": "healthy"}
    
@ns.route("/entrenar")
@api.response(200, "resultado validacion")
class ejecutar(Resource):
    @api.expect(Diabetes_train_GCP)
    def post(self):
        data = request.json

        print(data)

        ciudades = data["instances"][0]["ciudades"]
        variables_para_entrenar_h = ['edad','genero','nivel_academico_paciente','compania','imc', 'Glicemia','HDL', 'LDL', 'trigliceridos', 'med_hipertension','familiar_dm', 'ant_cardiovascular',  'acantosis_nigricans', 'PERIMETRO_ABDOMINAL','hace_ejercicio']
        target_var = ['riesgo_final']

        try:
            pd.read_parquet('df_with_hba1c.parquet')
            pd.read_parquet('df_without_hba1c.parquet')
        except:
            preparador = prepare_data_to_train(SQL_train, client_bq)
            preparador.bring_raw_data()
            preparador.preprocess_data()
            preparador.save_data()

        for ciudad in ciudades:
            trainer = Train_diabetes(variables_to_train = variables_para_entrenar_h, target_var=target_var, ciudad=ciudad)
            trainer.train()
            trainer.save()


        return {"predictions": f'Modelos guardados exitosamente para las ciudades {ciudades}'}