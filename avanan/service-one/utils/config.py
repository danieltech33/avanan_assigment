import os
import boto3
from .logger_config import setup_logger

logger = setup_logger(__name__)

class Config:
    def __init__(self):
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.env =os.getenv("ENVIRONMENT",'dev')
        # Initialize SSM client first
        self.ssm = boto3.client('ssm', region_name=self.aws_region)
        
        # Get SQS queue URL from SSM
        self.sqs_queue_url = self.get_ssm_parameter(f"${self.env}/email-metadata-queue-url")
        self.token_param_name = os.getenv('TOKEN_PARAM_NAME', f'/${self.env}/auth_token')
        
        if not self.sqs_queue_url:
            logger.error("Failed to retrieve SQS_QUEUE_URL from SSM")
            raise ValueError("Could not retrieve SQS_QUEUE_URL from SSM")
        
        self._auth_token = None
        self._env = None
            
        logger.info(f"Loaded configuration - Region: {self.aws_region}, Queue URL: {self.sqs_queue_url}")

    def get_ssm_parameter(self, name):
        try:
            response = self.ssm.get_parameter(Name=name, WithDecryption=True)
            return response['Parameter']['Value']
        except Exception as e:
            logger.error(f"Failed to fetch SSM parameter {name}: {str(e)}")
            raise

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
    

    @property
    def env(self):
        if not self._env:
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