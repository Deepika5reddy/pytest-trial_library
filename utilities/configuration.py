# utilities/configuration.py
import configparser
import os
from utilities.resources import resources

def get_trial_search_base_url():
    config = configparser.ConfigParser()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(root_dir, "utilities", "properties.ini")
    config.read(config_path)

    endpoint_base = config["API_URL"]["endpoint"]
    return endpoint_base + resources.trial_search
