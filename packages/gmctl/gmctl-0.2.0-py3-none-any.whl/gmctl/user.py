from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from gmctl.gmclient import GitmoxiClient
import logging
from gmctl.utils import print_table

logger = logging.getLogger(__name__)

class UserRole(BaseModel):
    user_id: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)

    def __str__(self) -> str:
        return self.model_dump_json()

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
