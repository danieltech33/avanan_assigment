import boto3
import json
import time
from datetime import datetime
from .logger_config import setup_logger
from .config import config

logger = setup_logger(__name__)

class HandleSqsMessages:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name=config.aws_region)
        self.s3 = boto3.client('s3', region_name=config.aws_region)
        self.queue_url = config.sqs_queue_url
        self.bucket_name = config.s3_bucket

    def listen_to_queue(self, process_func):
        """Listen to the SQS queue and process messages."""
        while True:
            try:
                # Receive a message from the queue
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=10,
                    VisibilityTimeout=30
                )

                messages = response.get('Messages', [])
                if messages:
                    for message in messages:
                        try:
                            logger.info(f"Processing message: {message['MessageId']}")
                            
                            # Process the message using provided function
                            process_func(message['Body'])
                            
                            # Delete the message after successful processing
                            self.sqs.delete_message(
                                QueueUrl=self.queue_url,
                                ReceiptHandle=message['ReceiptHandle']
                            )
                            logger.info(f"Message {message['MessageId']} processed and deleted")
                        except Exception as e:
                            logger.error(f"Failed to process message {message['MessageId']}: {str(e)}")
                else:
                    logger.info("No messages received. Retrying...")

            except Exception as e:
                logger.error(f"Error in message listener: {e}")
                time.sleep(5)  # Wait before retrying on error

            time.sleep(1)  # Short pause between polling