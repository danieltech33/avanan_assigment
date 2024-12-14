module "sqs-payload-bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.14.0"

  bucket = "${var.environment}-sqs-payload-bucket"
  tags   = var.default-tags
}

resource "aws_ssm_parameter" "sqs-payload-bucket_arn" {
  name  = "${var.environment}/sqs-payload-bucket-arn"
  type  = "String"
  value = module.sqs-payload-bucket.s3_bucket_arn

  tags = var.default-tags
}