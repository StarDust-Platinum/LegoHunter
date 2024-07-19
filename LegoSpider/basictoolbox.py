import json


def load_config(config_loc):
    try:
        with open(config_loc, "r+") as f:
            return json.load(f)
    except Exception as e:
        print(e)    
