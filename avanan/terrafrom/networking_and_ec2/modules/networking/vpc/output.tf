output "public_subnet-a-id" {
  value = module.vpc.public_subnets[0]
}

output "public_subnet-b-id" {
  value = module.vpc.public_subnets[1]
}

output "private_subnet-a-id" {
  value = module.vpc.private_subnets[0]
}

output "private_subnet-b-id" {
  value = module.vpc.private_subnets[1]
}

output "vpc-id" {
  value = module.vpc.vpc_id
}

