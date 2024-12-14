
Here's the updated README with the required variables:
Terraform Infrastructure Projects
This repository contains two separate Terraform projects that need to be applied independently:

1. Networking and EC2 Project (networking_and_ec2/)
    This project sets up the core networking infrastructure and EC2 instances:

    Components:
    VPC with public and private subnets
    EC2 instances with security groups
    Elastic Load Balancer (ELB)
    ECR repositories for Docker images
    ACM certificate integration

    Required Variables:

        terraform apply \
        -var="environment=dev" \
        -var="region=eu-central-1" \
        -var="account_number=123456789012" \
        -var="external_alb_certificate=*.example.com" \
        -var='default-tags={
            Environment = "dev"
            Project     = "avanan"
            Owner       = "devops"
            ManagedBy   = "terraform"
        }'

2. Additional Resources Project (additional_resources/)

    This project manages auxiliary AWS resources:

    Components:
    S3 buckets for SQS payload storage
    SQS queues with DLQ (Dead Letter Queue) support
    SSM parameters for resource management

    Required Variables:

    terraform apply \
    -var="environment=dev" \
    -var="region=eu-central-1" \
    -var="account_number=123456789012" \
    -var='default-tags={
        Environment = "dev"
        Project     = "Avanan"
        Owner       = "Devops"
        ManagedBy   = "terraform"
    }'

Usage:

    Each project should be applied separately in the following order:
    1. First, apply the networking and EC2 project:

            cd networking_and_ec2/main
            terraform init
            terraform plan [with variables as shown above]
            terraform apply [with variables as shown above]
            
    2. Then, apply the additional resources project:

            cd additional_resources/main
            terraform init
            terraform plan [with variables as shown above]
            terraform apply [with variables as shown above]

    Prerequisites
    AWS credentials configured
    Terraform ~> 5.5.0
    Required variables set through CLI or terraform.tfvars
    Note
    Ensure you review the configuration and variables before applying either project, as they will create real resources in your AWS account. You can also store these variables in a terraform.tfvars file or use Terraform Cloud for better variable management.
