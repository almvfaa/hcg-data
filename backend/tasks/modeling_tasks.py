# backend/tasks/modeling_tasks.py
import pandas as pd
from worker import celery_app
from services.segmentation import SegmentationService
from db.session import SessionLocal

@celery_app.task(name="tasks.run_abc_analysis_task")
def run_abc_analysis_task() -> list:
    """
    A Celery task that performs ABC segmentation analysis.
    
    This function will be executed asynchronously by a Celery worker.
    It creates its own database session to ensure it's independent
    of the web server processes.
    """
    db = SessionLocal()
    try:
        # Instantiate the service with a new database session
        service = SegmentationService(db=db)
        
        # Run the analysis
        results_df = service.run_abc_analysis()
        
        # Celery works best with JSON-serializable results.
        # We convert the DataFrame to a list of dictionaries.
        # Note: Be mindful of large result sets, as they will be stored in your result backend (Redis).
        return results_df.to_dict(orient='records')
    except Exception as e:
        # It's good practice to log errors that occur within tasks.
        # You might want to add more robust logging here.
        print(f"An error occurred in ABC analysis task: {e}")
        # Reraise the exception so Celery can mark the task as FAILED.
        raise
    finally:
        # Ensure the database session is always closed.
        db.close()
