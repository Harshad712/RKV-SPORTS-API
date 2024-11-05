from motor.motor_asyncio import  AsyncIOMotorCollection
from typing import TypeVar
from models.banner_model import Banner_model
from repository.crud_repo import CrudRepository  
from utilities.utils import client

my_db = client['Rkv-Sports']
banner_db = my_db.banners

T = TypeVar('T',bound=Banner_model)

class BannerRepository(CrudRepository[Banner_model]):
    def __init__(self, collection:AsyncIOMotorCollection):
        super().__init__(collection)

banner_repo = BannerRepository(banner_db)
