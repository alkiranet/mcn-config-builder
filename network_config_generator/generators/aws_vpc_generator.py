from typing import List, Dict
from ..core.network_generator_base import NetworkGeneratorBase

class AWSVPCGenerator(NetworkGeneratorBase):
    '''
    Inherit from NetworkGeneratorBase and implement the generate method to build AWS specific portions of configuration.
    '''
    def generate(self) -> List[Dict]:
        num_vpcs = int(self.config['num_networks'])
        num_subnets = int(self.config['num_subnets'])
        return self.generate_network(num_vpcs, num_subnets, {
            'aws_account_id': self.config['account_id'],
            'region': self.config['region'],
            'credential': self.config['credential'],
            'cxp': self.config['cxp'],
            'group': self.config['group'],
            'segment': self.config['segment']
        })