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


class MusixMatchAPI:
    def __init__(self, proxies=None):
        self.base_url = "https://www.musixmatch.com/ws/1.1/"
        self.headers = {"User-Agent": USER_AGENT}
        self.proxies = proxies
        self.secret = self.get_secret()

    @cache
    def get_secret(self):
        data = requests.get("https://s.mxmcdn.net/site/js/common-c3a9f29dfd8f6a48a3c7.js", headers=self.headers,
                            proxies=self.proxies, timeout=5)
        regex_pattern = r'.*signatureSecret:"([^"]*)"'
        match = re.search(regex_pattern, data.text, re.DOTALL)
        if match:
            signature_secret = match.group(1)
            return signature_secret
        raise Exception("Couldn't find signature secret")

    def generate_signature(self, url):
        current_date = datetime.utcnow()
        l = str(current_date.year)
        s = str(current_date.month).zfill(2)
        r = str(current_date.day).zfill(2)
        message = (url + l + s + r).encode()
        key = self.secret.encode()
        hash_output = hmac.new(key, message, hashlib.sha1).digest()
        signature = "&signature=" + urllib.parse.quote(
            base64.b64encode(hash_output).decode()) + "&signature_protocol=sha1"
        return signature

    def search_tracks(self, track_query, page=1) -> dict:
        url = f"{EndPoints.SEARCH_TRACK.value}?app_id=community-app-v1.0&format=json&q={urllib.parse.quote(track_query)}&f_has_lyrics=true&page_size=100&page={page}"
        return self.make_request(url)

    def get_track(self, track_id) -> dict:
        url = f"{EndPoints.GET_TRACK.value}?app_id=community-app-v1.0&format=json&track_id={track_id}"
        return self.make_request(url)

    def get_track_lyrics(self, track_id) -> dict:
        url = f"{EndPoints.GET_TRACK_LYRICS.value}?app_id=community-app-v1.0&format=json&track_id={track_id}"
        return self.make_request(url)

    def get_artist_chart(self, country="US", page=1) -> dict:
        url = f"{EndPoints.GET_ARTIST_CHART.value}?app_id=community-app-v1.0&format=json&page_size=100&country={country}&page={page}"
        return self.make_request(url)

    def get_track_chart(self, country="US", page=1) -> dict:
        url = f"{EndPoints.GET_TRACT_CHART.value}?app_id=community-app-v1.0&format=json&page_size=100&country={country}&page={page}"
        return self.make_request(url)

    def search_artist(self, query, page=1) -> dict:
        url = f"{EndPoints.SEARCH_ARTIST.value}?app_id=community-app-v1.0&format=json&q_artist={query}&page_size=100&page={page}"
        return self.make_request(url)

    def get_artist(self, artist_id) -> dict:
        url = f"{EndPoints.GET_ARTIST.value}?app_id=community-app-v1.0&format=json&artist_id={artist_id}"
        return self.make_request(url)

    def get_artist_albums(self, artist_id, page=1) -> dict:
        url = f"{EndPoints.GET_ARTIST_ALBUMS.value}?app_id=community-app-v1.0&format=json&artist_id={artist_id}&page_size=100&page={page}"
        return self.make_request(url)

    def get_album(self, album_id) -> dict:
        url = f"{EndPoints.GET_ALBUM.value}?app_id=community-app-v1.0&format=json&album_id={album_id}"
        return self.make_request(url)

    def get_album_tracks(self, album_id, page=1) -> dict:
        url = f"{EndPoints.GET_ALBUM_TRACKS.value}?app_id=community-app-v1.0&format=json&album_id={album_id}&page_size=100&page={page}"
        return self.make_request(url)

    def get_track_lyrics_translation(self, track_id, selected_language) -> dict:
        url = f"{EndPoints.GET_TRACK_LYRICS_TRANSLATION.value}?app_id=community-app-v1.0&format=json&track_id={track_id}&selected_language={selected_language}"
        return self.make_request(url)

    def make_request(self, url) -> dict:
        url = self.base_url + url
        signed_url = url + self.generate_signature(url)
        response = requests.get(signed_url, headers=self.headers, proxies=self.proxies, timeout=5)
        return response.json()
