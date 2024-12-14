module "ec2" {
  source             = "../modules/ec2"
  environment        = var.environment
  default-tags       = var.default-tags
  public_subnet-a-id = module.vpc.public_subnet-a-id
  vpc-id             = module.vpc.vpc-id
  region             = var.region
}