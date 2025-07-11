from typing import Optional, Union, Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from core.logging import error_logger

class DatabaseError(HTTPException):
    def __init__(
        self,
        detail: str = "Database operation failed",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(HTTPException):
    def __init__(
        self,
        resource: str,
        identifier: Union[str, int],
        detail: Optional[str] = None
    ):
        if detail is None:
            detail = f"{resource} with id {identifier} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ValidationError(HTTPException):
    def __init__(
        self,
        detail: Union[str, Dict[str, Any]]
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

def handle_db_error(error: SQLAlchemyError, context: Optional[str] = None) -> None:
    """
    Maneja errores de base de datos de manera centralizada.
    Registra el error y lanza una excepción HTTP apropiada.
    """
    error_msg = str(error)
    error_context = f" during {context}" if context else ""
    error_logger.error(f"Database error{error_context}: {error_msg}")
    
    if "duplicate key" in error_msg.lower():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El recurso ya existe"
        )
    elif "foreign key" in error_msg.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referencia inválida a un recurso relacionado"
        )
    else:
        raise DatabaseError()
