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

    def test_string(self):
        self.assertEqual(str(self.test_song), "Hey Jude by The Beatles (1968) [Rock]")

    def test_len(self):
        self.assertEqual(len(self.test_song), 431)

class TestMovie(unittest.TestCase):
    def setUp(self):
        self.test_movie = proj1.Movie(title="Jaws", author="Steven Speilberg", release="1975", rating="PG", movie_length=124)

    def testConstructor(self):
        self.assertEqual(self.test_movie.rating, "PG")
        self.assertEqual(self.test_movie.movie_length, 124)

    def test_string(self):
        self.assertEqual(str(self.test_movie), "Jaws by Steven Speilberg (1975) [PG]")

    def test_len(self):
        self.assertEqual(self.test_movie.movie_length, 124)

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
        for result in proj1.getiTunesData("baby"):
            self.assertIsInstance(proj1.Media(json=result), proj1.Media)

        for result in proj1.getiTunesData("love"):
            self.assertIsInstance(proj1.Media(json=result), proj1.Media)

    def test_uncommonWords(self):
        for result in proj1.getiTunesData("moana"):
            self.assertIsInstance(proj1.Media(json=result), proj1.Media)

        for result in proj1.getiTunesData("helter skelter"):
            self.assertIsInstance(proj1.Media(json=result), proj1.Media)

    def test_nonsenseQueries(self):
        for result in proj1.getiTunesData("&@#!$"):
            self.assertIsInstance(proj1.Media(json=result), proj1.Media)

unittest.main()
