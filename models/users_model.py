from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name:str
    user_id:str
    year:str
    mail:str

class update_user(BaseModel):
    name: Optional[str]
    year : Optional[str]
    mail : Optional[str]