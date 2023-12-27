import os
import configparser
import yaml
from typing import Dict, List
from .network_generator_factory import NetworkGeneratorFactory

class NetworkConfigGenerator:
    '''
    This class is responsible for processing a configuration file
    and generating .yaml files for different cloud network configurations.
    '''
    def __init__(self, config_file: str):
        self.config = self.read_config(config_file)

    def read_config(self, config_file: str) -> Dict:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def generate_yaml(self) -> str:
        configurations = {}
        for cloud in ['aws_vpc', 'azure_vnet', 'gcp_vpc']:
            if cloud in self.config:
                generator = NetworkGeneratorFactory.get_generator(cloud, self.get_config_section(cloud))
                configurations[cloud] = generator.generate()

        for cloud, data in configurations.items():
            file_name = self.config[cloud]['file_name']
            self.process_configurations(cloud, data, file_name)

        return "Configuration files generated/updated successfully."

    def process_configurations(self, cloud_type: str, config_data: List[Dict], file_name: str):
        file_path = f"{file_name}.yaml"
        if os.path.exists(file_path):
            self.append_configurations(cloud_type, config_data, file_path)
        else:
            self.write_configurations({cloud_type: config_data}, file_path)

    def append_configurations(self, cloud_type: str, config_data: List[Dict], file_path: str):
        with open(file_path, 'r') as file:
            existing_data = yaml.safe_load(file) or {}

        if cloud_type in existing_data:
            existing_data[cloud_type].extend(config_data)
        else:
            existing_data[cloud_type] = config_data

        self.write_configurations(existing_data, file_path)

    def write_configurations(self, config_data: Dict, file_path: str):
        with open(file_path, "w") as file:
            yaml.safe_dump(config_data, file, indent=2, sort_keys=False)

    def get_config_section(self, section: str) -> Dict:
        return {key: self.config[section][key] for key in self.config[section]}