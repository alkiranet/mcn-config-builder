import random
import string
import ipaddress
from typing import Dict, List

class NetworkGeneratorBase:
    '''
    A base class for network generators, providing common functionality like generating unique names and CIDRs.
    Methods include generating random and sequential CIDR blocks, validating subnets, and generating network configurations in '.yaml'
    '''
    generated_cidrs = set()

    def __init__(self, config: Dict):
        self.config = config

    def generate_unique_id(self, length: int = 6) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_random_cidr_16(self) -> str:
        while True:
            second_octet = random.randint(0, 100)
            cidr = f"10.{second_octet}.0.0/16"
            if cidr not in self.generated_cidrs:
                self.generated_cidrs.add(cidr)
                return cidr

    def generate_sequential_cidr_24(self, base_cidr: str, num_subnets: int) -> List[str]:
        first_octet, second_octet, _, _ = base_cidr.split('.')
        base_third_octet = random.randint(0, 100 - num_subnets)
        subnet_cidrs = [f"{first_octet}.{second_octet}.{base_third_octet + i}.0/24" for i in range(num_subnets)]
        
        if not self.validate_subnets(base_cidr, subnet_cidrs):
            raise ValueError("Subnet CIDRs are not valid within the VPC CIDR")

        return subnet_cidrs

    def validate_subnets(self, vpc_cidr: str, subnet_cidrs: List[str]) -> bool:
        vpc_network = ipaddress.ip_network(vpc_cidr)
        for subnet_cidr in subnet_cidrs:
            subnet_network = ipaddress.ip_network(subnet_cidr)
            if not subnet_network.subnet_of(vpc_network):
                return False
        return True

    def generate_network(self, num_networks: int, num_subnets: int, extra_config: Dict) -> List[Dict]:
        networks = []
        for _ in range(num_networks):
            network_cidr = self.generate_random_cidr_16()
            subnet_cidrs = self.generate_sequential_cidr_24(network_cidr, num_subnets)
            subnets = [{'name': f"subnet{index + 1}-{self.generate_unique_id()}", 'cidr': cidr} for index, cidr in enumerate(subnet_cidrs)]
            unique_id = self.generate_unique_id()
            network_name_prefix = self.config.get("prefix", "network")
            network = {
                'name': f'{network_name_prefix}-{unique_id}',
                'network_cidr': network_cidr,
                'create_network': True,
                'subnets': subnets,
                **extra_config
            }
            networks.append(network)
        return networks