from google.cloud import bigquery
from google.cloud import storage
import os
from time import time
import joblib
from api.endpoint.params import *

client_bq = bigquery.Client(project= proyecto)

def create_table_bq(client,query,project_id,dataset_id,table_name,replace=False,**kwargs):

    
    """
    
    This function creates (or replaces or aggregates information) a table in BigQuery from a query and stores it in a specific dataset. 
    If the table already exists, it appends the query results to the existing table.
    
    Parameters:
    - client: BigQuery API client object.
    - query: String representing the query to execute.
    - project_id: String representing the ID of the project where the dataset is located.
    - dataset_id: String representing the ID of the dataset where the table will be stored.
    - table_name: String representing the name of the table to be created or updated.
    - replace (optional): Boolean value indicating whether to replace the existing table before creating a new one.
    - **kwargs: Optional parameters to configure table creation, such as destination, write mode, 
      time partitioning, and clustering fields.
    
    Returns:
    - None
    """
    t_i = time()
    #creacion referencia tabla
    # table_ref = client.dataset(dataset_id).table(table_name)

    
    # Verificar si la tabla existe en el dataset
    try:
        print(project_id+"."+dataset_id+"."+table_name)
        client.get_table(project_id+"."+dataset_id+"."+table_name)
        existe = True
    except BaseException as e:
        print(e)
        existe = False
    
    
    if existe and replace: # si existe y se desea rempleazar
        
        print("Existe la tabla, se procede a remplazar")
        
        print(f'Borrando la tabla {kwargs["destination"]}')
        
        client.delete_table(kwargs["destination"], not_found_ok=True)#.result()
        
        if kwargs["partition_field"] != '':
            job_config = bigquery.QueryJobConfig(destination=kwargs["destination"],write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                                                time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.MONTH, # Or HOUR
            field=kwargs["partition_field"]) # The name of the partitioning column)
            ,clustering_fields=kwargs["clustering_fields"])
        else:
            job_config = bigquery.QueryJobConfig(destination=kwargs["destination"],
                                                 write_disposition=None,                       
                                                 clustering_fields=kwargs["clustering_fields"])
        query_job =client.query(query, job_config=job_config)

        results=query_job.result()
        bytes_processed = query_job.total_bytes_processed
        gb_processed = bytes_processed / (1024 * 1024 * 1024)
        print("Cantidad de GB procesadas: ",gb_processed)
        print("-------------------------------------------")
        t_f = time()

        print("tiempo transcurrido creacion de tabla ",t_f-t_i)
    elif (existe == False and replace==True) or (existe == False and  replace==False): # si hay algun error en la entrada de parametros
        print("No existe la tabla, se procede a crearla")

        if kwargs["partition_field"] != '':
            job_config = bigquery.QueryJobConfig(destination=kwargs["destination"],
                                                write_disposition=None,
                                                time_partitioning=bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.MONTH, # Or HOUR
                                                field=kwargs["partition_field"]), # The name of the partitioning column
                                                clustering_fields=kwargs["clustering_fields"])
        else:
            job_config = bigquery.QueryJobConfig(destination=kwargs["destination"],
                                                write_disposition=None,
                                                clustering_fields=kwargs["clustering_fields"])
            
            

        query_job =client.query(query, job_config=job_config)

        results=query_job.result()
        bytes_processed = query_job.total_bytes_processed
        gb_processed = bytes_processed / (1024 * 1024 * 1024)
        print("Cantidad de GB procesadas: ",gb_processed)
        print("-------------------------------------------")
        t_f = time()

        print("tiempo transcurrido creacion de tabla ",t_f-t_i)
    else: 
        print("Se annade datos a la tabla existente")
        job_config = bigquery.QueryJobConfig()
        
        job_config.destination = project_id+"."+dataset_id+"."+table_name
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        query_job =client.query(query, job_config=job_config)
        
        results=query_job.result()
        bytes_processed = query_job.total_bytes_processed
        gb_processed = bytes_processed / (1024 * 1024 * 1024)
        print("Cantidad de GB procesadas: ",gb_processed)
        print("-------------------------------------------")
        t_f = time()
        print("tiempo transcurrido annadiendo data ",t_f-t_i)

#Paremeters
GCP_BASE_STORAGE_PATH = "https://storage.cloud.google.com/"


def load_from_gcs(bucket_name, destination_blob_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    print(bucket_name, destination_blob_name)

    storage_client = storage.Client()
    print("bucket_name:" + bucket_name)
    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    print(destination_blob_name)
    blob = bucket.blob(destination_blob_name)
    blob.download_to_filename("temp.pkl")
    model_gcp = joblib.load("temp.pkl")
    os.remove("temp.pkl")

    return model_gcp


def upload_to_gcs(
    object,
    filename,
    storage_client=storage.Client(),
    bucket_name="co-keralty-models",
    full_path="portafolio/cds/pred_diagnostico/diabetes/diabetes_avicena/",
):
    """
    Carga un archivo a un bucket de Google Cloud Storage

    Argumentos:
        object (object): Objeto a subir al GCS.
        filename (str): Nombre del archivo pickle a subir.
        storage_client (object): Cliente de la api de Cloud Storage.
        bucket_name (str): Nombre del bucket en GCS.
        full_path (str): Ruta en el bucket donde se va a guardar el archivo.
    """

    # traer el bucket definidio
    bucket = storage_client.bucket(bucket_name)

    # definir la ruta donde se va a guardar el archivo
    destination_blob_name = full_path + filename
    blob = bucket.blob(destination_blob_name)

    # guardar temporalmente y subir el archivo
    joblib.dump(object, "temp.pkl")
    blob.upload_from_filename("temp.pkl")
    os.remove("temp.pkl")

    
    return (
        GCP_BASE_STORAGE_PATH + bucket_name + "/" + destination_blob_name
    )