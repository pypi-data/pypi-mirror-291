from ac.api.connection import Connection
from ac.cli.util import is_valid_source_path, get_file_or_folder_name, convert_to_absolute_path
from ac.conf.remote import remote_server
import os

import logging

training_dataset_base_default_path = "/mnt/weka/dvc_data"

class DataLoad:
    def __init__(self, source):
        self.source = source
    
    def load(self, dataset_name, dataset_version, dest):
        training_dataset_base_path = os.getenv("training_dataset_base_path", training_dataset_base_default_path)
        dest_path = training_dataset_base_path + '/' + dataset_name + "_" + dataset_version
        if is_valid_source_path(dest_path):
            print(f"dataset {dest_path} already exsits in our training data base path.")
            return True
        else:
            print(f"We are going to create the dataset {dest_path}")
        try:
            os.makedirs(dest_path, exist_ok=True)
            print(f"Directory '{dest_path}' was created successfully.")
        except OSError as error:
            raise Exception(f"Creation of the directory {dest_path} failed due to {error}.")

        conn = Connection(url=remote_server)
        data = {
            "dataset_name": dataset_name,
            "version": dataset_version,
            "dest": dest_path
        }
        try:
            response = conn.post("/get", json=data, stream=True)
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    print(chunk)
        except Exception as e:
            raise(f"Dataloader error occurred: {e}")