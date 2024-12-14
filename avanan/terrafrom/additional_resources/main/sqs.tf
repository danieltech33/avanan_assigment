module "sqs" {
  source         = "../modules/sqs"
  environment    = var.environment
  default-tags   = var.default-tags
  account_number = var.account_number
  region         = var.region
  
  
}