from flask_restplus import fields
from api.restplus import api

# Parametros de entrenamientos
train_diabetes_estandar = api.model(
    "Data para Diabetes",
    {
        "ciudades": fields.Integer(
            required=True,
            description="Ciudades a tomar para el entrenamiento",
            default=[11001],
        )
    },
)

Diabetes_train_GCP = api.model(
    "payload endpoint vertex endpoint",
    {
        "instances": fields.List(fields.Nested(train_diabetes_estandar)),
    },
)

# Parametros para la creacion de los datos de diabetes
create_data_standar = api.model(
    "Creacion de la informacion de diabetes",
    {
        "Crear": fields.Integer(
            required=True,
            description="Parametro para la creacion de la data",
            default="No",
        )
    },
)

create_data_GCP = api.model(
    "payload endpoint vertex endpoint",
    {
        "instances": fields.List(fields.Nested(create_data_standar)),
    },
)