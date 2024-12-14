# this searches an exsiting certificate by var in aws - issuing one can take time so i used an existing one
  
data "aws_acm_certificate" "amazon_issued" {
  domain      = var.external_elb_certificate
  types       = ["AMAZON_ISSUED", "IMPORTED"]
  most_recent = true
} 