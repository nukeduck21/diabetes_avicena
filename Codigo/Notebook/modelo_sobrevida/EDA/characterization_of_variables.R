library(FactoClass)
library(bigrquery)
library(dplyr)
library(knitr)
library(DT)
library(DBI)

# Proyecto de GCP
project <- "co-keralty-costomedico"

# Query para traer la data de diabetes
query <- "SELECT * FROM Diabetes_avicena_survival.diabetes_final"

# Configuracion de la conexion a BigQuery
con <- dbConnect(bigrquery::bigquery(),
                 project = project,
                 dataset = "Diabetes_avicena_survival",
                 location = "us-east1")

# Traer la data desde BigQuery
data <- dbGetQuery(con, query)

# Columnas cualitativas
variables_numericas <- c("year",
                         "month",
                         "edad",
                         "peso",
                         "talla",
                         "HDL",
                         "LDL",
                         "trigliceridos",
                         "perimetro_abdominal",
                         "time_to_event")

# Columnas categoricas
variables_factores <- c("genero_paciente",
                        "raza_paciente",
                        "nivel_academico_paciente",
                        "ant_cardio",
                        "med_hipertension",
                        "ant_familiar_dm",
                        "hace_ejercicio",
                        "diabetes")

# Realizar cambios en cada una de las columnas de la data
data <- data %>% mutate(across(all_of(variables_factores), as.factor))
data <- data %>% mutate(across(all_of(variables_numericas), as.numeric))

# Vista de los cambios realizados
str(data)


print("Coeficientes de correlacion entre las variables continuas y Diabetes")
kable(centroids(data[, variables_numericas[3:length(variables_numericas)]],
                data$diabetes)$cr * 100,
      digits = 2)

print("Valores test para caracterización de variables cuantitativas y Diabetes")
cluster.carac(data[, variables_numericas[3:length(variables_numericas)]],
              data$diabetes,
              tipo.v = "co",
              v.lim = 2,
              dn = 4,
              dm = 4,
              neg = TRUE)

print("Pruebas Test y Chi2 para vars cualitativas y Diabetes")
kable(chisq.carac(data[, variables_factores], data$diabetes, decr = FALSE),
      digits = 8)

# Valores test para caracterización de diabetes
# según las variables cualitativas
data_prueba <- data.frame(data)
test_values <- cluster.carac(data_prueba[,
                               variables_factores[0:
                                                    (length(variables_factores)
                                                     - 1)]
                             ],
                             data_prueba$diabetes)

print("Valores test para las categorias contra Diabetes")
print(test_values)
