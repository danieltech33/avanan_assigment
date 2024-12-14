from .logger_config import setup_logger
from .config import config

logger = setup_logger(__name__)

def validate_payload(payload):
    """
    Validate the incoming payload structure and token
    
    Args:
        payload (dict): The payload to validate
        
    Returns:
        bool: True if validation passes
        
    Raises:
        ValueError: If validation fails with specific error message
    """
    # Check if basic structure exists
    if not isinstance(payload, dict):
        raise ValueError("Invalid payload format")
        
    if 'data' not in payload or 'token' not in payload:
        raise ValueError("Missing required fields: 'data' and 'token'")
        
    # Validate token
    if payload['token'] != config.auth_token:
        raise ValueError("Invalid authentication token")
        
    # Validate data fields
    required_fields = ['email_subject', 'email_sender', 'email_timestream', 'email_content']
    data = payload['data']
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required data fields: {', '.join(missing_fields)}")
        
    # Validate that no fields are empty
    empty_fields = [field for field in required_fields if not data[field]]
    if empty_fields:
        raise ValueError(f"Empty data fields not allowed: {', '.join(empty_fields)}")
    
    return True 