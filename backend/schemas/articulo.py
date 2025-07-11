from typing import Optional
from pydantic import BaseModel

# -------------------
# Base Schema
# -------------------
class ArticuloBase(BaseModel):
    """
    Fields that are common to all article-related operations.
    This is the base that other schemas will inherit from.
    """
    codigo_articulo: str
    descripcion_articulo: str
    unidad_medida: Optional[str] = None
    partida_especifica: int

# -------------------
# Create Schema
# -------------------
class ArticuloCreate(ArticuloBase):
    """
    Schema for creating a new article.
    Inherits all fields from ArticuloBase.
    You could add create-specific fields here if needed.
    """
    pass

# -------------------
# Update Schema
# -------------------
class ArticuloUpdate(BaseModel):
    """
    Schema for updating an existing article.
    All fields are optional, so clients can update just the fields they need to.
    The primary key (codigo_articulo) is not included to prevent it from being updated.
    """
    descripcion_articulo: Optional[str] = None
    unidad_medida: Optional[str] = None
    partida_especifica: Optional[int] = None


# -------------------
# Read Schema
# -------------------
class Articulo(ArticuloBase):
    """
    Schema for reading/returning an article from the API.
    This represents the full article object as it exists in the database.
    """
    # This schema doesn't add new fields but is defined for consistency.
    # If your DB model had fields you wanted to return but not create/update,
    # you would add them here (e.g., created_at, updated_at).
    
    class Config:
        """
        Pydantic configuration to enable mapping from ORM models.
        (Previously orm_mode = True)
        """
        from_attributes = True
