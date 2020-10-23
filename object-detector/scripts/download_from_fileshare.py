import os
import argparse
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


def list_files_in_azure_directory(connection_string, share_name, dir_path):
    try:
        files = []
        parent_dir = ShareDirectoryClient.from_connection_string(conn_str=connection_string, share_name=share_name,
                                                                 directory_path=dir_path)
        for item in list(parent_dir.list_directories_and_files()):
            if not item['is_directory']:
                files.append(item['name'])
        return files
    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


def download_azure_file(connection_string, share_name, dir_path, file_name, local_dir_path):
    try:
        # Build the remote path
        source_file_path = dir_path + "/" + file_name

        # Add a prefix to the filename to
        # distinguish it from the uploaded file
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--share_name", default="", type=str, help="share name of azure fileshare")
    parser.add_argument("-id", "--image_dir_path", default="", type=str, help="directory path of azure fileshare")
    parser.add_argument("-ld", "--label_dir_path", default="", type=str, help="directory path of azure fileshare")
    parser.add_argument("-i", "--local_image_path", default="", type=str, help="local file path of download files")
    parser.add_argument("-l", "--local_image_label_path", default="", type=str, help="local image label file path of download files")

    args = parser.parse_args()

    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    share_name = args.share_name
    image_dir_path = args.image_dir_path
    label_dir_path = args.label_dir_path
    local_image_path = args.local_image_path
    local_image_label_path = args.local_image_label_path
    image_file_list = list_files_in_azure_directory(connection_string, share_name, image_dir_path)
    image_label_file_list = list_files_in_azure_directory(connection_string, share_name, label_dir_path)

    for file_name in image_file_list:
        download_azure_file(connection_string, share_name, image_dir_path, file_name, local_image_path)

    for file_name in image_label_file_list:
        download_azure_file(connection_string, share_name, label_dir_path, file_name, local_image_label_path)


if __name__ == '__main__':
    main()
