import os
import uuid
import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
handler = Mangum(app)

# enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# song schema
# class Song(BaseModel):
#     song_id: str


# Playlist Model for Database
class PutPlaylistReq(BaseModel):
    songs: list
    # songs: Union[list[Song], None] = None
    playlist_id: Optional[str] = None
    user_id: Optional[str] = None


# HELPER FUNCTIONS
def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)


def _get_playlist(playlist_id: str, table):
    response = table.get_item(Key={"playlist_id": playlist_id})
    item = response.get("Item")

    return item


def _insert_playlist(item: dict, table):
    # upload data to table
    table.put_item(Item=item)


def _get_all_playlists(table):
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data


# Root of the API
@app.get("/")
def root():
    return {
        "message": "Welcome to your playlists(Create, Read, Update & Delete"
    }


# endpoint to create a playlist
@app.put("/create-playlist")
async def create_playlist(put_playlist_req: PutPlaylistReq):
    item = {
        "playlist_id": f"playlist_{uuid.uuid4().hex}",
        "user_id": put_playlist_req.user_id,
        "songs": put_playlist_req.songs,
    }
    table = _get_table()
    res = _insert_playlist(item, table)

    return {"playlist": item, "response": res}


# endpoint to get a single playlist
@app.get("/get-playlist/{playlist_id")
async def get_playlist(playlist_id: str):
    table = _get_table()

    item = _get_playlist(playlist_id, table)
    if not item:
        raise HTTPException(status_code=404,
                            detail=f"Playlist {playlist_id} not found!")

    return item


# # endpoint to get all playlists
@app.get("/get-playlists")
async def get_playlist():
    table = _get_table()
    data = _get_all_playlists(table)

    return data


# # endpoint to update playlist: Remove or add songs
@app.put("/update-playlist")
async def update_playlist(playlist_id: str, song_id: str, removeOrAdd: bool):
    table = _get_table()
    item = _get_playlist(table)

    if removeOrAdd:
        # add a track
        return item
    else:
        # remove the track
        if not item:
            raise HTTPException(status_code=404,
                                detail=f"Playlist {playlist_id} not found!")


# # endpoint to delete a playlist
# @app.delete("/delete-playlist/{playlist_id}")
# async def delete_playlist(playlist_id: str):
#     pass