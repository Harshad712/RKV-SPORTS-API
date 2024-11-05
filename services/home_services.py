from fastapi import HTTPException, UploadFile, File,Form
from typing import List,Optional
from models.home_model import BlockModel
from repository.home_repo import home_repo
from utilities.git_hub_utilities import upload_to_github, delete_file_from_github
from utilities.utils import client

mydb = client["Rkv-Sports"]
home_db = mydb.home

class HomeService:

    async def get_all_blocks(self) -> list:
        blocks = await home_repo.get_all()
        for block in blocks:
            block["_id"] = str(block["_id"])
        if not blocks:
            raise HTTPException(status_code=404, detail="No Banners Found.")
        return blocks
     
    async def get_block_byname(self,block_name: str) -> dict:
         
         block = await home_repo.find_by({"block_name":block_name})
         if not block:
            raise HTTPException(status_code=404, detail="No block found with the given name.")
         block["_id"] = str(block["_id"])
         return block\
         
    async def update_block(self,block_name: str, data: BlockModel) -> dict:

        block = await home_repo.find_by({"block_name": block_name.lower()})
        if not block:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        updated_data = data.model_dump()
        update_data = {k: v for k, v in updated_data.items()if v is not None}
        await home_repo.update(block["_id"],update_data)
        return {"message": "Block updated successfully"}
    
    async def delete_block(self,block_name: str) -> dict:

        block = await home_repo.find_by({"block_name": block_name.lower()})
        if not block:
            raise HTTPException(
                status_code=404, detail="Data not found in the database.")
        block_image_delete = await delete_file_from_github(block["block_image_url"])
        if block_image_delete.status_code != 200 :
            raise HTTPException(
                status_code=409,
                detail="Conflict:Unable to delete the block"
            )
        await home_repo.delete(block["_id"])
        return {"message":"Block Deleted Successfully."}
    
    async def create_block(self,block_name : str = Form(...),
                           block_content : str = Form(...),
                           block_image : UploadFile = File(...)) -> dict:
        
        existing_block = await home_repo.find_by({"block_name": block_name.lower()})
        if existing_block:
            raise HTTPException(status_code=400, detail="Block with this name already exists.")

        # Insert the new block
        new_block = BlockModel(
            block_name = block_name,
            block_content = block_content,
        )
        new_block = new_block.model_dump()

        block_image_content = await block_image.read()
        block_image_response = await upload_to_github(block_image_content,block_image.filename)

        if block_image_response.status_code == 201 :
            block_image_url = block_image_response.json().get("content", {}).get("html_url", "")
            new_block["block_image_url"] = block_image_url

        else :
                raise HTTPException(status_code=400,detail="Error While Uploading The File Into Github")
        await home_repo.create(new_block)
        return {"message":"Block Created Successfully."}