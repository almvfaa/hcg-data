from fastapi import Depends
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..services.segmentation import SegmentationService

def get_segmentation_service(db: Session = Depends(get_db)) -> SegmentationService:
    """
    Dependency provider for the SegmentationService.
    
    Creates a SegmentationService instance with a database session.
    """
    return SegmentationService(db=db)

