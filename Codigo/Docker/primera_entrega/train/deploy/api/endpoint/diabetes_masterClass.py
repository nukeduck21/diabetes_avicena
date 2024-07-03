from google.cloud import bigquery

from api.endpoint.utils import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class Train_diabetes:

    def __init__(self, variables_to_train, target_var, ciudad = None):
        self.raw_data_hba1c = None
        self.raw_data_no_hba1c = None
        self.variables = variables_to_train
        self.target_var = target_var
        self.ciudad = ciudad
        self.model_with_hba1c = None
        self.model_without_hba1c = None

    def bring_data(self):
        print('Trayendo data')
        self.raw_data_hba1c = pd.read_parquet('df_with_hba1c.parquet')
        self.raw_data_no_hba1c = pd.read_parquet('df_without_hba1c.parquet')

    def train(self):
        self.bring_data()

        print('Entrenando modelo con HbA1c')

        if self.ciudad == 'No Aplica':
            df_to_train = self.raw_data_hba1c[self.variables + ['HbA1c','codigo_ciudad_sucursal'] + self.target_var].dropna()
        else:
            df_to_train = self.raw_data_hba1c[(self.raw_data_hba1c.codigo_ciudad_sucursal == self.ciudad)][self.variables + ['HbA1c'] + self.target_var].dropna()

        X = df_to_train.drop(columns = self.target_var)
        y = df_to_train[self.target_var]

        X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        
        model = RandomForestClassifier(n_estimators=20)
        model.fit(X_train, y_train)

        metrica = round(model.score(X_test, y_test)*100,2)

        print(f'Modelo entrenado con una precision de: {metrica}')

        self.model_with_hba1c = model
        
        print('Entrenando modelo sin HbA1c')

        if self.ciudad == 'No Aplica':
            df_to_train = self.raw_data_no_hba1c[self.variables + ['codigo_ciudad_sucursal'] + self.target_var].dropna()
        else:
            df_to_train = self.raw_data_no_hba1c[(self.raw_data_no_hba1c.codigo_ciudad_sucursal == self.ciudad)][self.variables + self.target_var].dropna()
            
        X = df_to_train.drop(columns = self.target_var)
        y = df_to_train[self.target_var]

        X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        
        model = RandomForestClassifier(n_estimators=20)
        model.fit(X_train, y_train)

        metrica = round(model.score(X_test, y_test)*100,2)

        print(f'Modelo entrenado con una precision de: {metrica}')

        self.model_without_hba1c = model

    def save(self):
        upload_to_gcs(self.model_with_hba1c,f'model_with_hba1c_{self.ciudad}.pkl')
        upload_to_gcs(self.model_without_hba1c,f'model_without_hba1c_{self.ciudad}.pkl')

class prepare_data_to_train:

    def __init__(self,query, cliente):
        self.raw_data = None
        self.df_with_hba1c = None
        self.df_without_hba1c = None
        self.client = cliente #bigquery.Client()
        self.main_query = query
        self.tipo_id_dict = {'Cédula de ciudadanía':0,
                'Tarjeta de identidad':1,
                'Permiso por Protección Temporal':2,
                'Pasaporte':3,
                'Permiso Especial de Permanencia':4,
                'Salvo Conducto de Permanencia':5,
                'Registro civil':6,
                'Diplomatico':7,
                'Cédula de extranjería':8}

        self.nivel_academico_dict = {'Ninguno':0,
                                'Especialización':1,
                                'Bachillerato técnico':2,
                                'Básica secundaria':3,
                                'Técnica profesional':4,
                                'Básica primaria':5,
                                'Profesional':6,
                                'Media académica o clásica':7,
                                'Tecnológica':8,
                                'Normalista':9,
                                'Doctorado':10,
                                'Maestría':11,
                                'Preescolar':12,
                                None:13}

        self.raza_dict = {'Otros':0,
                    'Mestizo':1,
                    'Afrocolombiano':2,
                    'Indígena':3,
                    'Palenquero':4,
                    'Raizales':5,
                    'Rom/Gitano':6,
                    None:13}

        self.ejercicio_dict = {'Nunca\n':0,
                        '40 minutos\n':1,
                        '20 minutos\n':2,
                        '60 minutos\n':3}

        self.sexo_dict = {'Masculino' : 1,
                          'Femeino' : 0}
        
        self.compania_dict = {'EPS' : 0,
                              'MP' : 1,
                              '["EPS","MP"]' : 2}

    def format_for_dictionaries(self):
        dict_list = [['Tipo de Identificacion',self.tipo_id_dict],
                     ['Nivel Academico',self.nivel_academico_dict],
                     ['Raza',self.raza_dict],
                     ['Actividad Fisica',self.ejercicio_dict],
                     ['Genero',self.sexo_dict],
                     ['Compañia',self.compania_dict]
                     ]
        for diccionario in dict_list:
            print('------------------------------------')
            print(f'--------{diccionario[0]}----------')
            print(diccionario[1])

    def load_from_bq(self,sql_query):
        print(f'Trayendo el query: {sql_query}')
        df = self.client.query(sql_query).result().to_dataframe()

        return df

    def bring_raw_data(self):
        self.raw_data = self.load_from_bq(self.main_query)

    def preprocess_data(self):
        df_total = self.raw_data.copy()
        df_total = df_total[(~df_total.Glicemia.isin(['PENDIENTE','VER ANEXO'])) & (~df_total.HbA1c.isin(['PENDIENTE','VER ANEXO'])) & (~df_total.HDL.isin(['PENDIENTE','VER ANEXO'])) & (~df_total.trigliceridos.isin(['PENDIENTE','VER ANEXO'])) & (~df_total.LDL.isin(['PENDIENTE','VER ANEXO','COMENTARIO']))]

        df_total.raza_paciente = df_total.raza_paciente.replace(self.raza_dict)
        df_total.nivel_academico_paciente = df_total.nivel_academico_paciente.replace(self.nivel_academico_dict)
        df_total.tipo_identificacion_paciente = df_total.tipo_identificacion_paciente.replace(self.tipo_id_dict)
        df_total.hace_ejercicio = df_total.hace_ejercicio.replace(self.ejercicio_dict)

        df_total.edad = df_total.edad.astype(int)
        df_total.genero = df_total.genero.astype(int)
        df_total.codigo_ciudad_sucursal = df_total.codigo_ciudad_sucursal.fillna(-13).astype(int)
        df_total.peso = df_total.peso.astype(float)
        df_total.talla = df_total.talla.astype(float)
        df_total.imc = df_total.imc.astype(float)
        df_total.Glicemia = df_total.Glicemia.astype(float)
        df_total.HDL = df_total.HDL.astype(float)
        df_total.LDL = df_total.LDL.astype(float)
        df_total.PERIMETRO_ABDOMINAL = df_total.PERIMETRO_ABDOMINAL.astype(float)
        df_total.trigliceridos = df_total.trigliceridos.astype(float)
        df_total.med_hipertension = df_total.med_hipertension.astype(int)
        df_total.familiar_dm = df_total.familiar_dm.astype(int)
        df_total.ant_cardiovascular = df_total.ant_cardiovascular.astype(int)
        df_total.ovario_poliquistico = df_total.ovario_poliquistico.astype(int)
        df_total.dm_gestacional = df_total.dm_gestacional.astype(int)
        df_total.acantosis_nigricans = df_total.acantosis_nigricans.astype(int)

        df_total = df_total.drop(columns = ['numero_identificacion_paciente','tipo_identificacion_paciente'])

        df_con, df_sin = df_total[(df_total.HbA1c.fillna('NOOOO') != 'NOOOO') & (~df_total.HbA1c.isin(['PENDIENTE','VER ANEXO','ANEXO']))].drop_duplicates(), df_total[df_total.HbA1c.fillna('NOOOO') == 'NOOOO'].drop(columns = 'HbA1c').drop_duplicates()

        self.df_without_hba1c,self.df_with_hba1c = df_sin, df_con

    def save_data(self):
        self.df_with_hba1c.to_parquet('df_with_hba1c.parquet')
        self.df_without_hba1c.to_parquet('df_without_hba1c.parquet')
