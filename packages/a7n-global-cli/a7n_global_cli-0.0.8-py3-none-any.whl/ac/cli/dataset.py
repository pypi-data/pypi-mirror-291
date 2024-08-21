import click

from ac.cli.util import click_group
from ac.api.connection import Connection
from ac.conf.remote import remote_server, remote_storage_prefix
from pprint import pprint
from tabulate import tabulate
import os
import sys
import signal


def is_valid_source_path(path: str) -> bool:
    """Check if the source path is valid."""
    if not os.path.exists(path):
        print(f"Your source {path} is invalid, path not exists")
        return False
    if not os.access(path, os.R_OK):
        print(f"Your source {path} is invalid, path not access")
        return False
    if not path.startswith(remote_storage_prefix):
        print(f"Your source {path} is invalid, path is not prefix of {remote_storage_prefix} ")
        return False
    return True

def convert_to_absolute_path(path: str) -> str:
    """Convert a relative path to an absolute path."""
    return os.path.abspath(path)

def get_file_or_folder_name(path: str) -> str:
    """Get the file name with extension or folder name from the given path."""
    if os.path.isdir(path):
        return os.path.basename(path)  # Return folder name
    elif os.path.isfile(path):
        return os.path.basename(path)  # Return file name with extension
    else:
        raise ValueError(f"Invalid path {path}")

@click_group()
def ds():
    pass


@ds.command()
@click.option("--source_path", "-s", type=str, help="Source path ot the dataset", required=True)
@click.option("--version", "-v", type=str, help="Dataset version you want to register", required=True)
@click.option("--message", "-m", type=str, help="Note of the dataset")
@click.pass_context
def add(ctx, source_path, version, message):
    if not is_valid_source_path(source_path):
        sys.exit(1) 
    abs_path = convert_to_absolute_path(source_path)
    dataset_name = get_file_or_folder_name(abs_path)
    conn = Connection(url=remote_server)
    data = {
        "dataset_name": dataset_name,
        "version": version,
        "source_path": abs_path,
        "dest_path": "local",
        "message": message
    }
    print(data)
    try:
        response = conn.post("/add", json=data, stream=True)
        
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                print(chunk)
    except KeyboardInterrupt:
        print(f"The dataset add operation may occur backend, you can check it later by `a7n ds list -n {dataset_name} -v {version}` ")
        sys.exit(0)
    except Exception as e:
        print(f"Error occurred: {e}")

@ds.command()
@click.option("--name", "-n", help="Name of the datasets in remote",)
def list(name):
    conn = Connection(url=remote_server)
    response = conn.get("/query_datasets", params={"dataset_name": name})
    
    if response.status_code == 200:
        data = response.json()
        headers = [
            "Created At", "Dataset Name", 
            "Dataset Version",  "Message"
        ]
        table = [
            [
                item["created_at"], item["dataset_name"],
                item["dataset_version"],
                item["message"]
            ] for item in data
        ]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("Failed to retrieve datasets. Status code:", response.status_code)


@ds.command()
@click.option("--name", "-n", help="Name of the datasets in remote", required=True)
@click.option("--version", "-v", help="Version of the dataset")
@click.option("--dest", "-d", help="Destination path you want to creat the dataset")
@click.pass_context
def get(ctx, name, version, dest):
    if not is_valid_source_path(dest):
        sys.exit(1) 

    abs_path = convert_to_absolute_path(dest)
    conn = Connection(url=remote_server)
    data = {
        "dataset_name": name,
        "version": version,
        "dest_path": abs_path
    }
    try:
        response = conn.post("/get", json=data, stream=True)
        
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                print(chunk)
    except KeyboardInterrupt:
        print(f"The dataset get operation may occur backend, you can check it later by `ls {abs_path}` ")
        sys.exit(0)
    except Exception as e:
        print(f"Error occurred: {e}")

def add_command(cli_group):
    cli_group.add_command(ds)
