from motor.motor_asyncio import  AsyncIOMotorCollection
from typing import TypeVar
from models.student_model import Student,update_student
from repository.crud_repo import CrudRepository  
from utilities.utils import client
from fastapi import HTTPException


my_db = client['Rkv-Sports']
students_db = my_db.students

T = TypeVar('T', bound=Student)
class StudentRepository(CrudRepository[Student]):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
   
    


class UpdateStudentRepository(CrudRepository[update_student]):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__(collection)

# Instantiate the StudentRepository
student_ = StudentRepository(students_db)
update_student_ = UpdateStudentRepository(students_db)
