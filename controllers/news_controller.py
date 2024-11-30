from fastapi import Form,File,UploadFile
from utilities.utils import handle_exception
from services.news_services import NewsServices

news_services = NewsServices()




class NewsController:
    @staticmethod
    @handle_exception
    async def get_all_news() -> list:
        """
        Retrieves all news.

        Returns:
            list: List of dictionaries, each representing a news.

        Raises:
            HTTPException: If no data is found in the database (404).
        """
        return await news_services.get_all_news()


    @staticmethod
    @handle_exception
    async def get_news_byname(title: str) -> dict:
        """
        Fetches a specific news by name.

        Args:
            title (str): Name of the news to retrieve.

        Returns:
            dict: news data as dictionary.

        Raises:
            HTTPException: If news is not found (404).
        """
        return await news_services.get_news_byname(title = title)


    @staticmethod
    @handle_exception
    async def update_news(title: str, news_content: str) -> dict:
        """
        Updates a news by name.

        Args:
            title (str): The news to be updated.
            data (newsModel): New data model for the news.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If news is not found (404).
        """
        return await news_services.update_news(title=title,news_content= news_content)


    @staticmethod
    @handle_exception
    async def delete_news(title: str) -> dict:
        """
        Deletes a news by name.

        Args:
            title (str): The news to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If news is not found (404).
        """
        return await news_services.delete_news(title = title)


    @staticmethod
    @handle_exception
    async def create_news(title : str = Form(...),
                          sport_type :str = Form(...),
                           news_content : str = Form(...),
                           news_image : UploadFile = File(...)) -> dict:
        """
        Inserts a new news into the database.

        Args:
            data (newsModel): The data for the new news.

        Returns:
            dict: Success message with the ID of the newly created news.

        Raises:
            HTTPException: If a news with the same name already exists.
        """
        return await news_services.create_news(title=title,sport_type=sport_type,news_content=news_content,news_image=news_image)
    @staticmethod
    @handle_exception
    async def update_news_image(title : str = Form(...),news_image : UploadFile = File(...)):
        """
    Updates the image of a specified news in the database.

    This function locates a news by its name, deletes its current image,
    uploads the new image, and updates the database with the new image URL.

    Args:
        title (str): The name of the news whose image is to be updated.
        news_image (UploadFile): The new image file to upload for the news.

    Raises:
        HTTPException: If the specified news is not found in the database, 
                       a 404 error is raised.

    Returns:
        dict: A dictionary containing a success message if the image is updated successfully.
    """
        return await news_services.update_news_image(title = title,news_image=news_image)
