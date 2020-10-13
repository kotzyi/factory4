import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

try:
    print("Azure Blob storage v" + __version__ + " - Python quickstart sample")
    # Quick start code goes here
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "models"

    # Create the container
    # container_client = blob_service_client.create_container(container_name)

    # Create a file in local data directory to upload and download
    upload_file_path = "/home/tflite-converter/exported-models/model.tflite" #os.path.join(local_path, local_file_name)
    local_file_name = "model.tflite"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
except Exception as ex:
    print('Exception:')
    print(ex)
