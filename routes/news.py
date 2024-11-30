from fastapi import APIRouter, File, UploadFile, Form
from controllers.news_controller import NewsController

app = APIRouter(tags=['News'])

@app.post("/",summary = "creates the news")
async def create_news(title : str = Form(...),sport_type : str = Form(...),news_content : str = Form(...),news_image : UploadFile = File(...)) :
    """An API EndPoint to create news"""
    return await NewsController.create_news(title ,sport_type,news_content,news_image )

@app.get("/",summary="fetches all news")
async def get_all_news():
    """An API EndPoints to fetch all news"""
    return await NewsController.get_all_news()

@app.get("/{title}",summary="fetches news by name")
async def get_news_byname(title: str) :
    """An API EndPoint to fetch news by name."""
    return await NewsController.get_news_byname(title)

@app.put("/",summary = "updates the news")
async def update_news(title: str, news_content:str):
    """An API EndPoint to update the news."""
    return await NewsController.update_news(title,news_content)

@app.put("/update_news_image",summary = "updates the cover image of the news")
async def update_news_image(title : str = Form(...),news_image : UploadFile = File(...)):
    """An API EndPoint to update the cover image of the news"""
    return await NewsController.update_news_image(title,news_image)

@app.delete("/",summary="deletes the news")
async def delete_news(title: str):
    """An API EndPoint to delete the news."""
    return await NewsController.delete_news(title)