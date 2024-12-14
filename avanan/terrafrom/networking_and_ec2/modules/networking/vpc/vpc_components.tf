module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0.0"
  name    = "${var.environment}-vpc"
  cidr    = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  map_public_ip_on_launch = true
  enable_nat_gateway      = true
  single_nat_gateway      = true
  one_nat_gateway_per_az  = false

  enable_dns_hostnames = true
  enable_dns_support   = true
  tags                 = var.default-tags

  
}