module "email-metadata-queue" {
  source = "terraform-aws-modules/sqs/aws"
  name   = "${var.environment}-email-metadata-queue"

  fifo_queue              = true
  create_dlq              = true
  create_dlq_queue_policy = true
  dlq_queue_policy_statements = {
    sns = {
      sid     = "owner_statement"
      actions = ["sqs:*"]
      principals = [
        {
          type        = "AWS"
          identifiers = ["arn:aws:iam::${var.account_number}:root"]
        }
      ]
    }
  }

  content_based_deduplication = true
  visibility_timeout_seconds  = 3600
  redrive_policy = {
    maxReceiveCount = 2
  }

  create_queue_policy = true
  queue_policy_statements = {
    sns = {
      sid     = "owner_statement"
      actions = ["sqs:*"]
      principals = [
        {
          type        = "AWS"
          identifiers = ["arn:aws:iam::${var.account_number}:root"]
        },
      ]
    }
  }
  tags = var.default-tags
}


resource "aws_ssm_parameter" "email_metadata_queue_url" {
  name  = "${var.environment}/email-metadata-queue-url"
  type  = "String"
  value = module.email-metadata-queue.queue_url

  tags = var.default-tags
}