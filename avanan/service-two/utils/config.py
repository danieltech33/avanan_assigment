import os
import boto3
from .logger_config import setup_logger

logger = setup_logger(__name__)

class Config:
    def __init__(self):
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.sqs_queue_url = os.getenv('SQS_QUEUE_URL')
        self.s3_bucket = os.getenv('S3_BUCKET_NAME')
        self.token_param_name = os.getenv('TOKEN_PARAM_NAME', '/service2/auth_token')
        
        if not self.sqs_queue_url:
            logger.error("SQS_QUEUE_URL environment variable is not set")
            raise ValueError("SQS_QUEUE_URL environment variable is required")
        
        if not self.s3_bucket:
            logger.error("S3_BUCKET_NAME environment variable is not set")
            raise ValueError("S3_BUCKET_NAME environment variable is required")
        
        # Initialize SSM client
        self.ssm = boto3.client('ssm', region_name=self.aws_region)
        self._auth_token = None
            
        logger.info(f"Loaded configuration - Region: {self.aws_region}, Queue URL: {self.sqs_queue_url}")

    @property
    def auth_token(self):
        if not self._auth_token:
            try:
                response = self.ssm.get_parameter(
                    Name=self.token_param_name,
                    WithDecryption=True
                )
                self._auth_token = response['Parameter']['Value']
            except Exception as e:
                logger.error(f"Failed to fetch auth token from SSM: {str(e)}")
                raise
        return self._auth_token

config = Config() 