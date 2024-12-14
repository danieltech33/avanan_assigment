resource "aws_elb" "ELB" {
  name    = "${var.environment}-external-ELB"
  subnets = [
    var.public_subnet-a-id,
    var.public_subnet-b-id
  ]
  security_groups = [module.elb-external-security_group.security_group_id]
  idle_timeout    = 60
  tags            = var.default-tags

  listener {
    instance_port      = 80
    instance_protocol  = "HTTP"
    lb_port           = 443
    lb_protocol       = "HTTPS"
    ssl_certificate_id = data.aws_acm_certificate.amazon_issued.id
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout            = 3
    target             = "HTTP:80/health_check"
    interval           = 30
  }

  cross_zone_load_balancing    = true
  connection_draining         = true
  connection_draining_timeout = 300

  instances = var.instance_id
}