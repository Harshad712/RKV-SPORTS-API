from fastapi import HTTPException,UploadFile,File,Form
from repository.news_repo import news_repo
from models.news_model import news_block,update_news
from typing import Optional

class NewsServices:
    
    async def get_all_news(self) -> list :
        all_news = await news_repo.get_all()
        for news in all_news:
            news["_id"] = str(news["_id"])
        if not all_news:
            raise HTTPException(status_code=404, detail="No News Found.")
        return all_news
    async def get_news_byname(self,title: str) -> dict:
         
         news = await news_repo.find_by({"title":title})
         if not news:
            raise HTTPException(status_code=404, detail="No news found with the given title.")
         news["_id"] = str(news["_id"])
         return news
         
    async def update_news(self,title: str, news_content:str) -> dict:

        news = await news_repo.find_by({"title": title.lower()})
        if not news:
            raise HTTPException(status_code=404, detail="Data not found in the database.")
        updated_news = update_news(title = title,news_content = news_content)
        updated_data = updated_news.model_dump(exclude_unset=True)
        update_data = {k: v for k, v in updated_data.items()if v is not None}
        await news_repo.update(news["_id"],update_data)
        return {"message": "news updated successfully"}
    
    async def delete_news(self,title: str) -> dict:

        news = await news_repo.find_by({"title": title.lower()})
        if not news:
            raise HTTPException(
                status_code=404, detail="Data not found in the database.")
        await news_repo.delete_image(news["news_image_url"])
        
        await news_repo.delete(news["_id"])
        return {"message":"news Deleted Successfully."}
    
    async def create_news(self,title : str = Form(...),
                          sport_type :str = Form(...),
                           news_content : str = Form(...),
                           news_image : UploadFile = File(...)) -> dict:
        
        existing_news = await news_repo.find_by({"title": title.lower()})
        if existing_news:
            raise HTTPException(status_code=400, detail="news with this name already exists.")

        # Insert the new news
        new_news = news_block(
            title = title.lower(),
            sport_type=sport_type,
            news_content = news_content,
        )
        new_news = new_news.model_dump()

        
        news_image_url = await news_repo.upload_image(news_image)

        
        new_news["news_image_url"] = news_image_url

        
        await news_repo.create(new_news)
        return {"message":"news Created Successfully."}
    
    async def update_news_image(self,title:str = Form(...),news_image:UploadFile = File(...)):

        news = await news_repo.find_by({"title": title.lower()})
        if not news:
            raise HTTPException(
                status_code=404, detail="Data not found in the database.")
        await news_repo.delete_image(news["news_image_url"])
        news_image_url = await news_repo.upload_image(news_image)
        await news_repo.update(news["_id"],{"news_image_url":news_image_url})

        return {"message":"Image Updated Successfully."}

            
    
    
