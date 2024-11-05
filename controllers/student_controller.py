from fastapi import HTTPException,Form,File,UploadFile
from bson import ObjectId
from utilities.utils import client
from utilities.git_hub_utilities import upload_to_github,delete_file_from_github
from models.student_model import Student,update_student
from typing import Optional
import logging

my_db = client['Rkv-Sports']
students_db = my_db.students

class Students():
    @staticmethod
    async def create_student(student_name:str = Form(...) ,
                             student_id:str = Form(...),
                             year:str = Form(...),
                             mail:str = Form(...),
                             gender : str = Form(...),
                             password : str = Form(...),
                             profile_image :UploadFile = File(None)) ->dict:

        """
    Creates a new user document in the database if a user with the same ID does not already exist.

    Args:
        name (str): The name of the user.
        user_id (str): The unique identifier for the user.
        year (str): The year associated with the user (e.g., joining year).
        mail (str): The email address of the user.

    Returns:
        dict: A success message indicating the user has been created.

    Raises:
        HTTPException: If a user with the same ID already exists (status code 409).
        HTTPException: If there is an error while creating the new user (status code 400).
    """

        student_exists = await students_db.find_one({"student_id":student_id})
        if student_exists :
            raise HTTPException(
                status_code = 409,
                detail = "A Student already found with the same Id."
            )
       
        student = Student(
            student_name= student_name,
            student_id = student_id,
            year = year,
            mail = mail,
            gender = gender,
            password= password
        )
        student = student.model_dump()

        if profile_image:

            profile_image_size = len(await profile_image.read())
            max_length = 10*1024*1024
            if profile_image_size > max_length:
                raise HTTPException(status_code=413, detail="File Size Exceeds the limit 10 MB.")

            profile_image_content = await profile_image.read()
            profile_image_response = await upload_to_github(profile_image_content,profile_image.filename)
            if profile_image_response.status_code ==201 :
                 profile_url = profile_image_response.json().get("content", {}).get("html_url", "")
                 student["profile_url"] = profile_url
            else :
                raise HTTPException(status_code=400,detail="Error While Uploading The File Into Github")

        result = await students_db.insert_one(student)
        if result.inserted_id:
            student["_id"] = str(result.inserted_id)
            return {"message":"Student Created Successfully"}
        else:
            raise HTTPException(status_code=400,detail = "Error While creating the new student")
        

    @staticmethod
    async def get_all_students() -> list :

        """
        Retrieves all student documents from the database.

        Returns:
            list: A list of student documents with their '_id' fields converted to strings.

        Raises:
            HTTPException: If no students are found in the database (status code 404).
        """
        students=[]
        async for student in  students_db.find():
            student["_id"] = str(student["_id"])
            students.append(student)
        if not students:
            raise HTTPException(
                status_code=404,
                detail = "No Users Found."
            )
        return students
    
    @staticmethod
    async def get_student_id(student_id:str) -> dict:

        """
        Retrieves a student document from the database by the given student ID.

        Args:
            student_id (str): The unique identifier of the student to be retrieved.

        Returns:
            dict: The student document if found.

        Raises:
            HTTPException: If no student is found with the given ID (status code 404).
        """
        user =await  students_db.find_one({"student_id":student_id})
        if not user:
            raise HTTPException(
                status_code=404,
                detail="No user found with the given id."
            )
        user["_id"] = str(user["_id"])

        return user
    
    @staticmethod
    async def update_student_details(student_id:str,
                                  student_name :Optional[str] = None,
                                  year : Optional[str]= None,
                                  mail : Optional[str] = None,
                                  gender : Optional[str] = None,
                                  password : Optional[str] = None) -> dict:
        
        """
    Updates the details of an existing user in the database.

    Args:
        user_id (str): The unique identifier of the user to be updated.
        name (Optional[str], optional): The new name of the user. Defaults to None.
        year (Optional[str], optional): The new year associated with the user. Defaults to None.
        mail (Optional[str], optional): The new email address of the user. Defaults to None.

    Returns:
        dict: A success message indicating that the user has been updated.

    Raises:
        HTTPException: If the user is not found (status code 404).
        HTTPException: If no data is provided for the update (status code 400).
        HTTPException: If the user is found but no modifications were made (status code 404).
        HTTPException: On successful update (status code 201).
    """
        user_exists = await students_db.find_one({"student_id":student_id})
        if not user_exists :
            raise HTTPException(
                status_code = 404,
                detail = "User not found with the given id."
            )
        
        user = update_student(
            student_name = student_name,
            year = year,
            mail = mail,
            gener = gender,
            password = password

        )
        user = user.model_dump()
       
        user = {k:v  for k,v in user.items() if v is not None}
        if not user :
            raise HTTPException(
                status_code= 400,
                detail = "No data Provided for update"
            )
        user_update = await students_db.update_one(
            {"student_id":student_id},
            {"$set":user}
        )
        if user_update.modified_count == 0:
            raise HTTPException(status_code=404, detail="No User found with the given ID or no changes made")
        
        return{"message":"User updated Successfully."}
    
    @staticmethod
    async def update_student_profile(student_id:str,profile_image:UploadFile = File(...)):
        
        """
    Updates the profile image of a student in the database.

    This function retrieves a student document from the database using the provided student ID,
    checks if the student exists, and updates their profile image URL if a new image is provided.
    The old image is deleted from GitHub, and the new image is uploaded.

    Args:
        student_id (str): The unique identifier of the student whose profile image is to be updated.
        profile_image (UploadFile, optional): The new profile image file to be uploaded. 
                                              This is required and must be provided as a file upload.

    Raises:
        HTTPException: If the student with the given ID is not found (status code 404).
        HTTPException: If there is a conflict while deleting the old profile image from GitHub (status code 409).
        HTTPException: If there is an error while uploading the new profile image (status code 400).
        HTTPException: If the profile image isn't changed or updated (status code 400).

    Returns:
        None: Raises HTTPException with appropriate messages indicating the result of the operation.
    """
        user = await students_db.find_one({"student_id":student_id})
        if not user :
            raise HTTPException(
                status_code = 404,
                detail = "User not found with the given id."
            )
        
        if profile_image :
            
            profile_image_delete = await delete_file_from_github(user["profile_url"])

            if profile_image_delete.status_code != 200:
                raise HTTPException(status_code=409, detail="conflict : Unable to change the file")
            profile_image_content = await profile_image.read()
            profile_image_response = await upload_to_github(profile_image_content, profile_image.filename)
            if profile_image_response.status_code == 201:
                profile_image_url = profile_image_response.json().get("content", {}).get("html_url", "")
                user["profile_url"] = profile_image_url

            else:
                raise HTTPException(status_code=400, detail="Error while uploading the cover image")
            
        profile_update = await students_db.update_one({"student_id": student_id},{"$set": {"profile_url": profile_image_url}})
        if profile_update.modified_count == 0:
            raise HTTPException(status_code=400,detail="profile_image isn't changed")

        raise HTTPException(status_code=201, detail="profile_image changed Successfully")

    @staticmethod
    async def delete_student(student_id:str)->dict:

        """
    Deletes a user document from the database by the given user ID.

    Args:
        user_id (str): The unique identifier of the user to be deleted.

    Returns:
        dict: A success message indicating that the user has been deleted.

    Raises:
        HTTPException: If no user is found with the given ID (status code 404).
        HTTPException: If the deletion fails for any reason (status code 500).
    """
        user = await students_db.find_one({"student_id":student_id})

        if not user :
            raise HTTPException(
                status_code = 404,
                detail = "User not found with the given id."
            )
        delete_user = await students_db.delete_one({"student_id":student_id})
        if delete_user.deleted_count == 1:
           return {"message":"User Deleted successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail = "failed to delete the user"
            )

