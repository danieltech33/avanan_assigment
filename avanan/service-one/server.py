from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from main import recieve_message
from utils.logger_config import setup_logger
import uvicorn

# Get logger instance
logger = setup_logger(__name__)

app = FastAPI()

@app.get("/health_check")
def health_check():
    logger.info("Health check endpoint called")
    return {"Response": "ok"}

@app.post("/")
def read_item(event_dict: dict, context: str = None, background_tasks: BackgroundTasks = None):
    try:
        logger.info("Processing incoming request")
        background_tasks.add_task(recieve_message, event_dict, context)
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Success"}
        }
        logger.info("Request accepted for processing")
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise


# remember in docker run map container port 8080 to host port 80 (fastApi run on 8080)
# if __name__ == '__main__':