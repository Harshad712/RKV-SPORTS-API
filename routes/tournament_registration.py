from fastapi import APIRouter,Form,UploadFile,File,Body
from typing import Optional,List
from models.tournament_registration_model import TournamentRegistration,Player,RegistrationStatus
from controllers.tournament_registration_controller import TournamentRegistrationController
from datetime import datetime

tournament_registration = TournamentRegistrationController()
app = APIRouter(tags=['TournamentRegistration'])

@app.post("/",summary = "Registers the Team For tournament")
async def register_tournament(
    team_name: str = Form(...),
    tournament_name :str = Form(...),
    sport_type:str = Form(...),
    player_ids: List[str] = Form(...),  # List of player IDs
    player_names: List[str] = Form(...),  # List of player names
    player_positions: List[Optional[str]] = Form(None),  # List of player positions
    coach_name: Optional[str] = Form(None),
    contact_number: Optional[str] = Form(None),
    registration_fee: Optional[float] = Form(None),
    additional_notes: Optional[str] = Form(None),
    registration_date: Optional[datetime] = Form(default_factory=datetime.utcnow),
    status: RegistrationStatus = Form(default=RegistrationStatus.pending),
    team_profile : UploadFile = File(...)
):
    """An API  EndPoint to Register the team for tournament."""
    return await tournament_registration.register_tournament(team_name,tournament_name,sport_type,player_ids,player_names,player_positions,coach_name,contact_number,registration_fee,additional_notes,registration_date,status,team_profile)

@app.get("/",summary = "Fetches all the teams ")
async def get_all_teams():
    """An API EndPoint to fetch all the teams registered for tournaments."""
    return await tournament_registration.get_all_teams()

@app.get("/{team_name}",summary = "fetches the team by name")
async def get_team_by_name(team_name : str):
    """An API EndPoint to fetch the team by name."""
    return await tournament_registration.get_team_by_name(team_name)

@app.put("/",summary="Updates the team details.")
async def update_team_details(
        team_name: str = Form(...),
        player_ids: Optional[List[str]] = Form(None),
        player_names: Optional[List[str]] = Form(None),
        player_positions: Optional[List[Optional[str]]] = Form(None),
        coach_name: Optional[str] = Form(None),
        contact_number: Optional[str] = Form(None),
        registration_fee: Optional[float] = Form(None),
        additional_notes: Optional[str] = Form(None),
        registration_date: Optional[datetime] = Form(None),
        status: Optional[RegistrationStatus] = Form(None)
    ):
    """An API Endpoint to update the team details. """
    return await tournament_registration.update_team_details(team_name,player_ids,player_names,player_positions,coach_name,contact_number,registration_fee,additional_notes,registration_date,status)

@app.put("/updateprofile",summary = "updates the profile of the team")
async def update_team_profile(team_name:str = Form(...),team_profile :UploadFile = File(...)):
    """An API EndPoint to update the team profile"""
    return await tournament_registration.update_team_profile(team_name,team_profile)

@app.delete("/",summary = "Deletes the team")
async def delete_team(team_name:str):
    """An API EndPoint to delete the team"""
    return await tournament_registration.delete_team(team_name)