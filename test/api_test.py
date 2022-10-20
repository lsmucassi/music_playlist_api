from uuid import uuid4
import requests
import random

ENDPOINT = "https://vfadintjowlokam5vklcwimxyy0wprvb.lambda-url.us-east-1.on.aws/"


# ===============================================================================
# TESTS
def test_create_and_get_playlist():
    '''
    Test the create and get playlist'''
    songs = create_randssngs()
    # create a playlist
    create_res = create_playlist(songs)
    # assert that the create method executed succesfully
    assert create_res.status_code == 200

    # get the created playlist
    new_playlist_id = create_res.json()["playlist"]["playlist_id"]
    get_res = get_playlist(new_playlist_id)
    assert get_res.status_code == 200

    # compare content
    playlist = get_res.json()
    # assert playlist["playlist"]["user_id"] == user_id
    assert playlist["playlist"]["songs"] == songs


def test_update():
    '''
        Test if a song can be added or removed in a playlist
    '''
    # create a playlist
    songs = create_randssngs()
    create_res = create_playlist(songs)
    assert create_res.status_code == 200

    # get the recently created playlist and remove a song
    new_playlist_id = create_res.json()["playlist"]["playlist_id"]
    get_res = get_playlist(new_playlist_id)
    assert get_res.status_code == 200

    # remove a song
    new_songs = get_res.json()["playlist"]["songs"]
    if new_songs:
        song_id = new_songs[0]
        #  remove
        update_remove_res = update_playlist(new_playlist_id,
                                            song_id,
                                            add_track=False)
        assert update_remove_res.status_code == 200

        # add a song
        song_id = f"song_id_{uuid4().hex}"
        update_add_res = update_playlist(new_playlist_id,
                                         song_id,
                                         add_track=False)
        assert update_add_res.status_code == 200


def test_delete_playlist():
    '''
        Test if a playlist can be deleted
    '''
    # create a playlist
    songs = create_randssngs()
    create_res = create_playlist(songs)
    assert create_res.status_code == 200

    # get the recently created playlist and remove a song
    new_playlist_id = create_res.json()["playlist"]["playlist_id"]
    get_res = get_playlist(new_playlist_id)
    assert get_res.status_code == 200

    # remove the playlist
    delete_res = delete_playlist(new_playlist_id)
    assert delete_res.status_code == 200

    # try to get deleted playlist, should return a 404
    get_playlist_res = get_playlist(new_playlist_id)
    assert get_playlist_res.status_code == 404


# ===============================================================================
# HELPER FUNCTIONS
def create_randssngs() -> dict:
    ''' creates random song ids'''
    songs = []

    for _ in range(0, random.randint(1, 10)):
        songs.append(f"song_id_{uuid4().hex}")

    return songs


def create_playlist(songs: list) -> dict:
    ''' creates a payload and request the create endpoint'''
    user_id = f"user_id_{uuid4().hex}"
    playlist_id = f"playlist_id_{uuid4().hex}"
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


def update_playlist(playlist_id: str, song_id: str, add_track: bool) -> dict:
    '''updates a playlist by adding or removing a song'''
    res = requests.put(
        f"{ENDPOINT}/update-playlist?playlist_id={playlist_id}&song_id={song_id}&add_track={add_track}"
    )
    return res


def delete_playlist(playlist_id: str) -> dict:
    res = requests.delete(f"{ENDPOINT}/delete-playlist/{playlist_id}")
    return res