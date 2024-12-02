from fastapi import HTTPException,Form,File,UploadFile
from services.tournament_creation_services import tournament_creation_service
from typing import Optional
from utilities.utils import handle_exception
from models.tournament_creation_model import TournamentCreation,TournamentPrize,SportSpecificDetails
from datetime import datetime
from pydantic import Field

tournament_service = tournament_creation_service()

class Tournamentcreation :
    @staticmethod
    @handle_exception
    async def create_tournament(
    tournament_name :str,
    sport_type: str,
    location: str,
    start_date: str,
    end_date: str,
    max_teams: int,
    team_size: int,
    prize_first_place: str,
    prize_second_place: str,
    prize_third_place: str,
    rules: Optional[str] = None,
    match_format: Optional[str] = None,
    entry_fee: Optional[float] = None,
    sport_specific_details: Optional[str] = None,
    tournament_image: UploadFile = File(...),
):
        """
    Create a new tournament in the database.

    This method accepts tournament data and an image file, checks if a similar tournament
    already exists in the database, uploads the provided image, and then stores the tournament
    details in the database. If a tournament with the same name, sport type, start date, and 
    end date already exists, an error is raised.

    Parameters:
    ----------
    tournament_data : TournamentCreation
        The data for the tournament to be created, including name, sport type, and dates.
    
    tournament_image : UploadFile
        The image file for the tournament. This image will be uploaded, and its URL 
        stored in the tournament details.

    Raises:
    -------
    HTTPException
        If a tournament with the same name, sport type, start date, and end date already exists.
        A 400 status code is returned with an error message.

    Returns:
    --------
    dict
        A success message indicating the tournament was created, along with the tournament's ID.
    """
        return await tournament_service.create_tournament( tournament_name=tournament_name,
                                                          sport_type=sport_type,
                                                          location=location,
                                                          start_date=start_date,
                                                          end_date=end_date,
                                                          max_teams=max_teams,
                                                          team_size=team_size,
                                                          prize_first_place=prize_first_place,
                                                          prize_second_place=prize_second_place,
                                                          prize_third_place=prize_third_place,
                                                          rules=rules,
                                                          match_format=match_format,
                                                          entry_fee=entry_fee,
                                                          sport_specific_details=sport_specific_details,
                                                          tournament_image=tournament_image)

    @staticmethod
    @handle_exception
    async def get_all_tournaments():
        """
    Retrieve all tournaments from the database.

    This method fetches all tournament records from the database. If no tournaments are
    found, it raises a 404 error. For each tournament, the MongoDB ObjectId is converted 
    to a string for JSON serialization.

    Raises:
    -------
    HTTPException
        If no tournaments are found, a 404 status code is returned with an appropriate error message.

    Returns:
    --------
    list of dict
        A list of dictionaries containing tournament details. Each dictionary represents a tournament,
        with the "_id" field as a string instead of an ObjectId.
    """
        return await tournament_service.get_all_tournaments()
    
    @staticmethod
    @handle_exception
    async def get_tournament_name( tournament_name: str):
        """
    Retrieve a tournament by its name from the database.

    This method searches the database for a tournament with a specific name.
    If the tournament is found, its MongoDB ObjectId is converted to a string 
    for JSON serialization. If no tournament matches the provided name, a 404 
    error is raised.

    Parameters:
    -----------
    tournament_name : str
        The name of the tournament to search for.

    Raises:
    -------
    HTTPException
        If no tournament is found with the specified name, a 404 status code 
        is returned along with an error message.

    Returns:
    --------
    dict
        A dictionary containing the details of the tournament, with the "_id" 
        field as a string instead of an ObjectId.
    """
        return await tournament_service.get_tournament_name(tournament_name=tournament_name)
    
    @staticmethod
    @handle_exception
    async def update_tournament_details(tournament_name: str,
    sport_type: Optional[str]=None,
    location: Optional[str]=None,
    start_date: Optional[str]=None,
    end_date: Optional[str] = None,
    max_teams: Optional[int] = None,
    team_size: Optional[int] = None,
    prize_first_place: Optional[str] = None,
    prize_second_place: Optional[str] = None,
    prize_third_place: Optional[str] = None,
    rules: Optional[str] = None,
    match_format: Optional[str] = None,
    entry_fee: Optional[float] = None,
    sport_specific_details: Optional[str] = None,
):
        """
    Update tournament details based on the provided tournament name.
    
    Parameters:
        tournament_name (str): The name of the tournament to update.
        sport_type (Optional[str]): Type of sport (e.g., 'cricket', 'basketball').
        location (Optional[str]): Location of the tournament.
        start_date (Optional[str]): Tournament start date.
        end_date (Optional[str]): Tournament end date.
        max_teams (Optional[int]): Maximum number of teams allowed.
        team_size (Optional[int]): Number of players per team.
        prize_first_place (Optional[str]): Prize for first place.
        prize_second_place (Optional[str]): Prize for second place.
        prize_third_place (Optional[str]): Prize for third place.
        rules (Optional[str]): Rules of the tournament.
        match_format (Optional[str]): Format of the match (e.g., "T20").
        entry_fee (Optional[float]): Entry fee for the tournament.
        sport_specific_details (Optional[str]): JSON string of sport-specific details.

    Raises:
        HTTPException: If the tournament with the provided name does not exist.

    Returns:
        dict: A success message indicating the tournament was updated.
    """
        return await tournament_service.update_tournament_details( tournament_name=tournament_name,
                                                          sport_type=sport_type,
                                                          location=location,
                                                          start_date=start_date,
                                                          end_date=end_date,
                                                          max_teams=max_teams,
                                                          team_size=team_size,
                                                          prize_first_place=prize_first_place,
                                                          prize_second_place=prize_second_place,
                                                          prize_third_place=prize_third_place,
                                                          rules=rules,
                                                          match_format=match_format,
                                                          entry_fee=entry_fee,
                                                          sport_specific_details=sport_specific_details)
    
    
    @staticmethod
    @handle_exception 
    async def update_tournament_profile(tournament_name: str, tournament_image: UploadFile = None):
        """
    Update the profile image for a specific tournament.

    This function allows updating the image of an existing tournament by:
    1. Verifying that the tournament exists in the database.
    2. Deleting the existing image associated with the tournament.
    3. Uploading the new image.
    4. Updating the tournament record with the new image URL.

    Parameters:
        tournament_name (str): The name of the tournament whose profile image is to be updated.
        tournament_image (UploadFile, optional): The new image file to be uploaded. Defaults to None.

    Raises:
        HTTPException: If the tournament is not found in the database, raises a 404 error.
    
    Returns:
        dict: A success message indicating the image has been updated.
    """
        return await tournament_service.update_tournament_profile(tournament_name=tournament_name,tournament_image=tournament_image)
    
    @staticmethod
    @handle_exception
    async def delete_tournament(tournament_name: str):
        """
    Delete a specific tournament by its name.

    This function handles the deletion of a tournament by:
    1. Checking if the tournament exists in the database.
    2. Deleting the associated profile image from GitHub if it exists.
    3. Removing the tournament record from the database.

    Parameters:
        tournament_name (str): The name of the tournament to be deleted.

    Raises:
        HTTPException: 
            - 404: If the tournament is not found with the given name.
            - 409: If there is a conflict and the profile image could not be deleted from GitHub.
    
    Returns:
        dict: A success message indicating that the tournament was deleted successfully.
    """
        return await tournament_service.delete_tournament(tournament_name)