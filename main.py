from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes.students as students
import routes.banner as banner
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify a list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#including routers
app.include_router(students.app,prefix="/students")
app.include_router(banner.app,prefix = "/banner")


@app.get("/",tags=["Root"])
async def root_message():
    return {"Detail":"Welcome to the  RKVSPORTS-API. Use the docs to get started."}