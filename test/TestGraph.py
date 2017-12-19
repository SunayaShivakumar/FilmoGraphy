import os.path
import unittest

from graphlibrary.Graph import Graph


class TestGraph(unittest.TestCase):

    def testMovieGross(self):
        """ unit test for the movie_gross method """

        graph = Graph()

        path = os.path.dirname(__file__)
        m_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/movies.json")
        movies = Graph().read_from_json(m_file)
        movies = movies["Movies"]

        test_movie_gross = graph.movie_gross("American Psycho", movies)

        self.assertEqual(34300000, test_movie_gross)
        self.assertNotEqual(0, test_movie_gross)

    def testMoviesWithActor(self):
        """ unit test for the movies_with_actor method """

        graph = Graph()

        path = os.path.dirname(__file__)
        a_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/actors.json")
        actors = Graph().read_from_json(a_file)
        actors = actors["Actors"]

        test_movies_with_actor = graph.movies_with_actor("Jared Leto", actors)

        self.assertEqual("Blade Runner 2049", test_movies_with_actor[23][0])
        self.assertEqual("Fight Club", test_movies_with_actor[8][0])
        self.assertNotEqual("Fight Club", test_movies_with_actor[0][0])

    def testActorsInMovie(self):
        """ unit test for the actors_in_movie method """

        graph = Graph()

        path = os.path.dirname(__file__)
        m_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/movies.json")
        movies = Graph().read_from_json(m_file)
        movies = movies["Movies"]

        test_actors_in_movie = graph.actors_in_movie("American Psycho", movies)

        self.assertEqual("Christian Bale", test_actors_in_movie[0][0])
        self.assertEqual("Willem Dafoe", test_actors_in_movie[1][0])
        self.assertNotEqual("Reese Witherspoon", test_actors_in_movie[0][0])

    def testActorsGross(self):
        """ unit test for the actors_gross method """

        graph = Graph()

        path = os.path.dirname(__file__)
        m_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/movies.json")
        movies = Graph().read_from_json(m_file)
        movies = movies["Movies"]

        test_actors_gross = graph.actors_gross(5, movies)

        self.assertEqual("Willem Dafoe", test_actors_gross[1][0])
        self.assertNotEqual("Bill Sage", test_actors_gross[1][0])

    def testOldestActors(self):
        """ unit test for the oldest_actors method """

        graph = Graph()

        path = os.path.dirname(__file__)
        a_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/actors.json")
        actors = Graph().read_from_json(a_file)
        actors = actors["Actors"]

        test_oldest_actors = graph.oldest_actors(2, actors)

        self.assertEqual("Willem Dafoe", test_oldest_actors[0][0])
        self.assertEqual("Bill Sage", test_oldest_actors[1][0])

    def testYoungestActors(self):
        """ unit test for the youngest_actors method """

        graph = Graph()

        path = os.path.dirname(__file__)
        a_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/actors.json")
        actors = Graph().read_from_json(a_file)
        actors = actors["Actors"]

        test_youngest_actors = graph.youngest_actors(2, actors)

        self.assertEqual("Cara Seymour", test_youngest_actors[0][0])
        self.assertEqual("Reese Witherspoon", test_youngest_actors[1][0])

    def testMoviesInYear(self):
        """ unit test for the movies_in_year method """

        graph = Graph()

        path = os.path.dirname(__file__)
        m_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/movies.json")
        movies = Graph().read_from_json(m_file)
        movies = movies["Movies"]

        test_movies_in_year = graph.movies_in_year(2000, movies)

        self.assertEqual("American Psycho", test_movies_in_year[0])
        self.assertNotEqual("Good Will Hunting", test_movies_in_year[0])

    def testActorsInYear(self):
        """ unit test for the actors_in_year method """

        graph = Graph()

        path = os.path.dirname(__file__)
        m_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/movies.json")
        movies = Graph().read_from_json(m_file)
        movies = movies["Movies"]

        test_actors_in_year = graph.actors_in_year(2000, movies)

        self.assertEqual("Justin Theroux", test_actors_in_year[9][0])
        self.assertNotEqual("Willem Dafoe", test_actors_in_year[9][0])

    def testListAllActors(self):
        """ unit test for the list_all_actors method """

        graph = Graph()

        path = os.path.dirname(__file__)
        a_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/actors.json")
        actors = Graph().read_from_json(a_file)
        actors = actors["Actors"]
        graph.actors = actors

        all_actors = graph.actors
        self.assertIsNotNone(all_actors)
        self.assertEqual(10, len(all_actors))

    def testListAllMovies(self):
        """ unit test for the list_all_movies method """

        graph = Graph()
        path = os.path.dirname(__file__)
        m_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "test/testdata/movies.json")
        movies = Graph().read_from_json(m_file)
        movies = movies["Movies"]
        graph.movies = movies

        all_movies = graph.movies
        self.assertIsNotNone(all_movies)
        self.assertEqual(1, len(all_movies))

    def testHubActors(self):
        """ unit test for the find_hub_actors method """

        graph = Graph()

        data_path = os.path.dirname(__file__)
        data_file = os.path.join(os.path.abspath(os.path.join(data_path, os.pardir)), "data/testdata.json")
        data = Graph().read_from_json(data_file)
        graph.create_graph(data)

        top_x = 3
        hub_actors = graph.find_hub_actors(top_x)
        self.assertEqual(3, len(hub_actors))
        self.assertEqual(2, hub_actors[0][1])
        self.assertEqual(2, hub_actors[1][1])
        self.assertEqual(2, hub_actors[2][1])

    def testAgeGross(self):
        """ unit test for the analyze_age_gross method """

        graph = Graph()

        data_path = os.path.dirname(__file__)
        data_file = os.path.join(os.path.abspath(os.path.join(data_path, os.pardir)), "data/testdata.json")
        data = Graph().read_from_json(data_file)
        graph.create_graph(data)

        age_gross = graph.analyze_age_gross()

        self.assertEqual(10, len(age_gross))
        self.assertEqual(562709189, age_gross[6][1])
        self.assertEqual(515893034, age_gross[7][1])
        self.assertEqual(6269000, age_gross[8][1])
        self.assertEqual(70, age_gross[6][0])
        self.assertEqual(80, age_gross[7][0])
        self.assertEqual(90, age_gross[8][0])
        self.assertEqual(0, age_gross[0][1])
        self.assertEqual(10, age_gross[0][0])
