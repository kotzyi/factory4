import os
from azure.core.exceptions import (
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareDirectoryClient,
    ShareFileClient
)


def download(connection_string, share_name, source_dir_path, local_image_path):
    try:
        files = []
        parent_dir = ShareDirectoryClient.from_connection_string(conn_str=connection_string, share_name=share_name,
                                                                 directory_path=source_dir_path)
        for item in list(parent_dir.list_directories_and_files()):
            if item['is_directory']:
                os.makedirs(os.path.join(local_image_path, item['name']))
                download(
                    connection_string,
                    share_name,
                    os.path.join(source_dir_path, item['name']),
                    os.path.join(local_image_path, item['name']))
            else:
                source_file_path = os.path.join(source_dir_path, item['name'])
                download_from_azure_file_share(connection_string, share_name, source_file_path, local_image_path)

        return files
    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


def download_from_azure_file_share(connection_string, share_name, source_file_path, local_dir_path):
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
    local_image_path = os.getenv('IMAGE_DIR_PATH')
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    share_name = os.getenv('AZURE_SHARE_NAME')
    source_dir_path = os.getenv('AZURE_CLASS_IMAGE_DIR_PATH')

    download(connection_string, share_name, source_dir_path, local_image_path)


if __name__ == '__main__':
    main()
