from fastapi import HTTPException, UploadFile, File
from typing import List,Optional
from models.student_model import Student, update_student  # Your Pydantic models
from repository.student_repo import student_, update_student_  # Your student repository
from utilities.git_hub_utilities import upload_to_github, delete_file_from_github  # GitHub utility functions

class StudentService:

    async def create_student(self, student_name: str, student_id: str, year: str, 
                             mail: str, gender: str, password: str,
                             profile_image: UploadFile = File(None)) -> dict:
        
        student_exists = await student_.find_by({"student_id": student_id})
        if student_exists:
            raise HTTPException(status_code=409, detail="A Student already found with the same ID.")

        student = Student(
            student_name=student_name,
            student_id=student_id,
            year=year,
            mail=mail,
            gender=gender,
            password=password
        )

        student_data = student.model_dump(exclude_unset=True)

        if profile_image:
            profile_image_size = len(await profile_image.read())
            max_length = 10 * 1024 * 1024  # 10 MB
            if profile_image_size > max_length:
                raise HTTPException(status_code=413, detail="File Size Exceeds the limit of 10 MB.")

            profile_image_content = await profile_image.read()
            profile_image_response = await upload_to_github(profile_image_content, profile_image.filename)
            if profile_image_response.status_code == 201:
                profile_url = profile_image_response.json().get("content", {}).get("html_url", "")
                student_data["profile_url"] = profile_url
            else:
                raise HTTPException(status_code=400, detail="Error While Uploading The File Into GitHub")
        update_data = {k: v for k, v in student_data.items()if v is not None}
        result = await student_.create(update_data)  # Ensure this is awaited
        return {"message": "Student Created Successfully", "_id": str(result["_id"])}

    async def get_all_students(self) -> List[dict]:
        students = await student_.get_all()
        for student in students:
            student["_id"] = str(student["_id"])
        if not students:
            raise HTTPException(status_code=404, detail="No Students Found.")
        return students

    async def get_student_by_id(self, student_id: str) -> dict:
        user = await student_.find_by({"student_id": student_id})
        if not user:
            raise HTTPException(status_code=404, detail="No user found with the given ID.")
        user["_id"] = str(user["_id"])
        return user

    async def update_student_details(self, student_id:str,
                                  student_name :Optional[str] = None,
                                  year : Optional[str]= None,
                                  mail : Optional[str] = None,
                                  gender : Optional[str] = None,
                                  password : Optional[str] = None) -> dict:
        user_exists = await student_.find_by({"student_id": student_id})
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found with the given ID.")
        update_data = update_student(student_name=student_name,
                                     year = year,
                                     mail = mail,
                                     gender = gender,
                                     password = password)
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            raise HTTPException(status_code=400, detail="No data Provided for update")
        update_data = {k: v for k, v in update_dict.items()if v is not None}
        

        user_update = await student_.update(user_exists["_id"], update_data)
        if not user_update:
            raise HTTPException(status_code=404, detail="No User found with the given ID or no changes made")
        return {"message": "User updated Successfully."}

    async def update_student_profile(self, student_id: str, profile_image: UploadFile = File(...)) -> dict:
        user = await student_.find_by({"student_id": student_id})  # Ensure correct usage
        if not user:
            raise HTTPException(status_code=404, detail="User not found with the given ID.")

        if profile_image:
            profile_image_delete = await delete_file_from_github(user["profile_url"])

            if profile_image_delete.status_code != 200:
                raise HTTPException(status_code=409, detail="Conflict: Unable to change the file")

            profile_image_content = await profile_image.read()
            profile_image_response = await upload_to_github(profile_image_content, profile_image.filename)
            if profile_image_response.status_code == 201:
                profile_image_url = profile_image_response.json().get("content", {}).get("html_url", "")
                data = {"profile_url":profile_image_url}
                await student_.update(user["_id"], data)
            else:
                raise HTTPException(status_code=400, detail="Error while uploading the cover image")

        return {"message": "Profile image updated successfully."}

    async def delete_student(self, student_id: str) -> dict:
        user = await student_.find_by({"student_id": student_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found with the given ID.")
        if user["profile_url"] is not None:
            delete_user_profile = await delete_file_from_github(user["profile_url"])

            if delete_user_profile.status_code != 200:
                raise HTTPException(status_code=409, detail="Conflict: Unable to delete the profile")

        await student_.delete(user["_id"])
        return {"message": "User Deleted successfully"}
   