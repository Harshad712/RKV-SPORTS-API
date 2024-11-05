from pydantic import BaseModel,Field,HttpUrl
from typing import Optional
from datetime import datetime


class Banner_model(BaseModel):
    created_at:datetime = Field(default_factory=datetime.now)
    banner_id:str
    #banner_link : url
    class config:
        arbitrary_types_allowed = True
   