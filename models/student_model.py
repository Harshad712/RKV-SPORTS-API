from pydantic import BaseModel,HttpUrl
from typing import Optional
from datetime import datetime

class Student(BaseModel):
    student_name:str
    student_id:str
    year:str
    mail:str
    gender :str
    password : str
    #profile_url:str

class update_student(BaseModel):
    student_name: Optional[str]
    year : Optional[str]
    mail : Optional[str]
    gender : Optional[str]
    password : Optional[str]
   # profie_url:Optional[HttpUrl]