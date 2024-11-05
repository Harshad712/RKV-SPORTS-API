from fastapi import HTTPException, File, UploadFile, Form
from models.banner_model import Banner_model
from utilities.git_hub_utilities import upload_to_github,delete_file_from_github
from services.banner_services import BannerService
from utilities.utils import handle_exception

banner_service = BannerService()
class Banners() :
    @staticmethod
    @handle_exception
    async def get_banners() :
        """
        Retrieve all banner images from the database, sorted by creation date.

        This function fetches all banners from the database, sorted in descending order by `created_at`.
        
        If no banners are found, an HTTPException is raised.

        Returns:
            
            list: A list of banner documents, each with `_id` as a string for easier JSON serialization.

        Raises:
            
            HTTPException: If no banners are found in the database.
        """

        return await banner_service.get_banners()
    
    @staticmethod
    @handle_exception
    async def upload_banner(banner_id : str = Form(...),banner_image : UploadFile = File(...) ) :
        """
        Upload a new banner image to GitHub and store the banner details in the database.

        This function takes a `banner_id` and an image file, uploads the image to GitHub,
        
        retrieves the image URL, and stores the banner details, including the URL, in the database.
        
        Args:
        
            banner_id (str): The unique identifier for the banner.
        
            banner_image (UploadFile): The image file for the banner to be uploaded.

        Returns:
        
            dict: A dictionary containing a success message and the newly created banner's `_id`.
        
                For example: {"Message": "Banner Uploaded Successfully", "_id": "<banner_id>"}.

        Raises:
        
            HTTPException: If there is an error uploading the banner image to GitHub.
            
            HTTPException: If there is an error inserting the banner data into the database.
        """
        return await banner_service.upload_banner(banner_id = banner_id,banner_image = banner_image)


    @staticmethod
    @handle_exception
    async def update_banner(banner_id : str,banner_image: UploadFile = File(...)):
        """
        Update an existing banner's image in the database.

        This function updates a banner's image by first validating the banner ID, deleting the existing banner image from GitHub,
        
        uploading the new image, and updating the image link in the MongoDB database.

        Args:
        
            id (str): The ID of the banner to update. Must be a valid MongoDB ObjectId string.
        
            banner_image (UploadFile): The new banner image file to upload and link to the banner.

        Returns:
        
            HTTPException: Raises a 201 status code exception upon successful update with a message indicating success.

        Raises:
        
            HTTPException: If the `id` is invalid or improperly formatted.
        
            HTTPException: If no banner is found with the given ID.
        
            HTTPException: If there is a conflict or error when deleting the current banner image from GitHub.
        
            HTTPException: If there is an error uploading the new banner image to GitHub.
        
            HTTPException: If the database update for the banner image link fails.
        """
        
        
        return await banner_service.update_banner(banner_id = banner_id,banner_image = banner_image)
    @staticmethod
    @handle_exception
    async def delete_banner(banner_id:str):

        """
    Deletes a banner from the database and its corresponding file from GitHub.

    Args:
        banner_id (str): The unique identifier of the banner to be deleted.

    Raises:
        HTTPException: If the banner is not found, or if there is a conflict when 
        trying to delete the file from GitHub, or if the deletion fails.

    Returns:
        HTTPException: A success message if the banner is successfully deleted.
    """
        
        return await banner_service.delete_banner(banner_id = banner_id)