import os
from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareServiceClient,
    ShareClient,
    ShareDirectoryClient,
    ShareFileClient
)


def upload_local_file(connection_string, local_file_path, share_name, dest_file_path):
    try:
        source_file = open(local_file_path, "rb")
        data = source_file.read()

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, dest_file_path)

        print("Uploading to:", share_name + "/" + dest_file_path)
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


def main():
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    local_file_path = "/home/tflite-converter/exported-models/model.tflite"  # os.path.join(local_path, local_file_name)
    share_name = "models"

    dest_file_path = "test/1/model.tflite"
    # Create a ShareServiceClient from a connection string
    upload_local_file(connection_string, local_file_path, share_name, dest_file_path)

if __name__ == '__main__':
    main()
