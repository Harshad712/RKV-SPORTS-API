from motor.motor_asyncio import  AsyncIOMotorCollection
from typing import TypeVar
from models.home_model import BlockModel
from repository.crud_repo import CrudRepository  
from utilities.utils import client
from fastapi import File,UploadFile,HTTPException
from utilities.git_hub_utilities import upload_to_github,delete_file_from_github


my_db = client['Rkv-Sports']
home_db = my_db.home

T = TypeVar('T',bound=BlockModel)

class HomeBlocks(CrudRepository[BlockModel]):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__(collection)

    async def upload_image(self,file: UploadFile = File(...)) :
        """
        Uploads a file to the server. The file is stored in the GitHub and its link is stored in the MongoDB database.

        Args:

            file (UploadFile): The file to be uploaded.

        Returns:

            dict: A dictionary containing the message "File uploaded successfully" and the "_id" of the file in the database.

        Raises:

            HTTPException: If there is an error while uploading the file.
        """


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


home_repo = HomeBlocks(home_db)