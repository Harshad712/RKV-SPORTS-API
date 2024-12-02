from fastapi import HTTPException
from repository.match_repo import matches_repo
from repository.tournament_repo import tournament_registration_db
from models.match_model import Matches,MatchStatus,update_match
from typing import Optional

class MatchesServices:
    
    async def get_all_matches(self) -> list :
        all_matches = await matches_repo.get_all()
        for matches in all_matches:
            matches["_id"] = str(matches["_id"])
        if not all_matches:
            raise HTTPException(status_code=404, detail="No matches Found.")
        return all_matches
    async def get_matches_byname(self,match_id: str) -> dict:
         
         matches = await matches_repo.find_by({"match_id":match_id})
         if not matches:
            raise HTTPException(status_code=404, detail="No matches found with the given match_id.")
         matches["_id"] = str(matches["_id"])
         return matches
         
    async def update_matches(self,match_id: str, team1_score:Optional[str] = None, 
                             team2_score: Optional[str] = None,
                             match_status : Optional[MatchStatus] =None ) -> dict:

        matches = await matches_repo.find_by({"match_id": match_id})
        if not matches:
            raise HTTPException(status_code=404, detail="Data not found in the database.")
        updated_matches = update_match(match_id = match_id,team1_score=team1_score,team2_score=team2_score,match_status=match_status)
        updated_data = updated_matches.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in updated_data.items()if v is not None}
        await matches_repo.update(matches["_id"],update_data)
        return {"message": "match updated successfully"}
    
    async def delete_matches(self,match_id: str) -> dict:

        matches = await matches_repo.find_by({"match_id": match_id.lower()})
        if not matches:
            raise HTTPException(
                status_code=404, detail="Data not found in the database.")
       
        
        await matches_repo.delete(matches["_id"])
        return {"message":"matches Deleted Successfully."}
    
    async def create_matches(self,match_id : str ,
                             team1_name:str,
                             team2_name:str,
                             team1_score:str,
                             team2_score:str,
                             match_status:MatchStatus) -> dict:
        
        existing_matches = await matches_repo.find_by({"match_id": match_id.lower()})
        if existing_matches:
            raise HTTPException(status_code=400, detail="matches with this name already exists.")
        #fetches team1 profile
        team1 = await tournament_registration_db.find_one({"team_name":team1_name})
        if not team1:
            team1_profile_url = "https://www.google.com/imgres?q=default%20team%20profile%20picture&imgurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-vector%2Fbusiness-man-icon-team-work-260nw-404838214.jpg&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-vector%2Fbusiness-man-icon-team-work-404838214&docid=l7RYew6jLEbsKM&tbnid=8DfcrRA5HAkhqM&vet=12ahUKEwiYoInrwYmKAxXsTWwGHUovEWYQM3oECB0QAA..i&w=260&h=280&hcb=2&ved=2ahUKEwiYoInrwYmKAxXsTWwGHUovEWYQM3oECB0QAA"
        else :
            team1_profile_url = team1["team_profile_url"]
        #fetches team2 profile
        team2 = await tournament_registration_db.find_one({"team_name":team2_name})
        if team2:
            team2_profile_url = team2["team_profile_url"]
        else:
            team2_profile_url = "https://www.google.com/imgres?q=default%20team%20profile%20picture&imgurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-vector%2Fbusiness-man-icon-team-work-260nw-404838214.jpg&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-vector%2Fbusiness-man-icon-team-work-404838214&docid=l7RYew6jLEbsKM&tbnid=8DfcrRA5HAkhqM&vet=12ahUKEwiYoInrwYmKAxXsTWwGHUovEWYQM3oECB0QAA..i&w=260&h=280&hcb=2&ved=2ahUKEwiYoInrwYmKAxXsTWwGHUovEWYQM3oECB0QAA"

        # Insert the new matches
        new_match = Matches(
            match_id = match_id,
            team1_name=team1_name,
            team2_name=team2_name,
            team1_score=team1_score,
            team2_score=team2_score,
            match_status=match_status
        )
        new_matches = new_match.model_dump(exclude_unset=True)
        new_matches["team1_profile_url"] = team1_profile_url
        new_matches["team2_profile_url"] = team2_profile_url

        await matches_repo.create(new_matches)
        return {"message":"matches Created Successfully."}