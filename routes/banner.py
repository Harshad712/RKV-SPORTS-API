from fastapi import APIRouter, File, UploadFile, Form
from utilities.utils import client, handle_exception
from controllers.banner_controller import Banners

app = APIRouter(tags=['Banner'])


@app.post("/")
async def upload_banner(banner_id : str = Form(...),banner_image : UploadFile = File(...) ):
    """An API EndPoint to Upload the Banner."""
    return await Banners.upload_banner(banner_id=banner_id, banner_image= banner_image)


@app.get("/")
async def get_banners():
    """An API EndPoint to Fetch all the Banners."""
    return await Banners.get_banners()


@app.put("/")
async def update_banner(banner_id : str,banner_image: UploadFile = File(...)):
    """An API EndPoint to Update the Banner."""
    
    return await Banners.update_banner(banner_id = banner_id , banner_image = banner_image)

@app.delete("/" )
async def delete_banner(banner_id:str):
    """An API EndPoint to Delete the Banner."""
    return await Banners.delete_banner(banner_id = banner_id)