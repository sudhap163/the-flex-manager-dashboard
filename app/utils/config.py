import yaml
import sys

# read the configuration file from current working directory
configuration = {}
try:
    with open("./config.yaml", "r") as yaml_file:
        configuration = yaml.load(yaml_file, Loader=yaml.FullLoader)
    if configuration is None:
        raise Exception("empty data in configuration file")
    print("configuration loaded from ./config.yaml")
except Exception as e:
    print(f"error while loading the config.yaml: {e}")
    sys.exit(101)
    