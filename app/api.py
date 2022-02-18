from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data import MongoDB
from app.model import MatcherSortSearch

API = FastAPI(
    title='Underdog Devs DS API',
    version="0.43.5",
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


@API.get("/collections")
async def collections():
    """ Returns collection name and size of each collection. """
    return {"result": API.db.get_database_info()}


@API.post("/{collection}/create")
async def create(collection: str, data: Dict):
    """ Creates a new record. """
    return {"result": API.db.create(collection, data)}


@API.post("/{collection}/read")
async def read(collection: str, data: Optional[Dict] = None):
    """ Returns array of records that exactly match the query. """
    return {"result": API.db.read(collection, data)}


@API.post("/{collection}/update")
async def update(collection: str, query: Dict, update_data: Dict):
    """ Returns an array containing the query and updated data. """
    return {"result": API.db.update(collection, query, update_data)}


@API.post("/{collection}/search")
async def collection_search(collection: str, search: str):
    """ Returns array of records that loosely match the search,
    automatically ordered by relevance. """
    return {"result": API.db.search(collection, search)}


@API.post("/match/{profile_id}")
async def match(profile_id: int, n_matches: int):
    """ Returns array of mentor matches for any given mentee profile_id
    automatically ordered by relevance. """
    return {"result": API.matcher(n_matches, profile_id)}


@API.delete("/{collection}/delete/{profile_id}")
async def delete(collection: str, profile_id: int):
    """ Removes a user from the collection """
    API.db.delete(collection, {"profile_id": profile_id})
    return {"result": {"deleted": profile_id}}
