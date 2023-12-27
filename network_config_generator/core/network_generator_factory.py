from typing import Dict
from .network_generator_base import NetworkGeneratorBase
from ..generators.aws_vpc_generator import AWSVPCGenerator
from ..generators.azure_vnet_generator import AzureVNetGenerator
from ..generators.gcp_vpc_generator import GCPVPCGenerator

class NetworkGeneratorFactory:
    '''
    Factory class that returns an instance of a specific network generator (AWS, Azure, GCP) based on input.
    '''
    @staticmethod
    def get_generator(cloud: str, config: Dict) -> NetworkGeneratorBase:
        if cloud == 'aws_vpc':
            return AWSVPCGenerator(config)
        elif cloud == 'azure_vnet':
            return AzureVNetGenerator(config)
        elif cloud == 'gcp_vpc':
            return GCPVPCGenerator(config)
        raise ValueError(f"Unsupported cloud type: {cloud}")