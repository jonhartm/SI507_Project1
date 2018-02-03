import requests
import json

class Media:
    media_types_trackname = ['song', 'feature-movie', 'music-video', 'podcast', 'tv-episode']
    name = "Media"

    def __init__(self, title="No Title", author="No Author", release="No Year", json=None):
        if json is None:
            self.title = title
            self.author = author
            self.release = release
        else:
            if 'kind' in json and json['kind'] in self.media_types_trackname:
                self.title = json['trackName']
            elif json['wrapperType'] == 'audiobook':
                self.title = json['collectionName']
            else:
                raise Exception("new media type") # TODO: this can't stay here
            self.author = json["artistName"]
            self.release = int(json["releaseDate"][:4])

    def __str__(self):
        return "{} by {} ({})".format(self.title, self.author, self.release)

    def __len__(self):
        return 0

## Other classes, functions, etc. should go here

class Song(Media):
    name = "Song"

    def __init__(self, title="No Title", author="No Author", release="No Year", album="No Album", genre="No Genre", track_length=0, json=None):
        if json is None:
            super().__init__(title, author, release, json=json)
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            super().__init__(json=json)
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = round(int(json["trackTimeMillis"]) / 1000)

    def __str__(self):
        return super().__str__() + " [{}]".format(self.genre)

    def __len__(self):
        return self.track_length

class Movie(Media):
    name = "Movie"

    def __init__(self, title="No Title", author="No Author", release="No Year", rating="No Rating", movie_length=0, json=None):
        if json is None:
            super().__init__(title, author, release)
            self.rating = rating
            self.movie_length = movie_length
        else:
            super().__init__(json=json)
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = round(int(json["trackTimeMillis"])/1000/60)

    def __str__(self):
        return super().__str__() + " [{}]".format(self.rating)

    def __len__(self):
        return self.movie_length

def getiTunesData(search_term, max_results=10):
    baseurl = "https://itunes.apple.com/search"
    dict_params = {}
    dict_params['term'] = search_term
    dict_params['limit'] = max_results
    return requests.get(baseurl, dict_params).json()["results"]

def sortMediaResults(results):
    media_dict = {
        'Media' : [],
        'Songs' : [],
        'Movies' : []
    }
    for result in results:
        if 'kind' in result:
            if result["kind"] == "song":
                media_dict['Songs'].append(Song(json=result))
            elif result["kind"] == "feature-movie":
                media_dict['Movies'].append(Movie(json=result))
        else:
            media_dict['Media'].append(Media(json=result))
    return media_dict['Songs']+media_dict['Movies']+media_dict['Media']

# Determine if a string can be converted to an integer
# params: a string to test
# returns: True if the string can be converted to an integer
# from https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    s = ""
    while s != "exit":
        s = input("Enter a search term or \"exit\" to quit: ")
        results = sortMediaResults(getiTunesData(s, 50))
        # print out the list of results, formatted, and with a counter so the user can select them
        counter = 0
        current_type = None
        for result in results:
            # print the header for each section
            if type(result) != current_type:
                current_type = type(result)
                print("-----{}-----".format(result.name))
            print(str(counter).ljust(2) + " - " + str(result))
            counter += 1
