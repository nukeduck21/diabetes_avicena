from flask_restplus import fields
from api.restplus import api

diabetes_estandar = api.model('Data de la Tasa de Uso', {
    'Ciudad': fields.Integer(
        required=True,
        description='Ciudad de la atencion',
        default=11001
    ),
    'Edad': fields.Integer(
        required=True,
        description='Edad del paciente',
        default='65'
    ),
    'Genero': fields.Integer(
        required=True,
        description='Genero del paciente',
        default='Femenino'
    ),
    'Nivel_Academico': fields.Integer(
        required=True,
        description='Nivel academico del paciente',
        default=''
    ),
    'Compañia': fields.Integer(
        required = True,
        description = 'Compañia aseguradora del paciente',
        default = 'EPS'
    ),
    # 'Raza': fields.Integer(
    #     required = True,
    #     description = 'Raza del paciente',
    #     default = ''
    # ),
    'Peso': fields.Integer(
        required = True,
        description = 'Peso del paciente',
        default = 70
    ),
    'Talla': fields.Integer(
        required = True,
        description = 'Talla del paciente',
        default = 1.80
    ),
    'Perimetro_Abdominal': fields.Integer(
        required = True,
        description = 'Perimetro Abdominal del paciente',
        default = 80
    ),
    'Glicemia': fields.Integer(
        required = True,
        description = 'Examen de Glicemia',
        default = 90
    ),
    'HbA1c': fields.Integer(
        required = True,
        description = 'Examen de HbA1c',
        default = 'No Aplica'
    ),
    'HDL': fields.Integer(
        required = True,
        description = 'Examen HDL',
        default = 40
    ),
    'LDL': fields.Integer(
        required = True,
        description = 'Examen LDL',
        default = 80
    ),
    'Trigliceridos': fields.Integer(
        required = True,
        description = 'Examen de trigliceridos',
        default = 200
    ),
    'Med_Hipertension': fields.Integer(
        required = True,
        description = '¿Consume medicamentos para la hipertension?',
        default = 'Si'
    ),
    'Familiar_con_DM': fields.Integer(
        required = True,
        description = '¿Algun familiar ha sido diagnosticado con Diabetes?',
        default = 'No'
    ),
    'Ant_Cardiovascular': fields.Integer(
        required = True,
        description = '¿Tiene algun antecedente cardiovascular?',
        default = 'Si'
    ),
    'Acantosis_Nigricans': fields.Integer(
        required = True,
        description = '¿Tiene acantosis nigricans?',
        default = 'No'
    ),
    'Ejercicio': fields.Integer(
        required = True,
        description = 'Actividad fisica diaria del paciente',
        default = 'No'
    )
})

Diabetes_gcp_arguments = api.model('payload endpoint vertex endpoint', {
    'instances': fields.List(fields.Nested(diabetes_estandar)),
})