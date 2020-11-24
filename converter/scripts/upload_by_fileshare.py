import os
from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)
from azure.storage.fileshare import ShareFileClient


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
    model_file_name = str(os.getenv('MODEL_FILENAME_PREFIX')) + "_" + os.getenv('MODEL_FILE_NAME')
    saved_model_dir = os.getenv('EXPORTED_MODEL_SAVED_PATH')
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    share_name = os.getenv('AZURE_SHARE_NAME')
    dir_path = os.getenv('AZURE_MODEL_DIR_PATH')
    local_file_path = os.path.join(saved_model_dir, model_file_name)
    dest_file_path = os.path.join(dir_path, model_file_name)
    upload_local_file(connection_string, local_file_path, share_name, dest_file_path)


if __name__ == '__main__':
    main()
