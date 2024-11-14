from fastapi import APIRouter,File,Form,UploadFile
from controllers.tournament_creation_controller import Tournamentcreation
from models.tournament_creation_model import TournamentCreation,TournamentPrize,SportSpecificDetails
from typing import Optional
from datetime import datetime
from pydantic import Field

app = APIRouter(tags=['TournamentCreation'])

@app.post("/",summary="Creates the Tournaments")
async def create_tournament(
    tournament_name: str = Form(...),  # required parameter
    sport_type: str = Form(...),  # required parameter
    location: str = Form(...),  # required parameter
    start_date: str = Form(...),  # required parameter
    end_date: str = Form(...),  # required parameter
    max_teams: int = Form(...),  # required parameter
    team_size: int = Form(...),  # required parameter
    prize_first_place: str = Form(...),  # required parameter for prize
    prize_second_place: str = Form(...),  # required parameter for prize
    prize_third_place: str = Form(...),  # required parameter for prize
    rules: Optional[str] = Form(None),  # optional parameter
    match_format: Optional[str] = Form(None),  # optional parameter
    entry_fee: Optional[float] = Form(None),  # optional parameter
    sport_specific_details: Optional[str] = Form(None),  # optional parameter
    tournament_image: UploadFile = File(...),  # file upload parameter
):
    """An API EndPoint to create the tournaments"""
    
    return await Tournamentcreation.create_tournament(tournament_name,
                                                      sport_type,
                                                      location,
                                                      start_date,
                                                      end_date,
                                                      max_teams,
                                                      team_size,
                                                      prize_first_place,
                                                      prize_second_place,
                                                      prize_third_place,
                                                      rules,
                                                      match_format,
                                                      entry_fee,
                                                      sport_specific_details,
                                                      tournament_image)

@app.get("/",summary= "fetches all the tournaments created")
async def get_all_tournaments():
    """An API EndPoint to fetch all tournaments created"""
    return await Tournamentcreation.get_all_tournaments()

@app.get("/{tournament_name}",summary="fetches the tournament by name")
async def get_tournament_name(tournament_name:str):
    """An API EndPoint to fetch the tournament by name."""
    return await Tournamentcreation.get_tournament_name(tournament_name)

@app.put("/",summary = "Updates the tournament_details")
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
    """An API EndPoint to Update the Tournament details."""
    return await Tournamentcreation.update_tournament_details( tournament_name=tournament_name,
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
@app.put("/UpdateProfle",summary = "Updates the Profile of the tournaments")
async def update_tournament_profile(tournament_name: str = Form(...), tournament_image: UploadFile = File(...)):
    """An API EndPoint to Update The Tournament Profle."""
    return await Tournamentcreation.update_tournament_profile(tournament_name,tournament_image)

@app.delete("/",summary = "Deletes the Tournaments")
async def delete_tournament(tournament_name :str):
    """An API EndPoint to Delete the Tournament by name."""
    return await Tournamentcreation.delete_tournament(tournament_name)