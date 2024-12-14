locals {
  user_data = <<-EOT
  #!/bin/bash
  echo "export AWS_REGION=${var.region}" >> /etc/environment
  echo "export ENVIRONMENT=${var.environment}" >> /etc/environment
 
  
  aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${account_number}.dkr.ecr.eu-central-1.amazonaws.com
  python -m <run a python code to pull ECR:latest and run docker expose host 80 to container port 8080>

  source /etc/environment
  EOT
}

module "service-one-ec2" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name                        = "${var.environment}-service-one"
  ami                         = "ami-0ff8a91507f77f867"
  instance_type               = "t2.medium"
  key_name                    = "service-one"
  associate_public_ip_address = false
  subnet_id                   = var.public_subnet-a-id
  vpc_security_group_ids      = [module.ec2.service-one-ec2-security_group.security_group_id]
  user_data_base64            = base64encode(local.user_data)
  root_block_device           = [{ volume_size = 150 }]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  tags = var.default-tags
}