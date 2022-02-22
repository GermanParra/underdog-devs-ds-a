from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.model import MatcherSortSearch

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.43.7",
    docs_url='/',
)

API.db = MongoDB("UnderdogDevs")
API.matcher = MatcherSortSearch()

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version")
async def version():
    """ Returns the current version of the API. """
    return {"result": API.version}

# Data.py Starts
@API.get("/collections")
async def collections():
    """ Returns collection name and size of each collection. """
    return {"result": API.db.get_database_info()}


@API.post("/{collection}/create")
async def create(collection: str, data: Dict):
    """ Creates a new record.
    Input Example:
    collection = "Mentees"
    data = {
        "profile_id": "test001",
        "first_name": "Luca",
        "last_name": "Evans",
        "email": "fake@email.com",
        "city": "Ashland",
        "state": "Oregon",
        "country": "USA",
        "formerly_incarcerated": true,
        "underrepresented_group": true,
        "low_income": true,
        "list_convictions": [
          "Infraction",
          "Felony"
        ],
        "subject": "Web: HTML, CSS, JavaScript",
        "experience_level": "Beginner",
        "job_help": false,
        "industry_knowledge": false,
        "pair_programming": true,
        "other_info": "Notes"
    }
    """
    return {"result": API.db.create(collection, data)}


@API.post("/{collection}/create_many")
async def create(collection: str, data: Dict):
    """ Creates multiple new record.
    Input Example:
    collection = "Mentees"
    data = { "profile_one" :
                { 
                    "profile_id": "test001",
                    "first_name": "Luca",
                    "last_name": "Evans",
                    "email": "fake@email.com",
                    "city": "Ashland", 
                    "state": "Oregon", 
                    "country": "USA", 
                    "formerly_incarcerated": true, 
                    "underrepresented_group": true, 
                    "low_income": true, 
                    "list_convictions": [ "Infraction", "Felony" ],
                    "subject": "Web: HTML, CSS, JavaScript", 
                    "experience_level": "Beginner", 
                    "job_help": false, 
                    "industry_knowledge": false, 
                    "pair_programming": true, 
                    "other_info": "Notes"
                },
                "profile_two" :
                { 
                    "profile_id": "test002",
                    "first_name": "Luca's Twin",
                    "last_name": "Evans",
                    "email": "fake@email.com",
                    "city": "Ashland", 
                    "state": "Oregon", 
                    "country": "USA", 
                    "formerly_incarcerated": true, 
                    "underrepresented_group": true, 
                    "low_income": true, 
                    "list_convictions": [ "Infraction", "Felony" ],
                    "subject": "Web: HTML, CSS, JavaScript", 
                    "experience_level": "Beginner", 
                    "job_help": false, 
                    "industry_knowledge": false, 
                    "pair_programming": true, 
                    "other_info": "Notes"
                }
    """
    print(data)
    return {"result": API.db.create(collection, data)}


@API.post("/{collection}/first")
async def first(collection: str, query: Optional[Dict] = None):
    """ Returns first match that occurs with query in a collection. """
    return {"result": API.db.first(collection, query)}


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """ Returns array of records that exactly match the query. """
    return {"result": API.db.read(collection, data)}


@API.post("/{collection}/update")
async def update(collection: str, query: Dict, update_data: Dict):
    """ Returns an array containing the query and updated data. """
    return {"result": API.db.update(collection, query, update_data)}

@API.delete("/{collection}/delete/{profile_id}")
async def delete(collection: str, profile_id: str):
    """ Removes a user from the collection """
    API.db.delete(collection, {"profile_id": profile_id})
    return {"result": {"deleted": profile_id}}

@API.post("/{collection}/count")
async def count(collection: str, query: Optional[Dict] = None):
    """ Returns the amount of times a query appears in a collection. """
    return {"result":  API.db.count(collection, query)}

@API.post("/{collection}/search")
async def collection_search(collection: str, search: str):
    """ Returns array of records that loosely match the search,
    automatically ordered by relevance. """
    return {"result": API.db.search(collection, search)}

# Data.py ends

@API.post("/match/{profile_id}")
async def match(profile_id: str, n_matches: int):
    """ Returns array of mentor matches for any given mentee profile_id
    automatically ordered by relevance. """
    return {"result": API.matcher(n_matches, profile_id)}


