from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MatchStatus(str,Enum):
    LIVE = "live"
    PAST = "past"
    UPCOMING = "upcoming"

class Matches(BaseModel):
    match_id : str
    team1_name :str
    team2_name :str
    team1_score :str
    team2_score :str
    match_status :MatchStatus
    #team1_profile_url:str
    #team2_profile_url:str
    
class update_match(BaseModel):
    match_id:str
    team1_score:Optional[str]
    team2_score:Optional[str]
    match_status:Optional[MatchStatus]