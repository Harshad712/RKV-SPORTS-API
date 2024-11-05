from fastapi import HTTPException,Form,File,UploadFile
from models.home_model import BlockModel
from utilities.utils import client
from utilities.git_hub_utilities import upload_to_github,delete_file_from_github

# Initialize the MongoDB connection
mydb = client["Rkv-Sports"]
home_db = mydb.home


class Blocks:
    @staticmethod
    async def get_all_blocks() -> list:
        """
        Retrieves all blocks.

        Returns:
            list: List of dictionaries, each representing a block.

        Raises:
            HTTPException: If no data is found in the database (404).
        """
        blocks = await home_db.find().to_list(length=None)
        if not blocks:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        for block in blocks:
            block["_id"] = str(block["_id"])  # Convert ObjectId to string
        return blocks


    @staticmethod
    async def get_block_byname(block_name: str) -> dict:
        """
        Fetches a specific block by name.

        Args:
            block_name (str): Name of the block to retrieve.

        Returns:
            dict: Block data as dictionary.

        Raises:
            HTTPException: If block is not found (404).
        """
        result = await home_db.find_one({"name": block_name.lower()})
        if not result:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        result["_id"] = str(result["_id"])
        return result


    @staticmethod
    async def update_block(block_name: str, data: BlockModel) -> dict:
        """
        Updates a block by name.

        Args:
            block_name (str): The block to be updated.
            data (BlockModel): New data model for the block.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If block is not found (404).
        """
        block = await home_db.find_one({"name": block_name.lower()})
        if not block:
            raise HTTPException(status_code=404, detail="Data not found in the database.")

        updated_data = data.model_dump()
        await home_db.update_one({"name": block_name.lower()}, {"$set": updated_data})
        return {"message": "Block updated successfully"}


    @staticmethod
    async def delete_block(block_name: str) -> dict:
        """
        Deletes a block by name.

        Args:
            block_name (str): The block to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If block is not found (404).
        """
        block = await home_db.find_one({"name": block_name.lower()})
        if not block:
            raise HTTPException(
                status_code=404, detail="Data not found in the database.")
        block_image_delete = await delete_file_from_github(block["block_image_url"])
        if block_image_delete.status_code != 200 :
            raise HTTPException(
                status_code=409,
                detail="Conflict:Unable to delete the block"
            )

        delete_block = await home_db.delete_one({"name": block_name.lower()})
        if delete_block.deleted_count == 1 :
            return {"message": "Block deleted successfully"}
        else :
            raise HTTPException(
                status_code = 500,
                detail = "Unable to delete the user"
            )


    @staticmethod
    async def create_block(block_name : str = Form(...),
                           block_content : str = Form(...),
                           block_image : UploadFile = File(...)) -> dict:
        """
        Inserts a new block into the database.

        Args:
            data (BlockModel): The data for the new block.

        Returns:
            dict: Success message with the ID of the newly created block.

        Raises:
            HTTPException: If a block with the same name already exists.
        """
        # Check if the block name already exists
        existing_block = await home_db.find_one({"block_name": block_name.lower()})
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
        
        result = await home_db.insert_one(new_block)
        if result.inserted_id :
             return {"message": "Block created successfully", "block_id": str(result.inserted_id)}
        else :
            raise HTTPException(
                status_code=400,
                detail = "Error while creating new block."
            )

