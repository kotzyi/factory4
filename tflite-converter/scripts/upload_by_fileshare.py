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
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--share_name", default="", type=str, help="share name of azure fileshare")
    parser.add_argument("-d", "--dir_path", default="", type=str, help="directory path of azure fileshare")
    parser.add_argument("-l", "--local_dir_path", default="", type=str, help="local file path of model file")
    parser.add_argument("-f", "--model_file_name", default="model.tflite", type=str, help="model file name")
    args = parser.parse_args()

    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    local_file_path = os.path.join(args.local_dir_path, args.model_file_name)
    dest_file_path = os.path.join(args.dir_path, args.model_file_name)
    upload_local_file(connection_string, local_file_path, args.share_name, dest_file_path)


if __name__ == '__main__':
    main()
