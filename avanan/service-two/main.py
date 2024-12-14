from utils.logger_config import setup_logger
from utils.sqs_client import HandleSqsMessages
from datetime import datetime
import json

logger = setup_logger(__name__)

class EmailProcessor:
    def __init__(self):
        self.handler = HandleSqsMessages()
        self.s3 = self.handler.s3
        self.bucket_name = self.handler.bucket_name

    def save_to_s3(self, content, email_subject):
        """Save message content to S3"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Create a safe filename from the subject
            safe_subject = "".join(x for x in email_subject if x.isalnum() or x in (' ', '-', '_')).strip()
            key = f"emails/{timestamp}_{safe_subject}.txt"
            
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType='text/plain'
            )
            logger.info(f"Successfully saved message to S3: {key}")
            return key
        except Exception as e:
            logger.error(f"Error saving to S3: {str(e)}")
            raise

    def process_message(self, message_body):
        """Process a single message"""
        try:
            # Parse the message body
            data = json.loads(message_body)
            
            # Extract email content and subject
            email_content = data.get('email_content', '')
            email_subject = data.get('email_subject', 'no_subject')
            
            # Save to S3
            s3_key = self.save_to_s3(email_content, email_subject)
            logger.info(f"Message processed and saved to S3: {s3_key}")
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def start(self):
        """Start processing messages"""
        self.handler.listen_to_queue(self.process_message)

if __name__ == "__main__":
    logger.info("Starting Service-two")
    processor = EmailProcessor()
    processor.start()