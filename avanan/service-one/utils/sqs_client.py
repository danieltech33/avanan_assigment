import boto3
import json
from .logger_config import setup_logger
from .config import config

logger = setup_logger(__name__)

class SQSClient:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name=config.aws_region)
        self.queue_url = config.sqs_queue_url
        
    def push_message(self, message_body, message_attributes=None):
        """
        Push a message to SQS queue
        
        Args:
            message_body (dict): The message to send
            message_attributes (dict, optional): Message attributes for the SQS message
            
        Returns:
            dict: Response from SQS containing MessageId if successful
            None: If sending fails
        """
        try:
            message_params = {
                'QueueUrl': self.queue_url,
                'MessageBody': json.dumps(message_body)
            }
            
            if message_attributes:
                message_params['MessageAttributes'] = message_attributes
                
            response = self.sqs.send_message(**message_params)
            
            logger.info(f"Successfully sent message to SQS. MessageId: {response.get('MessageId')}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send message to SQS: {str(e)}")
            raise 