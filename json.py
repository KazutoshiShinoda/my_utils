import json

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
