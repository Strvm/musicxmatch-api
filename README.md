# MusicXMatch API

Musixmatch is the world's largest catalog of song lyrics and translations. The service is used by millions of people around the world to find lyrics for songs playing around them, to translate lyrics, and to get the facts behind the songs.

# What is this?

This is a Python wrapper for the [Musixmatch API](https://developer.musixmatch.com/). It uses the community API key to make requests to the API. These requests have the the same access as a **[Plus](https://developer.musixmatch.com/plans)** plan but for **free**.

# What can I access?

You can basically query for any lyrics and translation from their API, a more detailed list can be viewed here: [Musixmatch API Documentation](https://developer.musixmatch.com/documentation).

# How do I use it?

First, you need to install the package:

```bash
git clone https://github.com/Strvm/MusicXMatchAPI.git 
```

Then, you can import the package and start using it:

```bash
pip install requirements.txt
```

# Examples

Search for artists
```python
    # If you need to make a high volume of requests, consider using proxies
    api = MusixMatchAPI(proxies=proxies)
    search = api.search_artist("eminem")
```

Search for songs
```python
    # If you need to make a high volume of requests, consider using proxies
    api = MusixMatchAPI(proxies=proxies)
    search = api.search_tracks("eminem")
```

Search for a specific song
```python
    # If you need to make a high volume of requests, consider using proxies
    api = MusixMatchAPI(proxies=proxies)
    search = api.get_track(track_id=15445219)
```