from motor.motor_asyncio import  AsyncIOMotorCollection
from typing import TypeVar
from models.match_model import Matches
from repository.crud_repo import CrudRepository  
from utilities.utils import client



my_db = client['Rkv-Sports']
matches_db = my_db.matches

T = TypeVar('T', bound=Matches)
class MatchesRepository(CrudRepository[Matches]):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
   
    



# Instantiate the NewsRepository
matches_repo = MatchesRepository(matches_db)

