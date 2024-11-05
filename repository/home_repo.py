from motor.motor_asyncio import  AsyncIOMotorCollection
from typing import TypeVar
from models.home_model import BlockModel
from repository.crud_repo import CrudRepository  
from utilities.utils import client


my_db = client['Rkv-Sports']
home_db = my_db.home

T = TypeVar('T',bound=BlockModel)

class HomeBlocks(CrudRepository[BlockModel]):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__(collection)

home_repo = HomeBlocks(home_db)