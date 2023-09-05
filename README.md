# MusicXMatch API

Musixmatch is the world's largest catalog of song lyrics and translations. The service is used by millions of people around the world to find lyrics for songs playing around them, to translate lyrics, and to get the facts behind the songs.

# What is this?

This is a Python wrapper for the [Musixmatch API](https://developer.musixmatch.com/). It uses the community API key to make requests to the API. These requests have the the same access as a **[Plus](https://developer.musixmatch.com/plans)** plan but for **free**.

# What can I access?

You can basically query for any lyrics and translation from their API, a more detailed list can be viewed here: [Musixmatch API Documentation](https://developer.musixmatch.com/documentation).

# How do I use it?

First, you need to install the package:

```bash
pip install musicxmatch_api
```

# Examples

Search for artists
```python
    # If you need to make a high volume of requests, consider using proxies
    from musicxmatch_api import MusixMatchAPI
    api = MusixMatchAPI(proxies=proxies)
    search = api.search_artist("adele")
```

Search for songs
```python
    # If you need to make a high volume of requests, consider using proxies
    import json
    from musicxmatch_api import MusixMatchAPI
    api = MusixMatchAPI()
    search = api.search_tracks("skyfall")
    print(json.dumps(search, indent=4))
```

Search for a specific song to get its lyrics
```python
    # If you need to make a high volume of requests, consider using proxies
    from musicxmatch_api import MusixMatchAPI
    track_id = 103149239 # Skyfall by Adele
    api = MusixMatchAPI(proxies=proxies)
    search = api.get_track_lyrics(track_id=track_id)
    # The lyrics are in the "lyrics_body" key
    lyrics = search["message"]["body"]["lyrics"]["lyrics_body"]
```


# Disclaimer

The content provided herein is intended strictly for educational purposes. Any misuse or abuse of this information that contradicts this purpose, including but not limited to the unauthorized distribution, reproduction, or alteration of content, or the use of information for illicit activities, is strictly prohibited and may constitute a violation of applicable laws and regulations. This could lead to serious consequences including legal action. Educational resources are to be used responsibly, ethically, and with integrity. We reserve the right to restrict access to these resources for anyone found violating these terms.