from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

travel_time = input("Which year do you want? Type the data in this Format YYYY-MM-DD: ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{travel_time}")
response = response.text

soup = BeautifulSoup(response,"html.parser")
song_names_spans = soup.select(selector="li ul li h3")


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://github.com/plamere/spotipy/blob/master/spotipy/oauth2.py#L483-L490",
        client_id="ef7127b163204f1899ea55f3a21553a4",
        client_secret="eff92c823ebd48ef937f274a3221cfa6",
        show_dialog=True,
        cache_path="token.txt",
        username="Wali Murtaza",
    )
)
user_id = sp.current_user()["id"]

song_names = [name.getText().strip() for name in song_names_spans]

song_urls = []
year = travel_time.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        url = result["tracks"]["items"][0]["uri"]
        song_urls.append(url)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{travel_time} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)