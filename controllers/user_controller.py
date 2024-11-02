from fastapi import HTTPException,Form
from bson import ObjectId
from utilities.utils import client
from models.users_model import User,update_user
from typing import Optional

my_db = client['Rkv-Sports']
users_db = my_db.users

class Users():
    @staticmethod
    async def create_user(name:str,user_id:str,year:str,mail:str) ->dict:

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

        user_exists = await users_db.find_one({"user_id":user_id})
        if user_exists :
            raise HTTPException(
                status_code = 409,
                detail = "A User already found with the same Id."
            )
        user = User(
            name= name,
            user_id = user_id,
            year = year,
            mail = mail
        )
        user = user.model_dump()
        result = await users_db.insert_one(user)
        if result.inserted_id:
            user["_id"] = str(result.inserted_id)
            return {"message":"User Created Successfully"}
        else:
            raise HTTPException(status_code=400,detail = "Error While creating the new user")
        

    @staticmethod
    async def get_all_users() -> list :

        """
    Retrieves all user documents from the database.

    Returns:
        list: A list of user documents with their '_id' fields converted to strings.

    Raises:
        HTTPException: If no users are found in the database (status code 404).
    """
        users=[]
        async for user in  users_db.find():
            user["_id"] = str(user["_id"])
            users.append(user)
        if not users:
            raise HTTPException(
                status_code=404,
                detail = "No Users Found."
            )
        return users
    
    @staticmethod
    async def get_user_id(user_id:str) -> dict:

        """
    Retrieves a user document from the database by the given user ID.

    Args:
        user_id (str): The unique identifier of the user to be retrieved.

    Returns:
        dict: The user document if found.

    Raises:
        HTTPException: If no user is found with the given ID (status code 404).
    """
        user =await  users_db.find_one({"user_id":user_id})
        if not user:
            raise HTTPException(
                status_code=404,
                detail="No user found with the given id."
            )
        user["_id"] = str(user["_id"])

        return user
    
    @staticmethod
    async def update_user_details(user_id:str,
                                  name :Optional[str] = None,
                                  year : Optional[str]= None,
                                  mail : Optional[str] = None) -> dict:
        
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
        user_exists = await users_db.find_one({"user_id":user_id})
        if not user_exists :
            raise HTTPException(
                status_code = 404,
                detail = "User not found with the given id."
            )
        user = update_user(
            name = name,
            year = year,
            mail = mail
        )
        user = user.model_dump()

        user = {k:v  for k,v in user.items() if v is not None}
        if not user :
            raise HTTPException(
                status_code= 400,
                detail = "No data Provided for update"
            )
        user_update = await users_db.update_one(
            {"user_id":user_id},
            {"$set":user}
        )
        if user_update.modified_count == 0:
            raise HTTPException(status_code=404, detail="No User found with the given ID or no changes made")
        
        return{"message":"User updated Successfully."}
    
    @staticmethod
    async def delete_user(user_id:str)->dict:

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
        user = await users_db.find_one({"user_id":user_id})

        if not user :
            raise HTTPException(
                status_code = 404,
                detail = "User not found with the given id."
            )
        delete_user = await users_db.delete_one({"user_id":user_id})
        if delete_user.deleted_count == 1:
           return {"message":"User Deleted successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail = "failed to delete the user"
            )

