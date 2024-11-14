from fastapi import HTTPException,File,UploadFile
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from pydantic import BaseModel, ValidationError as PydanticValidationError
from typing import TypeVar, Generic, Optional, List, Dict
from utilities.git_hub_utilities import upload_to_github,delete_file_from_github

T = TypeVar('T', bound=BaseModel)

class CrudRepository(Generic[T]):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, data: T) -> T:
        try:
            document = data.model_dump(exclude_unset=True) if hasattr(data, 'model_dump') else data
            result = await self.collection.insert_one(document)
            document["_id"] = str(result.inserted_id)  # Add the generated ID to the document
            return data.model_validate(document) if hasattr(data, 'model_validate') else document
        except Exception as error:
        # Log the specific error message
            print(f"Error creating document: {error}")  # Log to console or use a logging framework
            raise HTTPException(status_code=400, detail=f"Failed to create the document: {str(error)}") from error

    async def delete(self, id: str) -> Optional[T]:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

        response = await self.collection.find_one_and_delete({"_id": ObjectId(id)})
        if response is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return response

    async def get(self, id: str) -> Optional[T]:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

        response = await self.collection.find_one({"_id": ObjectId(id)})
        if response is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return response

    async def find_by(self, query: Dict) -> Optional[T]:
        response = await self.collection.find_one(query)
        return response

    async def get_all(self) -> List[T]:
        cursor = self.collection.find({})
        documents = await cursor.to_list(length=None)
        return [doc for doc in documents]

    async def update(self, id: str, data: T) -> Optional[T]:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

        document = data
        response = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": document},
            return_document=True
        )
        if response is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return response
    async def upload_image(self,file: UploadFile = File(...)) :
       

        if file:
            image_size = len(await file.read())
            max_length = 10 * 1024 * 1024  # 10 MB
            if image_size > max_length:
                raise HTTPException(status_code=413, detail="File Size Exceeds the limit of 10 MB.")
            
        file_content = await file.read()

        response = await upload_to_github(file_content, file.filename)

        if response.status_code == 201:
            file_url = response.json().get("content", {}).get("html_url", "")
        else:
            raise HTTPException(
                status_code=400, detail="Error uploading file to GitHub"
            )

        return file_url
    async def delete_image(self,image_url:str) :
        block_image_delete = await delete_file_from_github(image_url)
        if block_image_delete.status_code != 200 :
            raise HTTPException(
                status_code=409,
                detail="Conflict:Unable to delete the block"
            )
        return {"message":"Image Successfully deleted form git hub"}
