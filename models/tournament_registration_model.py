from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
from utilities.utils import PyObjectId
from bson import ObjectId


class RegistrationStatus(str, Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    rejected = "Rejected"

class CricketPlayerInfo(BaseModel):
    batting_style: Optional[str] = None  # E.g., "Right-hand", "Left-hand"
    bowling_style: Optional[str] = None  # E.g., "Fast", "Spin"
    role : Optional[str] = None #E.g., "Batter","Bowler""

class KabaddiPlayerInfo(BaseModel):
    role: Optional[str] = None  # E.g., "Raider", "Defender"

class BasketballPlayerInfo(BaseModel):
    position: Optional[str] = None  # E.g., "Guard", "Forward"

class HockeyPlayerInfo(BaseModel):
    position: Optional[str] = None  # E.g., "Midfielder", "Goalkeeper"

class BadmintonPlayerInfo(BaseModel):
    play_style: Optional[str] = None  # E.g., "Aggressive", "Defensive"

class SportSpecificPlayerInfo(BaseModel):
    cricket: Optional[CricketPlayerInfo] = None
    kabaddi: Optional[KabaddiPlayerInfo] = None
    basketball: Optional[BasketballPlayerInfo] = None
    hockey: Optional[HockeyPlayerInfo] = None
    badminton: Optional[BadmintonPlayerInfo] = None

class Player(BaseModel):
    player_id: str
    name: str
    position: Optional[str] = None
    

class TournamentRegistration(BaseModel):
    #torunament_id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    team_name: str
    players: List[Player]
    coach_name: Optional[str] = None
    contact_number: Optional[str] = None
    registration_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    registration_fee: Optional[float] = None
    status: RegistrationStatus = RegistrationStatus.pending
    additional_notes: Optional[str] = None
    #team_profile_url : HttpUrl
    class Config:
        json_encoders = {
            ObjectId: str
        }
class UpdateTeamDetails(BaseModel):
    team_name: Optional[str] = None
    players : Optional[List[Player]] = None
    coach_name: Optional[str] = None
    contact_number: Optional[str] = None
    registration_fee: Optional[float] = None
    additional_notes: Optional[str] = None
    registration_date: Optional[datetime] = None
    status: Optional[RegistrationStatus] = None