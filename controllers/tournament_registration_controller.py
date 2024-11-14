from fastapi import UploadFile
from typing import List,Optional
from utilities.utils import handle_exception
from services.tournament_registration_services import TournamentRegristrationService,RegistrationStatus
from models.tournament_registration_model import Player
from datetime import datetime


tournament_registration_service = TournamentRegristrationService()

class TournamentRegistrationController:
    
    @staticmethod
    @handle_exception
    async def register_tournament(
    team_name: str ,
    player_ids: List[str] ,  # List of player IDs
    player_names: List[str] ,  # List of player names
    player_positions: List[Optional[str]] = None,  # List of player positions
    coach_name: Optional[str] = None ,
    contact_number: Optional[str] = None ,
    registration_fee: Optional[float] = None ,
    additional_notes: Optional[str] = None,
    registration_date: Optional[datetime] = datetime.utcnow(),  # Default value set directly
    status: RegistrationStatus = RegistrationStatus.pending ,# Default value set directly
    team_profile : UploadFile = None
):
        """
    Registers a team for a tournament.

    This function handles team registration by saving team details, including coach information, contact number, 
    and a profile image. It validates if a team with the same name already exists, then uploads the team image 
    and stores the tournament registration details in the database.

    Parameters:
    - team_name (str): The name of the team to register. Must be unique across registrations.
    - players (List[Player]): List of players in the team, with detailed player-specific information.
    - coach_name (Optional[str]): Name of the team's coach. Default is None.
    - contact_number (Optional[str]): Contact number for team inquiries. Default is None.
    - registration_fee (Optional[float]): The registration fee for the tournament. Default is None.
    - additional_notes (Optional[str]): Any additional information or notes for the registration. Default is None.
    - registration_date (Optional[datetime]): Date of registration. Defaults to the current UTC time.
    - status (RegistrationStatus): Registration status, defaults to 'Pending'.
    - team_profile (UploadFile): Optional file upload for the team's profile image.

    Raises:
    - HTTPException: If a team with the specified name already exists in the database.

    Returns:
    - dict: A success message indicating the team was registered successfully, 
      along with the details stored in the database.

    Database Operations:
    - Checks if a team with `team_name` already exists in the database.
    - Uploads the profile image using `tournament_registration_repo.upload_image`.
    - Creates a new entry in the tournament registration repository.

    Example:
    >>> await register_tournament(
    >>>     team_name="The Strikers",
    >>>     players=[...],
    >>>     coach_name="Coach Doe",
    >>>     contact_number="123-456-7890",
    >>>     registration_fee=100.0,
    >>>     additional_notes="Excited to participate!",
    >>>     team_profile=uploaded_file
    >>> )

    Notes:
    - Ensure `team_name` is unique as this function enforces uniqueness per registration.
    - The `team_profile` image is saved and its URL is attached to the registration data.
    - Returns a dictionary containing a success message if the team is registered without conflicts.
    """
        return await tournament_registration_service.register_tournament(team_name,player_ids,player_names,player_positions,coach_name,contact_number,registration_fee,additional_notes,registration_date,status,team_profile)
    
    @staticmethod
    @handle_exception
    async def get_all_teams():
        """
    Retrieves all registered teams from the database.

    This function fetches all team records from the `tournament_registration_repo`. It raises an HTTPException
    if no teams are found. If teams are found, it iterates through each record, converting the ObjectId to a string
    to ensure compatibility with JSON serialization, and returns the list of teams.

    Raises:
    - HTTPException: If no teams are found, an HTTP 404 error is raised with the message "No teams found."

    Returns:
    - List[dict]: A list of dictionaries, where each dictionary represents a team with all relevant details.
      The `_id` field for each team is converted to a string for JSON serialization.

    Example:
    >>> teams = await get_all_teams()
    >>> print(teams)
    [
        {
            "_id": "64bdf7892c894001af05e9a3",
            "team_name": "The Warriors",
            "coach_name": "John Doe",
            "players": [...],
            ...
        },
        ...
    ]

    Notes:
    - This function expects that `tournament_registration_repo.get_all()` returns a list of dictionaries,
      with each dictionary containing the details of a registered team.
    - This function performs no modifications to the data aside from converting ObjectId fields for serialization.
    """
        return await tournament_registration_service.get_all_teams()
    
    @staticmethod
    @handle_exception
    async def get_team_by_name(team_name:str):
        """
    Retrieves a team by its name from the database.

    This function searches for a team in the `tournament_registration_repo` that matches the provided `team_name`. 
    If no matching team is found, an HTTP 404 error is raised. If a team is found, it converts the `_id` field 
    from an ObjectId to a string for JSON serialization and returns the team's details.

    Parameters:
    - team_name (str): The name of the team to retrieve.

    Raises:
    - HTTPException: If no team is found with the specified `team_name`, an HTTP 404 error is raised with the message "No team found."

    Returns:
    - dict: A dictionary representing the team details, including all relevant information, with the `_id` field converted to a string.

    Example:
    >>> team = await get_team_by_name("The Strikers")
    >>> print(team)
    {
        "_id": "64bdf7892c894001af05e9a3",
        "team_name": "The Strikers",
        "coach_name": "Jane Doe",
        "players": [...],
        ...
    }

    Notes:
    - This function expects `tournament_registration_repo.find_by` to return a dictionary containing the team's details.
    - The `_id` field is converted to a string to ensure compatibility with JSON serialization.
    """
        return await tournament_registration_service.get_team_by_name(team_name)
    
    @staticmethod
    @handle_exception
    async def update_team_details(
        team_name: str,
        player_ids: Optional[List[str]] = None,  # List of player IDs
        player_names: Optional[List[str]] = None,  # List of player names
        player_positions: Optional[List[Optional[str]]] = None,  # List of player positions
        coach_name: Optional[str] = None,
        contact_number: Optional[str] = None,
        registration_fee: Optional[float] = None,
        additional_notes: Optional[str] = None,
        registration_date: Optional[datetime] = None,
        status: Optional[RegistrationStatus] = None,
    ):
        """
    Updates the details of an existing team in the tournament registration system.

    This function retrieves a team by its unique name and updates its details based on
    the provided parameters. The team data is partially updated; only the fields with 
    provided values will be modified, leaving the rest unchanged.

    Parameters:
    - team_name (str): The name of the team to be updated. Used to locate the team record.
    - player_ids (Optional[List[str]]): A list of player IDs for updating the team roster.
    - player_names (Optional[List[str]]): A list of player names corresponding to player IDs.
    - player_positions (Optional[List[Optional[str]]]): A list of player positions, 
      indexed corresponding to player IDs and names.
    - coach_name (Optional[str]): The updated name of the team's coach.
    - contact_number (Optional[str]): The updated contact number for the team.
    - registration_fee (Optional[float]): The updated registration fee for the team.
    - additional_notes (Optional[str]): Any additional notes about the team.
    - registration_date (Optional[datetime]): The date of registration, if it needs updating.
    - status (Optional[RegistrationStatus]): The updated registration status of the team.

    Raises:
    - HTTPException: If the team with the provided name does not exist, or if the update fails.

    Returns:
    - dict: A success message indicating the team details were updated successfully.
    """
        return await tournament_registration_service.update_team_details(team_name,player_ids,player_names,player_positions,coach_name,contact_number,registration_fee,additional_notes,registration_date,status)
    
    @staticmethod
    @handle_exception
    async def update_team_profile( team_name: str, team_profile: UploadFile = None):
        """
    Update the profile of a tournament team.

    This function updates a team's profile image in the database. If an image already exists for
    the team, it deletes the existing image and uploads the new one, updating the database with
    the new image URL.

    Parameters:
        team_name (str): The name of the team whose profile is to be updated.
        team_profile (UploadFile, optional): The new profile image to be uploaded.

    Returns:
        dict: A message indicating the success of the operation.

    Raises:
        HTTPException: If the team is not found in the database.
    """
        return await tournament_registration_service.update_team_profile(team_name,team_profile)

    async def delete_team(self,team_name: str):
        """
    Delete a tournament team and its profile image.

    This function deletes a team from the database and removes its associated profile image
    if it exists. The function also checks if the image deletion from the storage (e.g., GitHub)
    is successful before removing the team record from the database.

    Parameters:
        team_name (str): The name of the team to delete.

    Returns:
        dict: A message indicating the successful deletion of the team.

    Raises:
        HTTPException: 
            - If the team is not found in the database.
            - If there is a conflict while deleting the profile image.
    """
        return await tournament_registration_service.delete_team(team_name)
