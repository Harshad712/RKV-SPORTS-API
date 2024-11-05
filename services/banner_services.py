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

        banner_content = await banner_image.read()
        banner_response = await upload_to_github(banner_content, banner_image.filename)
        if banner_response.status_code == 201 :
            banner_url = banner_response.json().get("content", {}).get("html_url", "")
        else :
            raise HTTPException(
                status_code= 400,
                detail= "Error While Uploading into github"
            )
        banner["banner_link"] = banner_url
        await banner_repo.create(banner)
        return {"message":"Banner Created Successfully"}
    
    async def update_banner(self,banner_id : str,banner_image: UploadFile = File(...)):

        banner = await banner_repo.find_by({"banner_id":banner_id})

        if not banner :
            raise HTTPException(status_code = 404 , detail = "Banner not found with the given id.")
        
        #Deleting the old banner_image form the github
        banner_delete = await delete_file_from_github(banner["banner_link"])

        if banner_delete.status_code !=200 :
            raise HTTPException(
                status_code = 409,
                detail = "Conflict : Unalbe to upload the banner"
            )

        #uploading the new banner_image  into github
        banner_content = await banner_image.read()

        banner_response  = await upload_to_github(banner_content,banner_image.filename)

        if banner_response.status_code == 201:
            banner_url = banner_response.json().get("content", {}).get("html_url", "")
        else :
            raise HTTPException(
                status_code=400, detail="Error Uploading file into github"
            )
        await banner_repo.update(banner["_id"],{"banner_link":banner_url})

        return {"message":"Banner Updated successfully"}
    async def delete_banner(self,banner_id:str):

        banner = await banner_repo.find_by({"banner_id":banner_id})

        if not banner :
            raise HTTPException(status_code = 404 , detail = "Banner not found with the given id.")
        
        banner_delete = await delete_file_from_github(banner["banner_link"])

        if banner_delete.status_code !=200 :
            raise HTTPException(
                status_code = 409,
                detail = "Conflict : Unalbe to delete the banner"
            )
        await banner_repo.delete(banner["_id"])
        return {"message":"Banner deleted successfully."}

