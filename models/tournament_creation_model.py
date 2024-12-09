from pydantic import BaseModel, Field,json
from typing import Optional, Union
from enum import Enum
from datetime import datetime
from utilities.utils import PyObjectId
from bson import ObjectId


class SportType(str, Enum):
    cricket = "Cricket"
    kabaddi = "Kabaddi"
    basketball = "Basketball"
    hockey = "Hockey"
    badminton = "Badminton"

class TournamentPrize(BaseModel):
    first_place: str
    second_place: str
    third_place: str

class CricketDetails(BaseModel):
    overs_per_innings: Optional[int] = None
    ball_type: Optional[str] = None  # E.g., "Leather", "Tennis"

class KabaddiDetails(BaseModel):
    match_duration: Optional[int] = None  # in minutes
    court_size: Optional[str] = None  # E.g., "13m x 10m"

class BasketballDetails(BaseModel):
    quarters: Optional[int] = None
    court_type: Optional[str] = None  # E.g., "Indoor", "Outdoor"

class HockeyDetails(BaseModel):
    field_type: Optional[str] = None  # E.g., "Turf", "Grass"
    match_duration: Optional[int] = None

class BadmintonDetails(BaseModel):
    match_type: Optional[str] = None  # E.g., "Singles", "Doubles"

class SportSpecificDetails(BaseModel):
    cricket: Optional[CricketDetails] = None
    kabaddi: Optional[KabaddiDetails] = None
    basketball: Optional[BasketballDetails] = None
    hockey: Optional[HockeyDetails] = None
    badminton: Optional[BadmintonDetails] = None

class TournamentCreation(BaseModel):
    tournament_name: str
    sport_type: str
    location: str
    start_date:str
    end_date: str
    rules: Optional[str] = None
    max_teams: int
    match_format: Optional[str] = None  # E.g., "T20", "3x3"
    team_size: int
    entry_fee: Optional[int] = None
    prize: TournamentPrize
    sport_specific_details: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    #tournament_image_url:HttpUrl
class UpateTournament(BaseModel):
    tournament_name: Optional[str] = None
    sport_type: Optional[str] = None
    location: Optional[str] = None
    start_date:Optional[str] = None
    end_date: Optional[str] = None
    rules: Optional[str] = None
    max_teams: Optional[int] = None
    match_format: Optional[str] = None  # E.g., "T20", "3x3"
    team_size: Optional[int] = None
    entry_fee: Optional[float] = None
    prize: Optional[TournamentPrize] = None
    sport_specific_details: Optional[str] = None
    
