from fastapi import APIRouter,HTTPException,Form,File,UploadFile
from utilities.utils import handle_exception
from controllers.student_controller import Students
from typing import Optional

app = APIRouter(tags=["Students"])

@app.post("/",summary="creates new users")
@handle_exception
async def create_student(student_name:str = Form(...) ,
                             student_id:str = Form(...),
                             year:str = Form(...),
                             mail:str = Form(...),
                             gender : str = Form(...),
                             password : str = Form(...),
                             profile_image :UploadFile = File(None)) ->dict:
    """An API EndPoint to Create New students"""
                    
    return await Students.create_student(student_name,student_id,year,mail,gender,password,profile_image)

@app.get("/",summary="fetches all users")
@handle_exception
async def get_all_students():
    """An API EndPoint to fetch all students."""

    return await Students.get_all_students()

@app.get("/{student_id}",summary="fetch single users by user_id")
@handle_exception
async def get_user_id(student_id:str ):
    """An API EndPoint fetch Single Student by student-id"""

    return await Students.get_student_id(student_id)

@app.put("/",summary="updates the user details")
@handle_exception
async def update_student_details(student_id:str,
                                  student_name :Optional[str] = None,
                                  year : Optional[str]= None,
                                  mail : Optional[str] = None,
                                  gender : Optional[str] = None,
                                  password : Optional[str] = None,
                                  profile_image :UploadFile = File(None)) -> dict:
    """An API EndPoint to Update student details."""

    return await Students.update_student_details(student_id,student_name,year,mail,gender,password,profile_image)

@app.post("/",summary = "Update the student profile")
@handle_exception
async def update_student_profile(student_id :str,profile_image :UploadFile = File(...)):
    """An API EndPoint to Update Student Profile."""
    
    return await Students.update_student_profile(student_id,profile_image)

@app.delete("/{student_id}",summary="deletes the users")
@handle_exception
async def delete_student(student_id:str):
    """An API EndPoint to delete the student."""

    return await Students.delete_student(student_id)