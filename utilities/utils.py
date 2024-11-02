from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import HTTPException
from functools import wraps

url = "mongodb+srv://harshadkokkinti:RkvSports@cluster0.ii5oq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(url, server_api=ServerApi("1"), connectTimeoutMS=50000)




def handle_exception(function):
    @wraps(function)
    async def wrapper(*arguments, **kwargs):
        try:
            return await function(*arguments, **kwargs)
        except HTTPException as http_exce:
            raise http_exce
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unknown error occurred.{str(e)}"
            )

    return wrapper
