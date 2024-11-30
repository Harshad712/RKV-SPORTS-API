from motor.motor_asyncio import  AsyncIOMotorCollection
from typing import TypeVar
from models.news_model import news_block,update_news
from repository.crud_repo import CrudRepository  
from utilities.utils import client



my_db = client['Rkv-Sports']
news_db = my_db.news

T = TypeVar('T', bound=news_block)
class NewsRepository(CrudRepository[news_block]):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)
   
    



# Instantiate the NewsRepository
news_repo = NewsRepository(news_db)

