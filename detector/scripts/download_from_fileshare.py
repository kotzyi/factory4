import os
from azure.core.exceptions import (
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareDirectoryClient,
    ShareFileClient
)


def list_files_in_azure_directory(connection_string, share_name, dir_path):
    try:
        files = []
        parent_dir = ShareDirectoryClient.from_connection_string(conn_str=connection_string, share_name=share_name,
                                                                 directory_path=dir_path)
        for item in list(parent_dir.list_directories_and_files()):
            if item['is_directory']:
                files += (list_files_in_azure_directory(
                    connection_string, share_name, os.path.join(dir_path, item['name'])))
            else:
                files.append(os.path.join(dir_path, item['name']))

        return files
    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


def download_azure_file(connection_string, share_name, source_file_path, local_dir_path):
    try:
        # Add a prefix to the filename to
        # distinguish it from the uploaded file
        file_name = source_file_path.split("/")[-1]
        dest_file_name = os.path.join(local_dir_path, file_name)

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, source_file_path)

        print("Downloading to:", dest_file_name)

        # Open a file for writing bytes on the local system
        with open(dest_file_name, "wb") as data:
            # Download the file from Azure into a stream
            stream = file_client.download_file()
            # Write the stream to the local file
            data.write(stream.readall())

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


def main():
    local_image_path = os.getenv('IMAGE_PATH')
    local_image_label_path = os.getenv('IMAGE_LABEL_DIR')
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    share_name = os.getenv('AZURE_SHARE_NAME')
    label_dir_path = os.getenv('AZURE_LABEL_DIR_PATH')
    image_dir_path = os.getenv('AZURE_OBJECT_IMAGE_DIR_PATH')

    image_file_path_list = list_files_in_azure_directory(connection_string, share_name, image_dir_path)
    image_label_file_path_list = list_files_in_azure_directory(connection_string, share_name, label_dir_path)

    for file_path in image_file_path_list:
        download_azure_file(connection_string, share_name, file_path, local_image_path)

    for file_path in image_label_file_path_list:
        download_azure_file(connection_string, share_name, file_path, local_image_label_path)


if __name__ == '__main__':
    main()
