from fastapi import Form,File,UploadFile
from utilities.utils import handle_exception
from typing import Optional
from services.student_services import StudentService

student_service = StudentService()


class Students():
    @staticmethod
    @handle_exception
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
        return await student_service.create_student(student_name=student_name,
                                                    student_id=student_id,
                                                    year=year,
                                                    mail=mail,
                                                    gender=gender,
                                                    password=password,
                                                    profile_image=profile_image)
       
        

    @staticmethod
    @handle_exception
    async def get_all_students() -> list :

        """
        Retrieves all student documents from the database.

        Returns:
            list: A list of student documents with their '_id' fields converted to strings.

        Raises:
            HTTPException: If no students are found in the database (status code 404).
        """
        return await student_service.get_all_students()
    
    @staticmethod
    @handle_exception
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
        return await student_service.get_student_by_id(student_id=student_id)
    
    @staticmethod
    @handle_exception
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
        return await student_service.update_student_details(student_id=student_id,
                                                            student_name=student_name,
                                                            mail=mail,
                                                            year=year,
                                                            gender=gender,
                                                            password=password)
    
    @staticmethod
    @handle_exception
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
        return await student_service.update_student_profile(student_id=student_id,profile_image=profile_image)

    @staticmethod
    @handle_exception
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
        return await student_service.delete_student(student_id=student_id)