locals {
  ecr_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "EC2ECRImageRetrievalPolicy",
          "Effect" : "Allow",
          "Principal" : {
            "AWS" : [
              "arn:aws:iam::${var.account_number}:root"
            ],
            "Service" : "ec2.amazonaws.com"
          },
          "Action" : "ecr:*"
        }
      ]
    }
  )
}


module "service-one" {
  source                          = "terraform-aws-modules/ecr/aws"
  version                         = "~> 1.6.0"
  repository_name                 = "${var.environment}-vector_store"
  create_lifecycle_policy         = false
  repository_image_tag_mutability = "MUTABLE"
  repository_encryption_type      = "AES256"
  create_repository_policy        = false
  repository_policy               = local.ecr_policy
  tags                            = var.default-tags
}

module "service-two" {
  source                          = "terraform-aws-modules/ecr/aws"
  version                         = "~> 1.6.0"
  repository_name                 = "${var.environment}-mail_separation"
  create_lifecycle_policy         = false
  repository_image_tag_mutability = "MUTABLE"
  repository_encryption_type      = "AES256"
  create_repository_policy        = false
  repository_policy               = local.ecr_policy
  tags                            = var.default-tags
}