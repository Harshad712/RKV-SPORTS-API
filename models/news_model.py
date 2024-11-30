from pydantic import BaseModel
from typing import Optional

class news_block(BaseModel):
    sport_type : str
    title : str
    news_content : str
    #news_image_url :str
    
class update_news(BaseModel):
    title:Optional[str] 
    news_content:Optional[str] 
    #news_image_url : str
     