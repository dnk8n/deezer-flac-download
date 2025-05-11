
import httpx

def get_album_info(playlist_id):
    # Step1: Try get all info from API first
    album_info = get_album_info_from_playlist(playlist_id)
    # Step2: Check through each id to make sure there is data
    for album_id, (artist_name, album_title, track_title) in album_info.copy().items():
        test = get_album_info_raw(album_id)
        if test.get("error"):
            print(f"BAD ALBUM: {album_id}")
            print(f"    artist_name: {artist_name}")
            print(f"    album_title: {album_title}")
            print(f"    track_title: {track_title}")
            del album_info[album_id]
            searched_album_info = search_album_info(track_title, artist_name)
            if searched_album_info:
                new_album_id = searched_album_info["album"]["id"]
                new_album_title = searched_album_info["album"]["title"]
                new_artist_name = searched_album_info["artist"]["name"]
                print(f'    REPLACED: {album_id} -> {new_album_id}')
                print(f'                         -> artist name: {new_artist_name}')
                print(f'                         -> album title: {new_album_title}')
                album_info[new_album_id] = (new_artist_name, new_album_title)
    return album_info

def search_album_info(track_title, artist_name=None, try_=0):
    url = "https://api.deezer.com/search?q="
    if artist_name:
        url = url + f'artist:"{artist_name}" '
    if track_title:
        url = url + f'track:"{track_title}"'
    print(f'    SEARCHING: {url}')
    with httpx.Client() as client:
        response = client.get(url)
        # We assume that the first entry is acceptable, as the closest match
        # if no match, try a more general search before moving on
        try:
            return response.json()["data"][0]
        except IndexError:
            try_ += 1
            if try_ < 3:
                return search_album_info(track_title, try_=try_)


def get_album_info_raw(album_id):
    url = f"https://api.deezer.com/album/{album_id}"
    with httpx.Client() as client:
        response = client.get(url)
        return response.json()

def get_album_info_from_playlist(playlist_id):
    url = f"https://api.deezer.com/playlist/{playlist_id}"
    with httpx.Client() as client:
        response = client.get(url)
        # NOTE: This has the added benefit of collapsing duplicate albums if the playlist contains more than 1 song from that album
        return {t["album"]["id"]: (t["artist"]["name"], t["album"]["title"], t["title"]) for t in response.json()['tracks']['data']}


def get_track_info_from_playlist(playlist_id):
    url = f"https://api.deezer.com/playlist/{playlist_id}"
    with httpx.Client() as client:
        response = client.get(url)
        # NOTE: This has the added benefit of collapsing duplicate albums if the playlist contains more than 1 song from that album
        return {t["id"]: (t["artist"]["name"], t["album"]["title"], t["title"]) for t in response.json()['tracks']['data']}

# Example usage:
playlist_id = 13342489063  # Replace with playlist id
# album_info = get_album_info(playlist_id)
track_info = get_track_info_from_playlist(playlist_id)
# print(album_info)
print(track_info)
# album_ids = [str(a) for a in album_info.keys()]
track_ids = [str(t) for t in track_info.keys()]
# print(' '.join(album_ids))
print(' '.join(track_ids))

# for a in album_ids:
#     print("https://www.deezer.com/en/album/" + a)
for t in track_ids:
    print("https://www.deezer.com/en/track/" + t)