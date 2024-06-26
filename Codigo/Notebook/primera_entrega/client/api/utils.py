from google.cloud import storage
import os
import joblib

def load_from_gcs(
    filename,
    bucket_name="co-keralty-models",
    full_path="portafolio/cds/pred_diagnostico/diabetes/diabetes_avicena/",
):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    destination_blob_name = full_path + filename

    print(f"Nombre del bucket: {bucket_name}")
    print(f"Ruta de donde se trae el modelo: {destination_blob_name}")

    storage_client = storage.Client()
    print("bucket_name:" + bucket_name)
    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(destination_blob_name)
    blob.download_to_filename("temp.pkl")
    model_gcp = joblib.load("temp.pkl")
    os.remove("temp.pkl")

    return model_gcp

ciudad_dict = {11001:'Bogotá, D.C.',
               76001: 'Cali',
               8001: 'Barranquilla',
               68001: 'Bucaramanga',
               50001: 'Villavicencio',
               5001: 'Medellín'
               }

sexo_dict = {0:'Mujeres',1:'Hombres'}