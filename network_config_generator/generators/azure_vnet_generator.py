from typing import List, Dict
from ..core.network_generator_base import NetworkGeneratorBase

class AzureVNetGenerator(NetworkGeneratorBase):
    '''
    Inherit from NetworkGeneratorBase and implement the generate method to build Azure specific portions of configuration.
    '''
    def generate(self) -> List[Dict]:
        num_vnets = int(self.config['num_networks'])
        num_subnets = int(self.config['num_subnets'])
        return self.generate_network(num_vnets, num_subnets, {
            'resource_group': self.config['resource_group'],
            'region': self.config['region'],
            'credential': self.config['credential'],
            'cxp': self.config['cxp'],
            'group': self.config['group'],
            'segment': self.config['segment']
        })