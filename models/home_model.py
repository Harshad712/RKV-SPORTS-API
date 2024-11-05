from pydantic import BaseModel,HttpUrl
from typing import Optional
import datetime


class BlockModel(BaseModel):
    block_name: str
    block_content: str
   # block_image_url: HttpUrl
