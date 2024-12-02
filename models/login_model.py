from pydantic import BaseModel
from datetime import datetime

class refresh_token_request(BaseModel):
    refresh_token : str
    access_token : str

class token_revocation(BaseModel):
    username:str
    access_token:str
    refresh_token:str
    expires_at: datetime
    #used to check the token_revocation status
    revoked_status:bool
