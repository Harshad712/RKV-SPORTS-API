from fastapi import HTTPException, UploadFile, File,Form
from typing import List,Optional
from models.banner_model import Banner_model  
from repository.banner_repo import banner_repo  
from utilities.git_hub_utilities import upload_to_github, delete_file_from_github  # GitHub utility functions

class BannerService :

    async def get_banners(self) -> List[dict]:
        banners = await banner_repo.get_all()
        for banner in banners:
            banner["_id"] = str(banner["_id"])
        if not banners:
            raise HTTPException(status_code=404, detail="No Banners Found.")
        return banners
    
    async def upload_banner(self,banner_id : str = Form(...),banner_image : UploadFile = File(...) ) ->dict :

        banner = Banner_model(banner_id = banner_id)
        banner = banner.model_dump()

        banner_url = await banner_repo.upload_image(banner_image)
        banner["banner_link"] = banner_url
        await banner_repo.create(banner)
        return {"message":"Banner Created Successfully"}
    
    async def update_banner(self,banner_id : str,banner_image: UploadFile = File(...)):

        banner = await banner_repo.find_by({"banner_id":banner_id})

        if not banner :
            raise HTTPException(status_code = 404 , detail = "Banner not found with the given id.")
        
        #Deleting the old banner_image form the github
        await banner_repo.delete_image(banner["banner_link"])

        

        #uploading the new banner_image  into github
        banner_url = await banner_repo.upload_image(banner_image)
        await banner_repo.update(banner["_id"],{"banner_link":banner_url})

        return {"message":"Banner Updated successfully"}
    async def delete_banner(self,banner_id:str):

        banner = await banner_repo.find_by({"banner_id":banner_id})

        if not banner :
            raise HTTPException(status_code = 404 , detail = "Banner not found with the given id.")
        
        await banner_repo.delete_image(banner["banner_link"])
        await banner_repo.delete(banner["_id"])
        return {"message":"Banner deleted successfully."}

