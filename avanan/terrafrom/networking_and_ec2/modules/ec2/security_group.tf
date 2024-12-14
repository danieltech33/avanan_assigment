module "service-one-ec2-security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.17.1"

  use_name_prefix = false
  name            = "${var.environment}-service-one-ec2-sg"
  description     = "${var.environment}-service-one-ec2-security-group"
  vpc_id          = var.vpc-id
  egress_rules    = ["all-all"]

# ingress only from elb port 80
  ingress_with_source_security_group_id = [
    {
      from_port                = 80
      to_port                  = 80
      protocol                 = "tcp"
      description              = "HTTP from elb"
      source_security_group_id = module.elb.elb-external-security_group.security_group_id
    }
  ]

  tags = var.default-tags
}