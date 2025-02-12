from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import prince
import pandas as pd
import numpy as np
from google.cloud import bigquery
import matplotlib.pyplot as plt

client_bq = bigquery.Client()

def escalar(data):
    
    # Crear el escalador
    scaler = MinMaxScaler()
    
    # Entrenar el escalador
    scaler.fit(data)
    
    # Re-escalar los datos
    df_escalado = pd.DataFrame(scaler.transform(data))
    
    return df_escalado

def outlier_label(value, limit):
    if value < limit[0]:
        return 'Abajo'
    elif value > limit[1]:
        return 'Arriba'
    else:
        return 'No'

def tag_outliers(data, variable):
    Q1 = data[variable].quantile(0.25)
    Q3 = data[variable].quantile(0.75)
    RIC = Q3 - Q1
    limit_inf = Q1 - (1.5 * RIC)
    limit_sup = Q3 + (1.5 * RIC)
    data[f'{variable}_outlier'] = data[variable].apply(lambda x: outlier_label(x, [limit_inf,limit_sup]))
    return data

def take_out_outliers(data, variables_with_outliers, verbose = True):
    
    data[variables_with_outliers] = data[variables_with_outliers].astype(float)
    for variable in variables_with_outliers:
        data_label = tag_outliers(data, variable)

    if verbose:
        for variable in variables_with_outliers:
            print(variable)
            conteos = data_label[f'{variable}_outlier'].value_counts().reset_index()
            total = conteos['count'].sum()
            conteos['Porcentaje'] = (conteos['count'] / total)*100
            display(conteos)

    columns_to_drop = [column + '_outlier' for column in variables_with_outliers]

    data_clean_outliers = data_label[(data_label.edad_outlier == 'No') &
                                     (data_label.IMC_outlier == 'No') &
                                     (data_label.HDL_outlier == 'No') &
                                     (data_label.LDL_outlier == 'No') &
                                     (data_label.trigliceridos_outlier == 'No')
                                    ]

    data_clean_outliers = data_clean_outliers.drop(columns = columns_to_drop)

    return data_clean_outliers

def criterio_benzecri(mca, plot = True):
    # Calcular la inercia total
    total_inertia = sum(mca.eigenvalues_)

    # Calcular el umbral de Benzécri
    benzecri_threshold = total_inertia / mca.n_components


    # Identificar las dimensiones a retener
    dimensions_to_keep = []
    for i in range(mca.n_components):
        if mca.eigenvalues_[i] > benzecri_threshold:
            dimensions_to_keep.append(i)

    # Visualizar las dimensiones retenidas
    print("Dimensiones retenidas (criterio de Benzécri):", dimensions_to_keep)

    if plot:
        # Puedes graficar la inercia explicada por cada dimensión
        plt.plot(range(1, mca.n_components + 1), mca.eigenvalues_, marker='o')
        plt.xlabel("Dimensión")
        plt.ylabel("Inercia explicada")
        plt.title("Inercia explicada por dimensión")
        plt.show()

    dimensions_to_keep = [f'Component_mca_{i}' for i in dimensions_to_keep]

    return dimensions_to_keep

def MCA(data, n_comp, benzecri = True, plot = True):
    ## Creacion de ejes principales con MCA

    # Definicion del MCA
    mca = prince.MCA(n_components=n_comp)

    # Entrenamiento del MCA
    mca.fit(data)

    # Convertir los datos categoricos en los ejes
    components_mca=mca.fit_transform(data)

    # Nombrar los ejes
    name_of_columns_mca = [f'Component_mca_{i}' for i in range(len(components_mca.columns))]

    # Crear DataFrame con los ejes principales
    components_mca.columns = name_of_columns_mca

    if benzecri:
        # Criterio de benzecri para tomar ejes mas relevantes
        ejes_a_tomar_mca = criterio_benzecri(mca=mca, plot=plot)
        return components_mca, mca, ejes_a_tomar_mca
    else:
        return components_mca, mca, []

def ACP(data, n_comp, scale = True):

    if scale:
        # Crear el escalador
        scaler = MinMaxScaler()
        # Entrenar el escalador
        scaler.fit(data)
        # Re-escalar los datos
        df_escalado = pd.DataFrame(scaler.transform(data))
    else:
        df_escalado = df_numerico[::]

    # Crear PCA
    pca = PCA(n_components=n_comp)

    # Crear los ejes factoriales
    components=pca.fit_transform(df_escalado)

    # Nombrar los ejes
    number_of_axis = [f'Component_{i}' for i in range(n_comp)]

    # Crear DataFrame con los ejes principales
    components_df=pd.DataFrame(data=components,columns=number_of_axis)

    return components_df, pca

def crear_ejes(data, pca_columns, pca_n_comp, acm_columns, acm_n_comp, benzecri = True, plot = True, scale = True):
    components_df, pca = ACP(data[pca_columns], pca_n_comp, scale = scale)
    components_mca, mca, ejes_a_tomar_mca = MCA(data[acm_columns], acm_n_comp, benzecri = benzecri, plot = plot)

    if benzecri:
        full_data = components_df.reset_index().merge(components_mca[ejes_a_tomar_mca].reset_index(), on = 'index', how = 'left')
    else:
        full_data = components_df.reset_index().merge(components_mca.reset_index(), on = 'index', how = 'left')

    full_data.drop(columns = 'index', inplace = True)

    return full_data