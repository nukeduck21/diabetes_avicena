# Entrenamiento modelo Diabetes Mellitus API - Registro del modelo en GCP

### Tabla de contenido
  * [Introducción](#introducción)
  * [Aplicativo](#aplicativo)
  * [Equipo](#equipo)
  * [Notas](#nota)

## Introducción
En esta seccion encontrara toda la información necesaria para el despliegue local del aplicativo Flask que consume el endpoint  para predecir haciendo uso del modelo de Diabetes Mellitus.

### Aplicativo
inciando una terminal y dirigiendose a la carpeta de 'deploy', al ejecutar el comando

```sh
  python main.py
```

Se desplegara por defecto en la url local 'http://0.0.0.0:8080/' el aplicativo que le permite ejecutar consumir el endpoint del modelo entrenado de diabetes, donde puede hacer uso del siguiente ejemplo de parametros para realizarlo

*Ejemplo de parametros*
```sh
    {
        "instances": [
            {
            "pregnancies": 3,
            "glucose": 110,
            "bloodpressure": 92,
            "skinthickness": 0,
            "insulin": 0,
            "bmi": 24,
            "dpf": 0.61,
            "age": 35,
            "model_name": "diabetes-prediction-rfc-model.pkl"
            }
        ]
    }
```

En la salida vera el resultado de la predicción de los datos proporcionados.

### Equipo
- Keralty - Analítica Avanzada (Gerencia Datos - Colombia)
  2023 (c)

### Nota:
- La aplicación web puede manejar la concurrencia hasta cierto punto, pero se puede escalar.
- Los desempeños pueden mejorar, pero este caso es solo TEST. En NINGÚN caso puede ser usado en producción
- Cada script posee su documentación y comentarios detallados.