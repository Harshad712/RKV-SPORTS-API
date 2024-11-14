from motor.motor_asyncio import AsyncIOMotorCollection
from typing import TypeVar, Union
from models.tournament_creation_model import TournamentCreation
from models.tournament_registration_model import TournamentRegistration
from repository.crud_repo import CrudRepository
from utilities.utils import client

# Initialize the database and collection
my_db = client['Rkv-Sports']
tournament_creation_db = my_db.tournaments_creations
tournament_registration_db = my_db.tournaments_registrations

# Define a type variable bound to models used in the repository
T = TypeVar('T', bound=Union[TournamentCreation, TournamentRegistration])

class TournamentRepository(CrudRepository[T]):
    """
    Repository class for performing CRUD operations on the tournament collection.
    Extends CrudRepository with models specific to tournament management.
    """
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

# Instantiate the tournament repository
tournament_creation_repo = TournamentRepository(tournament_creation_db)
tournament_registration_repo = TournamentRepository(tournament_registration_db)
