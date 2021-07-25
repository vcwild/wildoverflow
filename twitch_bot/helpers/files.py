import yaml
from pathlib import Path


def read_yaml(file: str):
    ROOT_DIR = Path(__file__).parent.parent.parent

    directory = str(ROOT_DIR) + "/data/"

    with open(directory + file, 'r') as file:
        stream = file.read()
        data = yaml.load(stream, Loader=yaml.FullLoader)

    return data
