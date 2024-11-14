from fastapi import HTTPException,Form,File,UploadFile
from models.tournament_creation_model import TournamentCreation,TournamentPrize,SportSpecificDetails,CricketDetails,BadmintonDetails,BasketballDetails,HockeyDetails,KabaddiDetails,UpateTournament
from repository.tournament_repo import tournament_creation_repo
from utilities.git_hub_utilities import upload_to_github,delete_file_from_github
from typing import Optional
from datetime import datetime
from pydantic import parse_obj_as
import json

class tournament_creation_service :

    async def create_tournament(self,
    tournament_name: str,
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
    tournament_image: UploadFile = None,
):
    
        tournament_exists = await tournament_creation_repo.find_by({
        "tournament_name": tournament_name })

        if tournament_exists:
            raise HTTPException(
            status_code=400, detail="Tournament already exists"
        )
    # Convert the model to a dictionary for manipulation
     # Create the TournamentPrize model from the form values
        prize = TournamentPrize(
            first_place=prize_first_place,
            second_place=prize_second_place,
            third_place=prize_third_place,
        )
        if sport_specific_details:
            sport_specific_details = json.loads(sport_specific_details)
     # Initialize `SportSpecificDetails` based on `sport_type`
        specific_details = None
        if sport_type.lower() == "cricket":
            sport_specific_details = SportSpecificDetails(cricket=CricketDetails(**sport_specific_details))
        elif sport_type.lower() == "kabaddi":
            sport_specific_details = SportSpecificDetails(kabaddi=KabaddiDetails(**sport_specific_details))
        elif sport_type.lower() == "basketball":
            sport_specific_details = SportSpecificDetails(basketball=BasketballDetails(**sport_specific_details))
        elif sport_type.lower() == "hockey":
            sport_specific_details = SportSpecificDetails(hockey=HockeyDetails(**sport_specific_details))
        elif sport_type.lower() == "badminton":
            sport_specific_details = SportSpecificDetails(badminton=BadmintonDetails(**sport_specific_details))
    # You can set the `created_at` and `updated_at` fields directly
        created_at = updated_at = datetime.utcnow()
        
        tournament_data = TournamentCreation(tournament_name = tournament_name,
                                        sport_type = sport_type,
                                        location = location,
                                        start_date = start_date,
                                        end_date=end_date,
                                        rules=rules,
                                        max_teams=max_teams,
                                        match_format=match_format,
                                        team_size=team_size,
                                        entry_fee = entry_fee,
                                        prize = prize,
                                        sport_specific_details=sport_specific_details,
                                        created_at=created_at,
                                        updated_at=updated_at

    

        )
        tournament = tournament_data.model_dump(exclude_unset=True)

    # Check if the tournament already exists
        

    # Upload tournament image and add the URL to tournament data
        tournament_image_url = await tournament_creation_repo.upload_image(tournament_image)
        tournament["tournament_image_url"] = tournament_image_url
        update_data = {k: v for k, v in tournament.items()if v is not None}
    # Create tournament in the database
        result = await tournament_creation_repo.create(update_data)

    # Return success message along with the created tournament's ID
        return {"message": "Tournament created successfully"}
    
    async def get_all_tournaments(self):
    # Fetch all tournaments
        tournaments = await tournament_creation_repo.get_all()
    
    # Check if tournaments are found before iterating
        if not tournaments:
            raise HTTPException(status_code=404, detail="No tournaments found.")
    
    # Convert ObjectId to string for JSON serialization
        for tournament in tournaments:
            tournament["_id"] = str(tournament["_id"])
        
    # Return tournaments in a structured format
        return tournaments
    
    async def get_tournament_name(self, tournament_name: str):
    # Find the tournament by name
        tournament = await tournament_creation_repo.find_by({"tournament_name": tournament_name})
    
    # If no tournament is found, raise a 404 error
        if not tournament:
            raise HTTPException(status_code=404, detail="No tournament found.")
    
    # Convert _id to string for JSON serialization
        tournament["_id"] = str(tournament["_id"])
    
    # Return the tournament in a structured format
        return  tournament
    
    async def update_tournament_details(self,
    tournament_name: str,
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
        # Check if the tournament exists in the database
        tournament_exists = await tournament_creation_repo.find_by({"tournament_name": tournament_name})
        if not tournament_exists:
            raise HTTPException(status_code=404, detail="The Tournament with the provided name doesn't exist.")
    
         # Ensure the prize fields are valid strings or set default values
        if prize_first_place is None:
            prize_first_place = "TBD"
        if prize_second_place is None:
            prize_second_place = "TBD"
        if prize_third_place is None:
            prize_third_place = "TBD"
    # Prepare the prize details
        prize = TournamentPrize(
            first_place=prize_first_place,
            second_place=prize_second_place,
            third_place=prize_third_place,
        )
    
    # Parse and structure sport-specific details if provided
        if sport_specific_details:
            sport_specific_details = json.loads(sport_specific_details)
    # Validate and ensure sport_specific_details is a valid dictionary
        if sport_specific_details is None:
            sport_specific_details = {}
    
    # Construct sport-specific details based on sport type
        if sport_type and sport_type.lower() == "cricket":
            sport_specific_details = SportSpecificDetails(cricket=CricketDetails(**sport_specific_details))
        elif sport_type and sport_type.lower() == "kabaddi":
            sport_specific_details = SportSpecificDetails(kabaddi=KabaddiDetails(**sport_specific_details))
        elif sport_type and sport_type.lower() == "basketball":
            sport_specific_details = SportSpecificDetails(basketball=BasketballDetails(**sport_specific_details))
        elif sport_type and sport_type.lower() == "hockey":
            sport_specific_details = SportSpecificDetails(hockey=HockeyDetails(**sport_specific_details))
        elif sport_type and sport_type.lower() == "badminton":
            sport_specific_details = SportSpecificDetails(badminton=BadmintonDetails(**sport_specific_details))
    
    # Populate the tournament data model
        tournament_data = UpateTournament(
            tournament_name=tournament_name,
            sport_type=sport_type,
            location=location,
            start_date=start_date,
            end_date=end_date,
            rules=rules,
            max_teams=max_teams,
            match_format=match_format,
            team_size=team_size,
            entry_fee=entry_fee,
            prize=prize,
            sport_specific_details=sport_specific_details
        )
    
    # Prepare update data, excluding any unset fields
        tournament = tournament_data.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in tournament.items() if v is not None}
    
    # Perform the update in the repository
        update_tournament = await tournament_creation_repo.update(tournament_exists["_id"], update_data)
    
        return {"message": "Tournament updated successfully"}
    
    async def update_tournament_profile(self, tournament_name: str, tournament_image: UploadFile = None):
    
    # Check if the tournament exists in the database
        tournament = await tournament_creation_repo.find_by({"tournament_name": tournament_name})
        if not tournament:
            raise HTTPException(
            status_code=404, detail="Tournament data not found in the database."
        )

    # Delete the existing image (if exists) associated with the tournament
        if tournament.get("tournament_image_url"):
            await tournament_creation_repo.delete_image(tournament["tournament_image_url"])

    # Upload the new image
        if tournament_image:
            block_image_url = await tournament_creation_repo.upload_image(tournament_image)
        # Update the tournament record with the new image URL
        await tournament_creation_repo.update(tournament["_id"], {"tournament_image_url": block_image_url})

        return {"message": "Tournament image updated successfully."}
    
    async def delete_tournament(self,tournament_name :str):
        tournament = await tournament_creation_repo.find_by({"tournament_name": tournament_name})
        if not tournament:
            raise HTTPException(status_code=404, detail="Tournament not found with the given Name.")
        if tournament["tournament_image_url"] is not None:
            delete_tournament_profile = await delete_file_from_github(tournament["tournament_image_url"])

            if delete_tournament_profile.status_code != 200:
                raise HTTPException(status_code=409, detail="Conflict: Unable to delete the profile")

        await tournament_creation_repo.delete(tournament["_id"])
        return {"message": "Tournament Deleted successfully"}
        
        

        
    


