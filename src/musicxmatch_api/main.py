import base64
import hashlib
import hmac
import json


import re
import urllib
from datetime import datetime
from enum import Enum
from functools import cache

import requests

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
SIGNATURE_KEY_BASE_URL = "https://s.mxmcdn.net/site/js/"


class EndPoints(Enum):
    GET_ARTIST = "artist.get"
    GET_TRACK = "track.get"
    GET_TRACK_LYRICS = "track.lyrics.get"
    SEARCH_TRACK = "track.search"
    SEARCH_ARTIST = "artist.search"
    GET_ARTIST_CHART = "chart.artists.get"
    GET_TRACT_CHART = "chart.tracks.get"
    GET_ARTIST_ALBUMS = "artist.albums.get"
    GET_ALBUM = "album.get"
    GET_ALBUM_TRACKS = "album.tracks.get"
    GET_TRACK_LYRICS_TRANSLATION = "crowd.track.translations.get"
    GET_TRACK_RICHSYNC = "track.richsync.get"


class MusixMatchAPI:
    def __init__(self, proxies=None):
        self.base_url = "https://www.musixmatch.com/ws/1.1/"
        self.headers = {"User-Agent": USER_AGENT}
        self.proxies = proxies
        self.secret = self.get_secret()

    @cache
    def get_latest_app(self):
        url = "https://www.musixmatch.com/search"

        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Cookie": "mxm_bab=AB",
        }
        response = requests.request("GET", url, headers=headers)
        # Fetch HTML content
        html_content = response.text

        # Regular expression to match `_app` script URLs
        pattern = r'src="([^"]*/_next/static/chunks/pages/_app-[^"]+\.js)"'

        # Find all matches
        matches = re.findall(pattern, html_content)

        # Extract the latest `_app` URL
        if matches:
            latest_app_url = matches[-1]  # Get the last match if multiple are found
        else:
            raise Exception("_app URL not found in the HTML content.")
        return latest_app_url

    @cache
    def get_secret(self):
        data = requests.get(
            self.get_latest_app(),
            headers=self.headers,
            proxies=self.proxies,
            timeout=5,
        )
        javascript_code = data.text

        # Regular expression to capture the string inside `from(...)`
        pattern = r'from\(\s*"(.*?)"\s*\.split'

        # Search for the encoded string
        match = re.search(pattern, javascript_code)

        if match:
            encoded_string = match.group(1)
            reversed_string = encoded_string[::-1]

            # Decode the reversed string from Base64
            decoded_bytes = base64.b64decode(reversed_string)

            # Convert bytes to a string
            decoded_string = decoded_bytes.decode("utf-8")
            return decoded_string
        else:
            raise Exception("Encoded string not found in the JavaScript code.")

    def generate_signature(self, url):
        current_date = datetime.now()
        l = str(current_date.year)
        s = str(current_date.month).zfill(2)
        r = str(current_date.day).zfill(2)
        message = (url + l + s + r).encode()
        key = self.secret.encode()
        hash_output = hmac.new(key, message, hashlib.sha256).digest()
        signature = (
            "&signature="
            + urllib.parse.quote(base64.b64encode(hash_output).decode())
            + "&signature_protocol=sha256"
        )
        return signature

    def search_tracks(self, track_query, page=1) -> dict:
        url = f"{EndPoints.SEARCH_TRACK.value}?app_id=web-desktop-app-v1.0&format=json&q={urllib.parse.quote(track_query)}&f_has_lyrics=true&page_size=100&page={page}"
        return self.make_request(url)

    def get_track(self, track_id=None, track_isrc=None) -> dict:
        if not (track_id or track_isrc):
            raise ValueError("Either track_id or track_isrc must be provided.")

        param = f"track_id={track_id}" if track_id else f"track_isrc={track_isrc}"
        url = f"{EndPoints.GET_TRACK.value}?app_id=web-desktop-app-v1.0&format=json&{param}"

        return self.make_request(url)

    def get_track_lyrics(self, track_id=None, track_isrc=None) -> dict:
        if not (track_id or track_isrc):
            raise ValueError("Either track_id or track_isrc must be provided.")

        param = f"track_id={track_id}" if track_id else f"track_isrc={track_isrc}"
        url = f"{EndPoints.GET_TRACK_LYRICS.value}?app_id=web-desktop-app-v1.0&format=json&{param}"

        return self.make_request(url)

    def get_artist_chart(self, country="US", page=1) -> dict:
        url = f"{EndPoints.GET_ARTIST_CHART.value}?app_id=web-desktop-app-v1.0&format=json&page_size=100&country={country}&page={page}"
        return self.make_request(url)

    def get_track_chart(self, country="US", page=1) -> dict:
        url = f"{EndPoints.GET_TRACT_CHART.value}?app_id=web-desktop-app-v1.0&format=json&page_size=100&country={country}&page={page}"
        return self.make_request(url)

    def search_artist(self, query, page=1) -> dict:
        url = f"{EndPoints.SEARCH_ARTIST.value}?app_id=web-desktop-app-v1.0&format=json&q_artist={urllib.parse.quote(query)}&page_size=100&page={page}"
        return self.make_request(url)

    def get_artist(self, artist_id) -> dict:
        url = f"{EndPoints.GET_ARTIST.value}?app_id=web-desktop-app-v1.0&format=json&artist_id={artist_id}"
        return self.make_request(url)

    def get_artist_albums(self, artist_id, page=1) -> dict:
        url = f"{EndPoints.GET_ARTIST_ALBUMS.value}?app_id=web-desktop-app-v1.0&format=json&artist_id={artist_id}&page_size=100&page={page}"
        return self.make_request(url)

    def get_album(self, album_id) -> dict:
        url = f"{EndPoints.GET_ALBUM.value}?app_id=web-desktop-app-v1.0&format=json&album_id={album_id}"
        return self.make_request(url)

    def get_album_tracks(self, album_id, page=1) -> dict:
        url = f"{EndPoints.GET_ALBUM_TRACKS.value}?app_id=web-desktop-app-v1.0&format=json&album_id={album_id}&page_size=100&page={page}"
        return self.make_request(url)

    def get_track_lyrics_translation(self, track_id, selected_language) -> dict:
        url = f"{EndPoints.GET_TRACK_LYRICS_TRANSLATION.value}?app_id=web-desktop-app-v1.0&format=json&track_id={track_id}&selected_language={selected_language}"
        return self.make_request(url)

    def get_track_richsync(
        self,
        commontrack_id: str = None,
        track_id: str = None,
        track_isrc: str = None,
        f_richsync_length: str = None,
        f_richsync_length_max_deviation: str = None,
    ) -> dict:
        """
        Fetch richsync data from Musixmatch with optional filters.

        Args:
            commontrack_id (str): Musixmatch commontrack ID.
            track_id (str): Musixmatch track ID.
            track_isrc (str): ISRC identifier.
            f_richsync_length (str): Desired sync length in seconds.
            f_richsync_length_max_deviation (str): Max allowed deviation from sync length.
        """
        base_url = f"{EndPoints.GET_TRACK_RICHSYNC.value}?app_id=web-desktop-app-v1.0&format=json"

        if commontrack_id:
            base_url += f"&commontrack_id={commontrack_id}"
        if track_id:
            base_url += f"&track_id={track_id}"
        if track_isrc:
            base_url += f"&track_isrc={track_isrc}"
        if f_richsync_length:
            base_url += f"&f_richsync_length={f_richsync_length}"
        if f_richsync_length_max_deviation:
            base_url += (
                f"&f_richsync_length_max_deviation={f_richsync_length_max_deviation}"
            )

        return self.make_request(base_url)

    def make_request(self, url) -> dict:
        url = url.replace("%20", "+").replace(" ", "+")
        url = self.base_url + url
        signed_url = url + self.generate_signature(url)
        response = requests.get(
            signed_url, headers=self.headers, proxies=self.proxies, timeout=5
        )
        return response.json()


if __name__ == "__main__":
    api = MusixMatchAPI()
    search = api.search_tracks("hey jude")
    print(json.dumps(search, indent=4))
