from flask_restplus import fields
from api.restplus import api

diabetes_estandar = api.model('Data para Diabetes', {
    'embarazos': fields.Integer(
        required=True,
        description='Cantidad de embarazasos',
        default=0
    ),
    'glucosa': fields.Integer(
        required=True,
        description='concentración de glucosa en plasma a las 2 horas en una prueba de tolerancia oral a la glucosa',
        default=0
    ),
    'Presión arterial': fields.Integer(
        required=True,
        description='presión arterial diastólica (mm Hg)',
        default=0
    ),
    'Grosor de la piel': fields.Integer(
        required=True,
        description='Grosor del pliegue cutáneo del tríceps (mm)',
        default=0
    ),
    'Insulina': fields.Integer(
        required=True,
        description='insulina sérica de 2 horas (mu U/ml)',
        default=0
    ),
    'IMC': fields.Integer(
        required=True,
        description='Índice de masa corporal (peso en kg/(altura en m)^2)',
        default=0
    ),
    'DiabetesPedigreeFunction': fields.Integer(
        required=True,
        description='función de pedigrí de diabetes',
        default=0
    ),
    'Edad': fields.Integer(
        required=True,
        description='Edad (años)',
        default=0
    ),
    'Nombre del modelo': fields.Integer(
        required=True,
        description='Nombre del modelo pickle en GCS a traer',
        default='diabetes-prediction-rfc-model.pkl'
    )
})

Diabetes_GCP = api.model('payload endpoint vertex endpoint', {
    'instances': fields.List(fields.Nested(diabetes_estandar)),
})