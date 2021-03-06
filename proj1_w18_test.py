import unittest
import json
import proj1_w18 as proj1

class TestMedia(unittest.TestCase):
    def setUp(self):
        self.test_media = proj1.Media("Bridget Jones's Diary (Unabridged)", "Helen Fielding", 2012)

    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        self.assertEqual(self.test_media.release, 2012)

        # media should not have any instance variables from sub classes
        with self.assertRaises(AttributeError): m1.album
        with self.assertRaises(AttributeError): m1.genre
        with self.assertRaises(AttributeError): m1.track_length
        with self.assertRaises(AttributeError): m1.rating
        with self.assertRaises(AttributeError): m1.movie_length

    def test_string(self):
        self.assertEqual(str(self.test_media), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")

    def test_len(self):
        self.assertEqual(len(self.test_media), 0)

class TestSong(unittest.TestCase):
    def setUp(self):
        self.test_song = proj1.Song(title="Hey Jude", author="The Beatles", album="Hey Jude (Single)", release=1968, genre="Rock", track_length=431)

    def testConstructor(self):
        s1 = proj1.Song()
        s2 = proj1.Song("Physical", "Olivia Newton-John", release=1981, genre="Dance")

        self.assertEqual(s1.title, "No Title")
        self.assertEqual(s1.author, "No Author")
        self.assertEqual(s1.album, "No Album")
        self.assertEqual(s1.release, "No Year")
        self.assertEqual(s1.genre, "No Genre")
        self.assertEqual(s2.title, "Physical")
        self.assertEqual(s2.author, "Olivia Newton-John")
        self.assertEqual(s2.release, 1981)
        self.assertEqual(s2.genre, "Dance")

        # song should not have any attributes from the movie class
        with self.assertRaises(AttributeError): s1.rating
        with self.assertRaises(AttributeError): s1.movie_length

    def test_string(self):
        self.assertEqual(str(self.test_song), "Hey Jude by The Beatles (1968) [Rock]")

    def test_len(self):
        self.assertEqual(len(self.test_song), 431)

class TestMovie(unittest.TestCase):
    def setUp(self):
        self.test_movie1 = proj1.Movie()
        self.test_movie2 = proj1.Movie(title="Jaws", author="Steven Speilberg", release="1975", rating="PG", movie_length=124)

    def testConstructor(self):
        self.assertEqual(self.test_movie1.title, "No Title")
        self.assertEqual(self.test_movie1.author, "No Author")
        self.assertEqual(self.test_movie1.release, "No Year")
        self.assertEqual(self.test_movie1.rating, "No Rating")
        self.assertEqual(self.test_movie1.movie_length, 0)

        self.assertEqual(self.test_movie2.title, "Jaws")
        self.assertEqual(self.test_movie2.author, "Steven Speilberg")
        self.assertEqual(self.test_movie2.release, "1975")
        self.assertEqual(self.test_movie2.rating, "PG")
        self.assertEqual(self.test_movie2.movie_length, 124)

        #movie should not have any attributes from the song class
        with self.assertRaises(AttributeError): self.test_movie2.album
        with self.assertRaises(AttributeError): self.test_movie2.genre
        with self.assertRaises(AttributeError): self.test_movie2.track_length

    def test_string(self):
        self.assertEqual(str(self.test_movie2), "Jaws by Steven Speilberg (1975) [PG]")

    def test_len(self):
        self.assertEqual(self.test_movie2.movie_length, 124)

class TestJSONConstructors(unittest.TestCase):
    def setUp(self):
        with open("sample_json.json", 'r') as file:
            jsonfile = json.load(file)

        for entry in jsonfile:
            if 'kind' in entry:
                if entry["kind"] == "song":
                    self.song_test = proj1.Song(json=entry)
                elif entry["kind"] == "feature-movie":
                    self.movie_test = proj1.Movie(json=entry)
            else:
                self.media_test = proj1.Media(json=entry)

    def test_Constructors(self):
        self.assertEqual(self.media_test.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(self.media_test.author, "Helen Fielding")
        self.assertEqual(self.media_test.release, 2012)

        self.assertEqual(self.song_test.title, "Hey Jude")
        self.assertEqual(self.song_test.author, "The Beatles")
        self.assertEqual(self.song_test.release, 1968)
        self.assertEqual(self.song_test.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(self.song_test.genre, "Rock")

        self.assertEqual(self.movie_test.title, "Jaws")
        self.assertEqual(self.movie_test.author, "Steven Spielberg")
        self.assertEqual(self.movie_test.release, 1975)
        self.assertEqual(self.movie_test.rating, "PG")

    def test_string(self):
        self.assertEqual(str(self.media_test), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
        self.assertEqual(str(self.song_test), "Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(str(self.movie_test), "Jaws by Steven Spielberg (1975) [PG]")

    def test_len(self):
        self.assertEqual(len(self.media_test), 0)
        self.assertEqual(len(self.song_test), 431)
        self.assertEqual(len(self.movie_test), 124)

class TestiTunesAPI(unittest.TestCase):
    def test_commonWords(self):
        self.runQuery("baby")
        self.runQuery("love")

    def test_uncommonWords(self):
        self.runQuery("moana")
        self.runQuery("helter skelter")

    def test_nonsenseQueries(self):
        self.runQuery("&@#!$")

    def test_blankQuery(self):
        self.runQuery("")

    def runQuery(self, query):
        test_object = None
        for result in proj1.getiTunesData(query):
            if 'kind' in result:
                if result["kind"] == "song":
                    test_object = proj1.Song(json=result)
                elif result["kind"] == "feature-movie":
                    test_object = proj1.Movie(json=result)
            else:
                test_object = proj1.Media(json=result)

            # generic tests
            self.assertIsNotNone(test_object.title)
            self.assertIsNotNone(test_object.author)
            self.assertIsNotNone(test_object.release)
            self.assertIsNotNone(test_object.url, "Missing collection URL")

            # tests specific to song objects
            if type(test_object) is proj1.Song:
                self.assertIsNotNone(test_object.album)
                self.assertIsNotNone(test_object.genre)
                self.assertIsNotNone(test_object.track_length)

            # tests specific to movie objects
            if type(test_object) is proj1.Movie:
                self.assertIsNotNone(test_object.rating)
                self.assertIsNotNone(test_object.movie_length)

unittest.main()
