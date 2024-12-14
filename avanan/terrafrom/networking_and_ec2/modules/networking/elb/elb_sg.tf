module "elb-external-security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 5.1.0"

  use_name_prefix = false
  name            = "${var.environment}-external-elb-security-group"
  description     = "security group for external elb"
  vpc_id          = var.vpc-id

  ingress_cidr_blocks = ["10.0.0.0/16", "0.0.0.0/0"]
  ingress_rules       = ["https-443-tcp"]
  ingress_with_cidr_blocks = [

    {
      rule        = "all-tcp"
      description = "access-from-everywhere"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  egress_cidr_blocks = ["0.0.0.0/0"]
  egress_rules       = ["all-tcp"]
  egress_with_source_security_group_id = [
    {
      from_port                = 8000
      to_port                  = 9000
      protocol                 = "tcp"
      description              = "access-to-ecs-sg"
      source_security_group_id = "${var.ecs_sg_id}"
    }
  ]
  tags = var.default-tags
}
