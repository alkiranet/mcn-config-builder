# MCN - Config Builder
When building a new environment for _proof-of-concepts_, _connectivity testing_, or any other number of use cases, why worry about trivial details like _subnetting_ or naming conventions? This script was built to be used with the [aws-builder](https://registry.terraform.io/modules/alkiranet/aws-builder/alkira/latest), [azure-builder](https://registry.terraform.io/modules/alkiranet/azure-builder/alkira/latest), and [gcp-builder](https://registry.terraform.io/modules/alkiranet/connector-gcp/alkira/latest) Terraform modules.

## What does it do?
This script will generate:
- **Unique names** for each resource:

  ```python
   def generate_unique_id(self, length: int = 6) -> str:
        characters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
  ```
- **Random _/16_ CIDRs** between **0-100**

  ```python
   def generate_random_cidr_16(self) -> str:
        while True:
            second_octet = random.randint(0, 100)
            cidr = f"10.{second_octet}.0.0/16"
            if cidr not in self.generated_cidrs:
                self.generated_cidrs.add(cidr)
                return cidr  
  ```
- **Sequential _/24_ subnets** from the _/16_ between **0-100**

  ```python
  def generate_sequential_cidr_24(self, base_cidr: str, num_subnets: int) -> List[str]:
        first_octet, second_octet, _, _ = base_cidr.split('.')
        base_third_octet = random.randint(0, 100 - num_subnets)
        subnet_cidrs = [f"{first_octet}.{second_octet}.{base_third_octet + i}.0/24" for i in range(num_subnets)]
  ```

:warning: The cloud network CIDR _(at the VPC/VNet/VCN level)_ should not overlap with the CIDR used for the [alkira_segment](https://registry.terraform.io/providers/alkiranet/alkira/latest/docs/resources/segment). This script uses a random integer selected from the range **0, 100** for the second octet of the _/16_. The segment CIDR should be in the range of 10.**101-254**.x.0/24.

## Install dependencies
```shell
pip3 install -r requirements.txt
```

## Define input configuration
This script uses an input configuration file _(see example.cnf)_ to define basic configuration criteria.

```shell
[aws_vpc]
num_networks = 8 # number of VPCs to provision
num_subnets = 3 # number of subnets per VPC
account_id = 12345678 # AWS specific account id
region = us-east-2 # cloud specific region
credential = aws # Alkira credential name
cxp = us-east-2 # Alkira Cloud Exchange Point
group = nonprod # Alkira group name
segment = business # Alkira segment name
file_name = networks # name of file to generate

[azure_vnet]
num_networks = 5
num_subnets = 3
resource_group = resource-group-name # Azure specific resource group
region = eastus
credential = azure
cxp = us-east-2
group = nonprod
segment = business
file_name = networks

[gcp_vpc]
num_networks = 4
num_subnets = 3
region = us-east4
credential = gcp
cxp = us-east-2
group = nonprod
segment = business
file_name = networks
```

## Generate configuration files
To generate the respective _.yaml_ files, simply run:

```shell
./run.sh example.cnf
```

## Using the configuration file
Once the configuration file is generated, it can then be used with _one_ or _all_ of the above-linked Terraform modules. In the above example, we used the name _networks_ which would generate _networks.yaml_. We can then use that file to build network infrastructure:

```hcl
module "aws_vpc" {
  source  = "alkiranet/aws-builder/alkira"

  # Path to .yml configuration files
  config_file = "./networks.yaml"

}

module "azure_vnet" {
  source  = "alkiranet/azure-builder/alkira"

  # Path to .yml configuration files
  config_file = "./networks.yaml"

}

module "gcp_vpc" {
  source  = "alkiranet/gcp-builder/alkira"

  # Path to .yml configuration files
  config_file = "./networks.yaml"

}
```