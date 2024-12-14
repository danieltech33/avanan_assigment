module "vpc" {
  source       = "../modules/networking/vpc"
  environment  = var.environment
  default-tags = var.default-tags
  region       = var.region
}