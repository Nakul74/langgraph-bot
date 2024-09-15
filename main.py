from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
import shutil
from typing import List
import time
import logger_config
from src import pipeline
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator

# Initialize logger
logger = logger_config.get_logger(os.path.join('log_dir', 'logs.txt'))

app = FastAPI()

# Directory to store uploaded files
UPLOAD_DIR = "sample_docs"

# Create the directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Initialize Prometheus instrumentation
PrometheusFastApiInstrumentator().instrument(app).expose(app)

@app.get("/")
async def home():
    logger.info("Home endpoint accessed")
    return JSONResponse(content={"message": "server is on"})

@app.post("/upload/")
async def upload_file_and_questions(
    file: UploadFile = File(...),
    questions: List[str] = Form(...)
):
    try:
        logger.info("Upload file and questions endpoint accessed")

        # Handle questions input in case they are passed as a single string
        if len(questions) == 1 and ',' in questions[0]:
            questions = questions[0].split(',')
        logger.info(f"Received questions: {questions}")

        # Create a unique folder using UUID
        save_dir = os.path.join(UPLOAD_DIR, str(uuid4()))
        os.makedirs(save_dir, exist_ok=True)
        logger.info(f"Created directory: {save_dir}")

        # Save the uploaded file to the created directory
        file_path = os.path.join(save_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File saved at: {file_path}")

        # Run the pipeline
        start_time = time.time()
        results = pipeline.run_pipeline(save_dir, questions)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Pipeline executed in {execution_time:.2f} seconds")

        # Clean up saved directory after processing
        shutil.rmtree(save_dir)
        logger.info(f"Directory {save_dir} deleted after processing")

        return JSONResponse(content=results)

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        # Raise HTTP exception for user-friendly message
        raise HTTPException(status_code=500, detail="An error occurred during file upload or processing.")
