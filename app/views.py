from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

from django.http import HttpResponse
import json

from pygooglenews import GoogleNews
import spotipy, json
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="f539ec37ab2d42b28898763eab435a82",
                                                           client_secret="4eeade9ac1ca41c6be5bbafa81086ee9"))


def _get_track(name):
    results = sp.search(q='track:' + name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

# get artist
def _get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


# show music recomendation for track
def show_recommendations_for_track(track, limit):
    results = sp.recommendations(seed_tracks=[track['id']], limit=limit)
    # print("Recomended songs for Track", track['name'])
    resp_dict = {
        'track_name': track['name'],
        'track_uri': track['uri'],
        'recommendations': [],
    }
    for track in results['tracks']:
        temp_dict = {}
        # print(json.dumps(track, indent=3))
        temp_dict['name'] = track['name']
        temp_dict['uri'] = track['uri']
        temp_dict['preview_url'] = track['preview_url']
        temp_dict['cover'] = track['album']['images'][1]
        resp_dict['recommendations'].append(temp_dict)
    return resp_dict



# get artist recomendation songs 
def show_recommendations_for_artist(artist, limit):
    results = sp.recommendations(seed_artists=[artist['id']], limit=limit)
    resp_dict = {
        'artist_name': artist['name'],
        'track_uri': artist['uri'],
        'recommendations': [],
    }
    # print("Recomended songs for artist", artist['name'])
    for track in results['tracks']:
        # print('Recommendation: %s - %s', track['name'],
        #             track['artists'][0]['name'])

        temp_dict = {}
        # print(json.dumps(track, indent=3))
        temp_dict['name'] = track['name']
        temp_dict['uri'] = track['uri']
        temp_dict['preview_url'] = track['preview_url']
        temp_dict['cover'] = track['album']['images'][1]
        resp_dict['recommendations'].append(temp_dict)
    return json(resp_dict, indent=3)

def show_recommendations_for_genre(genreList, limit):
    results = sp.recommendations(seed_genres=genreList, limit=limit)
    print("Recomended songs for Genre", genreList)
    resp_dict = {
        'genre_list':genreList, 
        'recommendations': [],
    }
    for track in results['tracks']:
        temp_dict = {}
        # print(track)
        # print(json.dumps(track, indent=3))
        temp_dict['name'] = track['name']
        temp_dict['uri'] = track['uri']
        temp_dict['preview_url'] = track['preview_url']
        temp_dict['cover'] = track['album']['images'][1]
        resp_dict['recommendations'].append(temp_dict)
    return json.dumps(resp_dict, indent=3)

class NewsParser:
    def __init__(self, lang, country):
        self.lang = lang
        self.country = country

    def _get_gn_object(self):
        gn = GoogleNews(lang = self.lang, country = self.country)
        return gn

    def top_news(self):
        gn = self._get_gn_object()
        top_n = gn.top_news()
        return [entry.title for entry in top_n['entries']]


    def geo_news_headlines(self, city="Dhaka"):
        gn = self._get_gn_object()
        top_geo_news = gn.geo_headlines(city)
        return [entry.title for entry in top_geo_news['entries']]



def index(request):
    lang = request.GET.get('lang', "")
    country = request.GET.get('country', "")

    return JsonResponse({
        'message': 'json',
        'type': 'ScapeGoat'
    })

def get_top_news(request):
    lang = request.GET.get('lang', "")
    country = request.GET.get('country', "")

    np = NewsParser(lang, country)

    _top_news = np.top_news()
    response = JsonResponse({
        'top_news': _top_news 
    })

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def get_geo_top_news(request):
    lang = request.GET.get('lang', "")
    country = request.GET.get('country', "")
    city = request.GET.get('city', "Dhaka")
    np = NewsParser(lang, country)

    _geo_top_news = np.geo_news_headlines(city)
    return JsonResponse({
        'top_news': _geo_top_news 
    })


def get_music_recom_track(request):
    try:
        name = request.GET.get('name', "High Hopes")
        limit = int(request.GET.get('limit', 5))

        track = _get_track(name)
        resp = show_recommendations_for_track(track, limit)
        return JsonResponse(resp)
    except Exception as e:
        print(e)
        return JsonResponse({
            'message': 'Something went wrong'
        })

def get_music_recom_artist(request):
    try:
        name = request.GET.get('name', "Pink Floyd")
        limit = int(request.GET.get('limit', 5))

        artist = _get_artist(name)
        resp = show_recommendations_for_artist(artist, limit)
        return JsonResponse(resp)
    except Exception as e:
        print(e)
        return JsonResponse({
            'message': 'Something went wrong'
        })

def get_music_recom_genre(request):
    try:
        genre = request.GET.get('genre', "alt-rock") 
        limit = int(request.GET.get('limit', 5))
        resp = show_recommendations_for_genre([genre], limit)
        return JsonResponse(resp)
    except Exception as e:
        print(e)
        return JsonResponse({
            'message': 'Something went wrong'
        })



