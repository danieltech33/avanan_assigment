module "s3" {
  source         = "../modules/s3"
  environment    = var.environment
  default-tags   = var.default-tags
  account_number = var.account_number
  region         = var.region
  
  
}