import json

def read_json(file_name):
    with open(file_name, 'r') as f:
        return json.loads(f)

def write_json(filename, data, indent=4):
    with open(str(filename), 'w') as f:
        json.dump(data, f, indent=indent)        