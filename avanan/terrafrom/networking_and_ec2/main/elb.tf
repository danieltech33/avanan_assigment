module "elb" {
  source                   = "../modules/networking/elb"
  environment              = var.environment
  default-tags             = var.default-tags
  public_subnet-a-id       = module.vpc.public_subnet-a-id
  public_subnet-b-id       = module.vpc.public_subnet-b-id
  private_subnet-a-id      = module.vpc.private_subnet-a-id
  private_subnet-b-id      = module.vpc.private_subnet-b-id
  vpc-id                   = module.vpc.vpc-id
  external_elb_certificate = var.external_alb_certificate
  instance_id              = module.ec2.instance_id
  ecs_sg_id                = module.ec2.security_group_id
}