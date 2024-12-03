from fastapi import APIRouter
from controllers.matches_controller import MatchController
from models.match_model import MatchStatus
from typing import Optional



app = APIRouter(tags=['matches'])


@app.post("/",summary = "creates the matches")
async def create_matches(match_id : str ,
                          team1_name:str,
                           team2_name:str,
                           team1_score:str,
                           team2_score:str,
                           match_status:MatchStatus) -> dict:
    """An API EndPoint to create matches"""
    return await MatchController.create_matches(match_id=match_id,
                                                   team1_name=team1_name,
                                                   team2_name=team2_name,
                                                   team1_score=team1_score,
                                                   team2_score=team2_score,
                                                   match_status=match_status)

@app.get("/",summary="fetches all matches")
async def get_all_matches():
    """An API EndPoints to fetch all matches"""
    return await MatchController.get_all_matches()

@app.get("/{match_id}",summary="fetches matches by name")
async def get_matches_byname(match_id: str) :
    """An API EndPoint to fetch matches by name."""
    return await MatchController.get_matches_byname(match_id)

@app.put("/",summary = "updates the matches")
async def update_matches(match_id: str,team1_score :Optional[str] = None,
                             team2_score:Optional[str]= None,
                             match_status: Optional[MatchStatus] = None) -> dict:
    """An API EndPoint to update the matches."""
    return await MatchController.update_matches(match_id=match_id,team1_score=team1_score,team2_score=team2_score,
                                                   match_status=match_status)


@app.delete("/",summary="deletes the matches")
async def delete_matches(match_id: str):
    """An API EndPoint to delete the matches."""
    return await MatchController.delete_matches(match_id)
