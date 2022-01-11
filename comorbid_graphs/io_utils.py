import yaml
import json


def read_from_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_yaml(filepath, data):
    with open(filepath, "w+") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def read_from_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def write_json(filepath, data):
    with open(filepath, "w+") as f:
        json.dump(data, f)
