import requests

class MusixService:

    artist_url = "http://api.musixmatch.com/ws/1.1/track.search?apikey=%s&page_size=3&page=1&s_track_rating=desc&q_track=%s"
    lyrics_url = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey=%s&track_id=%s"
    def __init__(self, key):
        self.api_key = key 

    def search_artist_by_track(self, track):
        res = requests.get(self.artist_url % (self.api_key, track))
        if res.status_code == 200:
            tracks = res.json()['message']['body']['track_list']
            artist_list = [(track['track']['artist_name'], track['track']['track_id']) for track in tracks]
            return artist_list

    def get_lyrics_by_track_id(self, track_id):
        res = requests.get(self.lyrics_url % (self.api_key, track_id))
        if res.status_code == 200:
            if len(res.json()['message']['body']) == 0:
                return (track_id, None)
            else:
                return (track_id, res.json()['message']['body']['lyrics']['lyrics_body'])



if __name__ == "__main__":
    service = MusixService("")
    artist_tuple = service.search_artist_by_track("hello")
    print(service.get_lyrics_by_track_id("adele"))


