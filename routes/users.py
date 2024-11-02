from fastapi import APIRouter,HTTPException,Form
from utilities.utils import handle_exception
from controllers.user_controller import Users
from typing import Optional

app = APIRouter(tags=["Users"])

@app.post("/",summary="creates new users")
@handle_exception
async def create_user(name :str ,
                      user_id : str ,
                      year : str ,
                      mail : str ):
    """An API EndPoint to Create New Users"""
                    
    return await Users.create_user(name,user_id,year,mail)

@app.get("/",summary="fetches all users")
@handle_exception
async def get_all_users():
    """An API EndPoint to fetch all users."""

    return await Users.get_all_users()

@app.get("/{user_id}",summary="fetch single users by user_id")
@handle_exception
async def get_user_id(user_id:str ):
    """An API EndPoint fetch Single User by user-id"""

    return await Users.get_user_id(user_id)

@app.put("/",summary="updates the user details")
@handle_exception
async def update_user_details(user_id : str,
                              name :Optional[str]= None,
                              year :Optional[str]= None,
                              mail :Optional[str]= None):
    """An API EndPoint to Update user details."""

    return await Users.update_user_details(user_id,name,year,mail)

@app.delete("/",summary="deletes the users")
@handle_exception
async def delete_user(user_id:str):
    """An API EndPoint to delete the users."""

    return await Users.delete_user(user_id)