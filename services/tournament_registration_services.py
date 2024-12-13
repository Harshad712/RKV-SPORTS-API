from utilities.git_hub_utilities import upload_to_github,delete_file_from_github
from typing import Optional
from datetime import datetime
from fastapi import HTTPException,UploadFile
from models.tournament_registration_model import TournamentRegistration,Player,RegistrationStatus,UpdateTeamDetails
from typing import List,Optional
from repository.tournament_repo import tournament_registration_repo


class TournamentRegristrationService:
    
    async def register_tournament(self,
    team_name: str ,
    tournament_name:str,
    sport_type:str,
    player_ids: List[str] ,  # List of player IDs
    player_names: List[str] ,  # List of player names
    player_positions: List[Optional[str]] =None,  # List of player positions
    coach_name: Optional[str] = None ,
    contact_number: Optional[str] = None ,
    registration_fee: Optional[float] = None ,
    additional_notes: Optional[str] = None,
    registration_date: Optional[datetime] = datetime.utcnow(),  # Default value set directly
    status: RegistrationStatus = RegistrationStatus.pending ,# Default value set directly
    team_profile : UploadFile = None
):
        team_exists = await tournament_registration_repo.find_by({"team_name":team_name.lower()})
        if team_exists:
            raise HTTPException(status_code=400,detail="A team already exists with the same name.")
         # Initialize a new list to store updated player details
        updated_players = []

        # Update player details if provided
        if player_ids and player_names:
            for i in range(len(player_ids)):
            
                    # Add new player if not already in the existing list
                    new_player = {
                        "player_id": player_ids[i],
                        "name": player_names[i],
                        "position": player_positions[i] if player_positions else None
                    }
                    updated_players.append(new_player)
        
        tournament_registration = TournamentRegistration(
        team_name=team_name,
        tournament_name=tournament_name,
        sport_type=sport_type,
        players=updated_players,
        coach_name=coach_name,
        contact_number=contact_number,
        registration_fee=registration_fee,
        additional_notes=additional_notes,
        registration_date=registration_date,
        status=status,
    )
        team = tournament_registration.model_dump(exclude_unset=True)

    # Check if the team already exists
        

    # Upload team image and add the URL to team data
        team_profile_url = await tournament_registration_repo.upload_image(team_profile)
        team["team_profile_url"] = team_profile_url
        team_data = {k: v for k, v in team.items()if v is not None}
    # Create team registration in the database
        await tournament_registration_repo.create(team_data)

    # Return success message 
        return {"message": "Team registered  successfully"}
    
    async def get_all_teams(self):
    # Fetch all teams
        teams = await tournament_registration_repo.get_all()
    
    # Check if teams are found before iterating
        if not teams:
            raise HTTPException(status_code=404, detail="No teams found.")
    
    # Convert ObjectId to string for JSON serialization
        for team in teams:
            team["_id"] = str(team["_id"])
        
    # Return teams in a structured format
        return teams
    
    async def get_team_by_name(self, team_name: str):
    # Find the team by name
        team = await tournament_registration_repo.find_by({"team_name": team_name})
    
    # If no team is found, raise a 404 error
        if not team:
            raise HTTPException(status_code=404, detail="No team found.")
    
    # Convert _id to string for JSON serialization
        team["_id"] = str(team["_id"])
    
    # Return the tournament in a structured format
        return  team
    
    async def update_team_details(
        self,
        team_name: str,
        player_ids: Optional[List[str]] = None,  # List of player IDs
        player_names: Optional[List[str]] = None,  # List of player names
        player_positions: Optional[List[Optional[str]]] = None,  # List of player positions
        coach_name: Optional[str] = None,
        contact_number: Optional[str] = None,
        additional_notes: Optional[str] = None,
        status: Optional[RegistrationStatus] = None,
    ):
        # Fetch the team to be updated
        team = await tournament_registration_repo.find_by({"team_name": team_name})
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found.")
        
       
        
        # Get existing players from the database
        existing_players = team.get("players", [])

        # Initialize a new list to store updated player details
        updated_players = []

        # Update player details if provided
        if player_ids and player_names:
            for i in range(len(player_ids)):
                # Check if the player is already in the existing player list
                existing_player = next((p for p in existing_players if p["player_id"] == player_ids[i]), None)
            
                if existing_player:
                    # Update the existing player details
                    existing_player["name"] = player_names[i]
                    existing_player["position"] = player_positions[i] if player_positions else existing_player.get("position")
                    updated_players.append(existing_player)
                else:
                    # Add new player if not already in the existing list
                    new_player = {
                        "player_id": player_ids[i],
                        "name": player_names[i],
                        "position": player_positions[i] if player_positions else None
                    }
                    updated_players.append(new_player)
    
        # Combine updated players with any existing players that were not modified
        for player in existing_players:
            if player["player_id"] not in player_ids:
                updated_players.append(player)
      

      
        updated_team = UpdateTeamDetails(team_name=team_name,
                                          players=updated_players,
                                          coach_name=coach_name,
                                          contact_number=contact_number,
                                          additional_notes=additional_notes,
                                          status=status)
        
        team_data = updated_team.model_dump(exclude_unset=True)
        updated_data = {k: v for k, v in team_data.items()if v is not None}

        # Update the team in the database
        result = await tournament_registration_repo.update( team["_id"], updated_data)
        
        # If no document is updated, raise an error
        if not result:
            raise HTTPException(status_code=400, detail="Failed to update team details.")

        # Return success message
        return {"message": "Team details updated successfully."}
    
    async def update_team_profile(self, team_name: str, team_profile: UploadFile = None):
    
    # Check if the team exists in the database
        team = await tournament_registration_repo.find_by({"team_name": team_name})
        if not team:
            raise HTTPException(
            status_code=404, detail="team data not found in the database."
        )

    # Delete the existing image (if exists) associated with the team
        if team.get("tournament_image_url"):
            await tournament_registration_repo.delete_image(team["team_profile_url"])

    # Upload the new image
        if team_profile:
            team_image_url = await tournament_registration_repo.upload_image(team_profile)
        # Update the team record with the new image URL
        await tournament_registration_repo.update(team["_id"], {"team_profile_url": team_image_url})

        return {"message": "Team profile updated successfully."}
    
    async def delete_team(self,team_name :str):
        team = await tournament_registration_repo.find_by({"team_name": team_name})
        if not team:
            raise HTTPException(status_code=404, detail="Team not found with the given Name.")
        if team["team_profile_url"] is not None:
            delete_team_profile = await delete_file_from_github(team["team_profile_url"])

            if delete_team_profile.status_code != 200:
                raise HTTPException(status_code=409, detail="Conflict: Unable to delete the profile")

        await tournament_registration_repo.delete(team["_id"])
        return {"message": "Team Deleted successfully"}
        
    