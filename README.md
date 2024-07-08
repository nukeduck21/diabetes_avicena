<h1 align="center"> DIABETES AVICENA </h1>

## Tabla de contenidos:
---
- [Introducción](#introducción)
- [Uso](#uso)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Requisitos previos](#requisitos-previos)
- [Contribuciones](#contribuciones)
- [Descripción y contexto](#descripción-y-contexto)
- [Guía de instalación](#guía-de-instalación)
- [Dependencias](#dependencias)
- [Información adicional](#información-adicional)

## Introducción
---
La diabetes es una enfermedad crónica que afecta la manera en que el cuerpo convierte el alimento en energía. Cuando el nivel de azúcar

en la sangre aumenta, el páncreas libera insulina, que actúa como una llave para permitir que la glucosa entre en las células del cuerpo

y se utilice como energía.

Existen varios tipos de diabetes, los más comunes son:

	- Diabetes tipo 1: Es una condición en la que el cuerpo no produce insulina y es diagnosticada comúnmente en niños y adultos jóvenes.
 
 	- Diabetes tipo 2: Es una condición en la que el cuerpo no usa insulina correctamente y se desarrolla a lo largo de muchos años.
  
  	- Diabetes gestacional: Ocurre durante el embarazo y puede aumentar el riesgo de desarrollar diabetes tipo 2 más adelante.

## Uso
---
Para utilizar este repositorio, sigue los siguientes pasos:

<b>1.</b>Clona el repositorio

 	git clone https://source.developers.google.com/p/co-keralty-costomedico/r/diabetes_avicena
  
<b>2.</b>Explorar los datos

El repositorio incluye diversos conjuntos de datos sobre diabetes, La organización de estos datos 

y el código asociado se distribuye de la siguiente manera:

### Estructura del repositorio:

	- 'diabetes_avicena/': Es la carpeta principal que contiene todos los datos y código relacionados 

	con el proyecto de diabetes.
 
 ---

	- 'Codigo/': Dentro de esta carpeta se encuentra el desarrollo del proyecto, al desplegar esta 

	carpeta, encontrarás varios tipos de archivos y subcarpetas.

 ---

	-'Docker/': Contiene la carpeta de primera entrega con codigo Python, facilitandon el análisis 

	de los datos.

 ---

	-'Notebook/': Contiene la carpeta de segunda entrega con codigo Python, que facilita la explicación

	y análisis de los datos.
 ---

	- 'Documentacion/': Esta carpeta contiene un documento 'README.md'.
 ---

	- '.gitignore': Espesifica que archivos o directorios deben ser ignorados y no incluidos.
 ---

	- 'README.md': Proporciona una visión general del proyecto, instruciones de uso, y cualquiero 

	otra información para los desarrolladores y usuarios del repositorio.
 ---
 
 Este proyecto contiene la siguiente estructura de carpetas y archivos:

 diabetes_avicena/

├── Codigo/

├── Docker/

├── primera_entrega/

│ ├── client/

│ ├── api/

│ │ ├── endpoint/

│ │ │ └── diabetes.py

│ ├── restplus.py

│ ├── serializers.py

│ ├── settings.py

│ ├── utils.py

│ ├── main.py

│ ├── requirements.txt

├── deploy/

├── api/

│ ├── static/

│ │ ├── diabetes.webp

│ │ └── no-diabetes.webp

│ ├── templates/

│ │ ├── index.html

│ │ └── result.html

│ ├── restplus.py

│ └── utils.py

├── gcp/

│ ├── api/

│ │ ├── endpoint.py

│ │ ├── restplus.py

│ │ ├── serializers.py

│ │ ├── settings.py

│ │ └── utils.py

│ ├── Dockerfile

│ ├── main.py

│ ├── requirements.txt

│ ├── Dockerfile

│ ├── main.py

│ ├── README.md

│ └── requirements.txt

├── train/

│ ├── deploy/

│ │ ├── api/

│ │ │ ├── endpoint/

│ │ │ │ ├── create_training_data.py

│ │ │ │ ├── diabetes_masterClass.py

│ │ │ │ ├── diabetes_train.py

│ │ │ │ ├── params.py

│ │ │ │ └── utils.py

│ │ │ ├── restplus.py

│ │ │ ├── serializers.py

│ │ │ ├── settings.py

│ │ │ ├── main.py

│ │ │ ├── README.md

│ │ │ └── requirements.txt

│ │ └── consolidacion_data.ipynb

├── Notebook/

├── segunda_entrega/

│ ├── analisis/

│ │ ├── analisisInicial.ipynb

│ │ └── requirements.txt

│ ├── 0_consolidacion_data.ipynb

│ ├── 1_primerEjercicio_prediccion.ipynb

│ ├── 2_ajustes_hiperparametros.ipynb

│ ├── README.md

├── Documentacion/

│ └── README.md

├── .gitignore

├── README.md


<b>3.</b>Visualiza resultados

  	Los resultados de los análisis y modelos se guardan en la carpeta 'diabetes_avicena/'. Utilizando los Notebook y scripts
   	proporcionados para visualizar y entender estos resultados.
   
## Tecnologías utilizadas
---
  Para utilizar localmente, necesitamos lo siguiente:

   - Un sistema operativo compatible (Windows, macOS o Linux)
     
   - Visual Studio Code: Entorno de desarrollar.

   - Python: Lenguaje de programación principal utilizado para el análisis de datos y la construcción de modelos.
     
   - Git: Sistema de control de versiones utilizado para gestionar el código fuente del proyecto.
     
   - Cloud sorce: Plataforma para alojar el repositorio y colaboración en el desarrollo del proyecto.

## Instalación
---
Para instalar sigue estos pasos:

<b>1.</b>Clona el repositorio

 	git clone https://source.developers.google.com/p/co-keralty-costomedico/r/diabetes_avicena
       
<b>2.</b>Navegamos hasta la dirección de la carpeta
   
      cd repo-remoto
  
      cd diabetes_avicena
  
<b>3.</b>Lista un estado actual del repositorio con lista de archivos modificados o agregados

      git status

<b>4.</b>Añadimos todos los archivos para el commit
   
      git add .
   
      git add archivo.txt

<b>5.</b>Hacemos el primer commit
   
      git commit -m "Texto que identifique porque se hizo el commit"

<b>6.</b>Busca los cambios nuevos y actualiza el repositorio
   
      git pull

<b>7.</b>subimos al repositorio
   
      git push

## Requisitos previos
---
Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- Git
- Python 
- Visual Studio Code (o cualquier otro editor de código)
  
## Contribuciones
---
¡Gracias por interesarse en contribuir en este proyecto!, Nos complace recibir correcciones e ideas. 

Para contribuir a este proyecto, sigue estos pasos:

### Documentación:

- Actualizar o mejora la documentación existente.

- Añadir comentarios al código para explicar su funcionamiento.

### Pruebas:

- Reporta errores encontrados durante las pruebas.

### Código:

- Optimizar y mejorar el rendimiento del código.

## Descripción y contexto
---
Esto es un archivo README. Debe contener la documentación de soporte uso de la herramienta digital. 
 	
## Guía de instalación
---
La guía de instalación debe contener de manera específica:
- Los requisitos del sistema operativo para la compilación (versiones específicas de librerías, software de gestión de paquetes y dependencias, SDKs y compiladores, etc.).
- Las dependencias propias del proyecto, tanto externas como internas (orden de compilación de sub-módulos, configuración de ubicación de librerías dinámicas, etc.).
- Pasos específicos para la compilación del código fuente y ejecución.

## Dependencias
---
Descripción de los recursos externos que generan una dependencia para la reutilización de la herramienta digital (librerías, frameworks, acceso a bases de datos y licencias de cada recurso). Es una buena práctica describir las últimas versiones en las que ha sido probada la herramienta digital. 

## Información adicional
---
Esta es la sección que permite agregar más información de contexto al proyecto como alguna web de relevancia, proyectos similares o que hayan usado la misma tecnología.

