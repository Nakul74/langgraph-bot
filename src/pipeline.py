from src.retriever_db import retrieval_db
from src.graph import retrieval_graph
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
import os
import logger_config
from dotenv import load_dotenv
load_dotenv()

# Initialize logger
logger = logger_config.get_logger(os.path.join('log_dir', 'logs.txt'))
graph_app = retrieval_graph.get_graph_workflow()

def process_question(question, retriever):
    """Process a single question to retrieve documents and generate an answer using the graph workflow."""
    try:
        logger.info(f"Processing question: {question}")
        inputs = {"question": question}

        # Invoke retriever to get relevant documents
        relevant_docs = retriever.invoke(question)
        if not relevant_docs:
            logger.warning(f"No relevant documents found for question: {question}")
            inputs["documents"] = []
        else:
            inputs["documents"] = [context.page_content for context in relevant_docs]
        
        # Pass the documents and question to the graph workflow for answer generation
        response = graph_app.invoke(inputs)
        answer = response.get('answer', 'No answer found.')
        
        logger.info(f"Answer for '{question}': {answer}")
        return question, answer

    except Exception as e:
        logger.error(f"Error processing question '{question}': {e}", exc_info=True)
        return question, "Error occurred while processing this question."

def run_pipeline(directory_path, questions_list):
    """Run the retrieval and graph workflow pipeline on a list of questions."""
    results_dict = {}
    
    try:
        logger.info(f"Starting pipeline with directory: {directory_path} and questions: {questions_list}")

        # Create the retriever using the provided directory path
        retriever = retrieval_db.create_retriever(directory_path)
        
        # Use ThreadPoolExecutor to process questions in parallel
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = {executor.submit(process_question, question, retriever): question for question in questions_list}

            # Collect results as each thread completes
            for future in as_completed(futures):
                question, answer = future.result()
                results_dict[question] = answer

        logger.info(f"Pipeline completed successfully.")
    
    except Exception as e:
        logger.error(f"Error running the pipeline: {e}", exc_info=True)
        raise RuntimeError("Pipeline execution failed.") from e
    
    return results_dict

if __name__ == '__main__':
    directory_path = 'sample_docs/sample_data'
    questions_list = [
        'who is Virat Kohli and when was he born?',
        'who is Sachin Tendulkar? Push the answer to Slack.'
    ]
    
    try:
        results = run_pipeline(directory_path, questions_list)
        print(results)
    except Exception as e:
        logger.error(f"Failed to run pipeline: {e}")
