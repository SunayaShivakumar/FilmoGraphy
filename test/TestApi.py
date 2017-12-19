from webapi import api

import json
import unittest


class TestApi(unittest.TestCase):

    def setUp(self):
        """ sets up app for unit testing """

        api.app.config["Testing"] = True
        self.app = api.app.test_client()

    def testFilterActorsByName(self):
        """ unit tests the filter_actors method for the name attribute """

        response = self.app.get("/actors/name/Bruce")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual("Bruce Willis", result["results"][0]["name"])
        self.assertEqual("Bruce Dern", result["results"][1]["name"])

    def testFilterActorsByAge(self):
        """ unit tests the filter_actors method for the age attribute """

        response = self.app.get("/actors/age/90")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual("Sidney Poitier", result["results"][0]["name"])
        self.assertEqual("Cloris Leachman", result["results"][1]["name"])


    def testFilterMoviesByName(self):
        """ unit tests the filter_movies method for the name attribute """

        response = self.app.get("/movies/name/Bandits")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual("Bandits", result["results"][0]["name"])

    def testFilterMoviesByYear(self):
        """ unit tests the filter_movies method for the year attribute """

        response = self.app.get("/movies/year/2001")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual("Bandits", result["results"][0]["name"])

    def testGetActor(self):
        """ unit tests the get_actor method """

        response = self.app.get("/actors/Bruce Willis")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual("Bruce Willis", result["Bruce Willis"]["name"])

    def testGetMovie(self):
        """ unit tests the get_movie method """

        response = self.app.get("/movies/Bandits")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual("Bandits", result["Bandits"]["name"])

    def testEditActor(self):
        """ unit tests the edit_actor method """

        response = self.app.put("/actors/Bruce Willis", data=json.dumps({"age": 100}), headers={"Content-Type": "application/json"})
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual(100, result["Bruce Willis"]["age"])

    def testEditMovie(self):
        """ unit tests the edit_movie method """

        response = self.app.put("/movies/The Bye Bye Man", data=json.dumps({"box_office": 0}), headers={"Content-Type": "application/json"})
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        self.assertEqual(0, result["The Bye Bye Man"]["box_office"])

    def testAddActor(self):
        """ unit tests the add_actor method """

        response = self.app.post("/actors", data=json.dumps({"name": "Test", "age": 21}), headers={"Content-Type": "application/json"})
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(201, result["_HTTP_"])

    def testAddMovie(self):
        """ unit tests the add_movie method """

        response = self.app.post("/movies", data=json.dumps({"name": "Test", "year": 21}), headers={"Content-Type": "application/json"})
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(201, result["_HTTP_"])

    def testRemoveActor(self):
        """ unit tests the remove_actor method """

        response = self.app.delete("/actors/Bruce Willis")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        response = self.app.get("/actors/Bruce Willis")
        self.assertEqual(400, response.status_code)

    def testRemoveMovie(self):
        """ unit tests the remove_movie method """

        response = self.app.delete("/movies/The Bye Bye Man")
        result = json.loads(response.get_data(as_text=True))

        self.assertEqual(200, result["_HTTP_"])

        response = self.app.get("/movies/The Bye Bye Man")
        self.assertEqual(400, response.status_code)
