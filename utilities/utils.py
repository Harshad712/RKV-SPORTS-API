from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import HTTPException
from functools import wraps
from bson import ObjectId 


url = "mongodb+srv://harshadkokkinti:RkvSports@cluster0.ii5oq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(url, server_api=ServerApi("1"), connectTimeoutMS=50000)


GITHUB_TOKEN = "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"
REPO_OWNER = "Harshad712"
REPO_NAME = "RKV-SPORTS-TEST"
FOLDER_PATH = "testing"
BRANCH = "main"



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




class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v,field = None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


