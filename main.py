from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes.students as students
import routes.banner as banner
import routes.home as home 
import routes.tournament_creation as Tournaments_created
import routes.tournament_registration as Teams_registered
import routes.news as News



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
app.include_router(home.app,prefix="/home")
app.include_router(Tournaments_created.app,prefix="/TournamentsCreation")
app.include_router(Teams_registered.app,prefix="/TeamsRegistration")
app.include_router(News.app,prefix="/News")


@app.get("/",tags=["Root"])
async def root_message():
    return {"Detail":"Welcome to the  RKVSPORTS-API. Use the docs to get started."}