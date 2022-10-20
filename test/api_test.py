from uuid import uuid4
import requests
import random

ENDPOINT = "https://vfadintjowlokam5vklcwimxyy0wprvb.lambda-url.us-east-1.on.aws/"


# ===============================================================================
# TESTS
def test_create_and_get_playlist():
    '''
    Test the create and get playlist'''
    user_id = f"user_id_{uuid4().hex}"
    playlist_id = f"playlist_id_{uuid4().hex}"
    songs = create_randssngs()

    # create a playlist
    create_res = create_playlist(playlist_id, user_id, songs)
    # assert that the create method executed succesfully
    assert create_res.status_code == 200

    # get the created playlist
    new_playlist_id = create_res.json()["playlist"]["playlist_id"]
    get_res = get_playlist(new_playlist_id)
    assert get_res.status_code == 200

    # compare content
    playlist = get_res.json()
    assert playlist["playlist"]["user_id"] == user_id
    assert playlist["playlist"]["songs"] == songs


def test_update():
    '''
        Test if a song can be added or removed in a playlist
    '''
    # create a playlist
    user_id = f"user_id_{uuid4().hex}"
    playlist_id = f"playlist_id_{uuid4().hex}"
    songs = create_randssngs()

    create_res = create_playlist(playlist_id, user_id, songs)


# ===============================================================================
# HELPER FUNCTIONS
def create_randssngs() -> dict:
    ''' creates random song ids'''
    songs = []

    for _ in range(0, random.randint(1, 10)):
        songs.append(f"song_id_{uuid4().hex}")

    return songs


def create_playlist(playlist_id: str, user_id: str, songs: list) -> dict:
    ''' creates a payload and request the create endpoint'''
    payload = {
        "playlist_id": playlist_id,
        "user_id": user_id,
        "songs": songs,
    }

    return requests.put(f"{ENDPOINT}/create-playlist", json=payload)


def get_playlist(playlist_id: str) -> dict:
    ''' calls the get playlist by id endpoint '''

    res = requests.get(f"{ENDPOINT}/get-playlist/{playlist_id}")
    return res