#!/usr/bin/env python3
# entry-point

import sys

# running python 3.6 or higher?
if sys.version_info < (3, 6):
    sys.exit("This script requires Python 3.6 or higher!")

import argparse
from network_config_generator.core.network_config_generator import NetworkConfigGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Configuration Generator")
    parser.add_argument("config_file", help="Path to the configuration file")
    args = parser.parse_args()

    generator = NetworkConfigGenerator(args.config_file)
    print(generator.generate_yaml())