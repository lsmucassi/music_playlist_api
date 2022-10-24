import os
from urllib import response
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


# ===============================================================================
# Playlist Model for Database
class PutPlaylistReq(BaseModel):
    songs: list
    playlist_id: Optional[str] = None
    user_id: Optional[str] = None


# ===============================================================================
# HELPER FUNCTIONS
def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource("dynamodb").Table(table_name)


def _get_playlist(playlist_id: str, table):
    response = table.get_item(Key={"playlist_id": playlist_id})
    item = response.get("Item")

    return item


def _get_all_playlists(table):
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data


def _update_playlist(playlist_id: str, songs: list, table):

    try:
        response = table.update_item(Key={
            'playlist_id': playlist_id,
        },
                                     UpdateExpression="set songs = :r",
                                     ExpressionAttributeValues={
                                         ':r': songs,
                                     },
                                     ReturnValues="UPDATED_NEW")
    except:
        return HTTPException(status_code=500,
                             detail=f"ERROR: Internal Server Error")

    return response


def _response(status_code, message):
    return HTTPException(status_code=status_code, detail=message)


# ===============================================================================
# Root of the API
@app.get("/")
def root():
    ''' root endpoint'''
    return {
        "message": "Welcome to your playlists(Create, Read, Update & Delete)"
    }


# endpoint to create a playlist
@app.post("/create-playlist")
async def create_playlist(put_playlist_req: PutPlaylistReq):
    ''' endpoint to create a playlist
        - takes in playlist, user and songs as a list
    '''
    item = {
        "playlist_id": f"playlist_{uuid.uuid4().hex}",
        "user_id": put_playlist_req.user_id,
        "songs": put_playlist_req.songs,
    }
    table = _get_table()
    # upload data to table
    table.put_item(Item=item)

    return {"playlist": item, "response": ""}


# endpoint to get a single playlist
@app.get("/get-playlist/{playlist_id}")
async def get_playlist(playlist_id: str):
    '''
        endpoint to get a playlist by ID
    '''
    table = _get_table()

    item = _get_playlist(playlist_id, table)
    if not item:
        raise _response(404, f"Playlist {playlist_id} Not Found!")

    return {"playlist": item}


# # endpoint to get all playlists
@app.get("/get-playlists")
async def get_playlist():
    ''' endpoint to get all playlists '''

    table = _get_table()
    data = _get_all_playlists(table)

    return {"playlists": data}


# # endpoint to update playlist: Remove or add songs
@app.put("/update-playlist")
async def update_playlist(playlist_id: str, song_id: str, add_track: bool):
    ''' endpoint to add or remove a song in a playlist '''
    table = _get_table()
    item = _get_playlist(playlist_id, table)

    if item and song_id:
        songs = item["songs"]
        if add_track:
            # add a track
            if song_id in songs:  # if the song already exists
                return _response(403,
                                 f"Song {song_id} Already Exists In Playlist")

            else:  # add it to the list of songs in the playlist
                songs.append(song_id)
                res = _update_playlist(playlist_id, songs, table)
                return _response(res['ResponseMetadata']['HTTPStatusCode'],
                                 f"Song {song_id} Added To Playlist")

        else:
            # remove the track
            if song_id in songs:
                songs.remove(song_id)
                res = _update_playlist(playlist_id, songs, table)
                return _response(res['ResponseMetadata']['HTTPStatusCode'],
                                 f"Song {song_id} Removed From Playlist")
            else:
                return _response(404, f"Song {song_id} Not Found In Playlist!")

    if not item:
        raise _response(404, f"Playlist {playlist_id} Not Found!")


# endpoint to delete a playlist
@app.delete("/delete-playlist/{playlist_id}")
async def delete_playlist(playlist_id: str):
    ''' endpoint to deletw a playlist '''
    table = _get_table()
    table.delete_item(Key={"playlist_id": playlist_id})
    return _response(200, f"Delete Playlist: {playlist_id}")