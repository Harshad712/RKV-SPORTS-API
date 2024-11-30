from fastapi import Form,File,UploadFile
from utilities.utils import handle_exception
from services.home_services import HomeService

home_service = HomeService()




class Blocks:
    @staticmethod
    @handle_exception
    async def get_all_blocks() -> list:
        """
        Retrieves all blocks.

        Returns:
            list: List of dictionaries, each representing a block.

        Raises:
            HTTPException: If no data is found in the database (404).
        """
        return await home_service.get_all_blocks()


    @staticmethod
    @handle_exception
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
        return await home_service.get_block_byname(block_name = block_name)


    @staticmethod
    @handle_exception
    async def update_block(block_name: str, block_content: str) -> dict:
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
        return await home_service.update_block(block_name=block_name,block_content= block_content)


    @staticmethod
    @handle_exception
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
        return await home_service.delete_block(block_name = block_name)


    @staticmethod
    @handle_exception
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
        return await home_service.create_block(block_name=block_name,block_content=block_content,block_image=block_image)
    @staticmethod
    @handle_exception
    async def update_block_image(block_name : str = Form(...),block_image : UploadFile = File(...)):
        """
    Updates the image of a specified block in the database.

    This function locates a block by its name, deletes its current image,
    uploads the new image, and updates the database with the new image URL.

    Args:
        block_name (str): The name of the block whose image is to be updated.
        block_image (UploadFile): The new image file to upload for the block.

    Raises:
        HTTPException: If the specified block is not found in the database, 
                       a 404 error is raised.

    Returns:
        dict: A dictionary containing a success message if the image is updated successfully.
    """
        return await home_service.update_block_image(block_name = block_name,block_image=block_image)
