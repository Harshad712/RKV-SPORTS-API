from utilities.utils import handle_exception
from services.matches_services import MatchesServices
from typing import Optional
from models.match_model import MatchStatus

match_serivces = MatchesServices()

class MatchController:
    @staticmethod
    @handle_exception
    async def get_all_matches() -> list:
        """
        Retrieves all matches.

        Returns:
            list: List of dictionaries, each representing a matches.

        Raises:
            HTTPException: If no data is found in the database (404).
        """
        return await match_serivces.get_all_matches()


    @staticmethod
    @handle_exception
    async def get_matches_byname(match_id: str) -> dict:
        """
        Fetches a specific matches by name.

        Args:
            match_id (str): Name of the matches to retrieve.

        Returns:
            dict: matches data as dictionary.

        Raises:
            HTTPException: If matches is not found (404).
        """
        return await match_serivces.get_matches_byname(match_id = match_id)


    @staticmethod
    @handle_exception
    async def update_matches(match_id: str,team1_score :Optional[str] = None,
                             team2_score:Optional[str]= None,
                             match_status: Optional[MatchStatus]=None) -> dict:
        """
        Updates a matches by name.

        Args:
            match_id (str): The matches to be updated.
            data (matchesModel): New data model for the matches.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If matches is not found (404).
        """
        return await match_serivces.update_matches(match_id=match_id,team1_score=team1_score,team2_score=team2_score,
                                                   match_status=match_status)


    @staticmethod
    @handle_exception
    async def delete_matches(match_id: str) -> dict:
        """
        Deletes a matches by name.

        Args:
            match_id (str): The matches to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: If matches is not found (404).
        """
        return await match_serivces.delete_matches(match_id = match_id)


    @staticmethod
    @handle_exception
    async def create_matches(match_id : str ,
                          team1_name:str,
                           team2_name:str,
                           team1_score:str,
                           team2_score:str,
                           match_status:MatchStatus) -> dict:
        """
        Inserts a new matches into the database.

        Args:
            data (matchesModel): The data for the new matches.

        Returns:
            dict: Success message with the ID of the newly created matches.

        Raises:
            HTTPException: If a matches with the same name already exists.
        """
        return await match_serivces.create_matches(match_id=match_id,
                                                   team1_name=team1_name,
                                                   team2_name=team2_name,
                                                   team1_score=team1_score,
                                                   team2_score=team2_score,
                                                   match_status=match_status)