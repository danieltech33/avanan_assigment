import os
import datetime
from utils.logger_config import setup_logger
from utils.sqs_client import SQSClient
from utils.config import config
from utils.validation import validate_payload

# Get logger instance
logger = setup_logger(__name__)

# Initialize SQS client
sqs_client = SQSClient()

def recieve_message(payload):
    """Process incoming message and publish to SQS if valid"""
    try:
        logger.info("Processing incoming message")
        
        # Validate payload
        validate_payload(payload)
        
        # Extract data for SQS
        message_data = payload['data']
        
        # Send to SQS
        response = sqs_client.push_message(message_data)
        
        logger.info(f"Successfully processed message. SQS MessageId: {response.get('MessageId')}")
        return {
            "status": "success",
            "message": "Message processed and sent to queue",
            "messageId": response.get('MessageId')
        }
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise
    