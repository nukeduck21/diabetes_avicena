# Importing essential libraries
# import sys
# sys.path.append('api/')
from flask import Flask, render_template, request
import pickle
import numpy as np
import os
from api.utils import predict_custom_trained_model_sample
from api.restplus import api
from flask_restplus import Resource
import joblib

app = Flask(__name__, template_folder="api/templates")


@app.route("/")
def home():
    return render_template(f"index.html")


@app.route("/predict", methods=["POST"])
@api.response(200, "resultado validacion")
def predict():

    # parametros de carga de endpoint de GCP
    project_id = "476800759991"
    endpoint_predict = "38781974134915072"

    if request.method == "POST":
        # preg = 
        # glucose = 
        # bp = 
        # st = 
        # insulin = 
        # bmi = 
        # dpf = 
        # age = 
        # filename = 

        # payload = {
        #     "embarazos": preg,
        #     "glucosa": glucose,
        #     "Presión arterial": bp,
        #     "Grosor de la piel": st,
        #     "Insulina": insulin,
        #     "IMC": bmi,
        #     "DiabetesPedigreeFunction": dpf,
        #     "Edad": age,
        #     "Nombre del modelo": filename,
        # }
        edad = int(request.form["Edad"])
        genero = int(request.form["Genero"])
        nivel_academico_paciente = int(request.form["Nivel Academico"])
        compania = int(request.form["Compañia"])
        raza_paciente = int(request.form["raza"])
        peso = float(request.form["peso"])
        talla = float(request.form["talla"])
        imc = peso/(talla**2)
        Glicemia = float(request.form["Glicemia"])
        HDL = int(request.form["HDL"])
        LDL = str(request.form["LDL"])
        trigliceridos = int(request.form["trigliceridos"])
        med_hipertension = int(request.form["Med Hipertension"])
        familiar_dm = int(request.form["Familiar con DM"])
        ant_cardiovascular = int(request.form["Ant. CArdiovascular"])
        acantosis_nigricans = int(request.form["Acantosis Nigricans"])
        variables = np.array([edad,genero,nivel_academico_paciente,compania,raza_paciente,imc, Glicemia,HDL, LDL, trigliceridos, med_hipertension,familiar_dm, ant_cardiovascular,  acantosis_nigricans]).reshape(1, -1)

        try:
            model = joblib.load('../diabetes_multilabel_11001_1.pkl')
            my_prediction = model.predict(variables)/22

            return render_template("result.html", prediction=my_prediction)
        except BaseException as e:
            return e


@app.route("/ping")
@api.response(200, "resultado validacion")
class Predecir(Resource):
    def get(self):
        return {"status": "healthy"}


if __name__ == "__main__":
    app.run(debug=False)#, host = '0.0.0.0',port=8080)
