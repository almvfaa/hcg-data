# backend/api/v1/endpoints/tasks.py
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from ...worker import celery_app

router = APIRouter()

@router.get("/{task_id}", summary="Check the status and result of a Celery task")
def get_task_status(task_id: str):
    """
    Retrieves the status and result of a background task.
    The frontend will poll this endpoint to see if the task is complete.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.state == 'SUCCESS':
        # The task completed successfully.
        return {
            "task_id": task_id,
            "status": task_result.state,
            "result": task_result.result
        }
    elif task_result.state == 'FAILURE':
        # The task failed. Return a 500 error with the exception details.
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "task_id": task_id,
                "status": task_result.state,
                # It's better to return a generic error message to the client
                # and log the full exception on the server for security.
                "error": "An error occurred during task execution.",
                # "detail": str(task_result.info) # Uncomment for debugging
            }
        )
    else:
        # The task is still pending, in progress, or in an unknown state.
        return {
            "task_id": task_id,
            "status": task_result.state,
            "result": None
        }
