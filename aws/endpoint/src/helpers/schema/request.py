"""Request pydantic model"""

from typing import Optional

from pydantic import BaseModel


class RequestModel(BaseModel):
    """Model to check if an input request is valid or not"""

    prompt: str
    duration: Optional[float] = 8.0
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 0.0
    top_k: Optional[int] = 250
    cfg_coefficient: Optional[float] = 3.0
