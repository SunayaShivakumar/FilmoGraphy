from graphlibrary import Node
from graphlibrary import Edge

import matplotlib.pylab as plt
import numpy as np

import json
import operator
import os.path


class Graph(object):
    """ Graph object represents graph where the nodes are actors or movies """

    def __init__(self):
        """ a graph constructor that keeps track of all actors and movies
            and edges between them in a graph object """

        self.actors = []
        self.movies = []
        self.edges = []

    def add_node(self, name, year, gross, node_type):
        """ method to make a new node to add to a graph
            :param name - the name associated with the node object
            :param year - the year associated with the node object
            :param gross - the gross amount for a movie node
            :param node_type - the type of the node, either "actor" or "movie" """

        new_node = Node.Node(name, year, gross, node_type)
        if new_node.node_type == "actor" and new_node not in self.actors:
            self.actors.append(new_node)
        if new_node.node_type == "movie" and new_node not in self.movies:
            self.movies.append(new_node)
        return new_node

    def add_edge(self, actor, movie):
        """ method to make a new edge between two nodes,
            which would be an actor and a movie
            :param actor - the actor node for an edge
            :param movie - the movie node for an edge """

        new_edge = Edge.Edge(actor, movie)
        if new_edge not in self.edges:
            self.edges.append(new_edge)

            if new_edge not in actor.edges:
                actor.edges.append(new_edge)

            if new_edge not in movie.edges:
                movie.edges.append(new_edge)

    def make_graph(self, actors, movies):
        """ makes a graph given the actors and movies data.
            the make_graph method acts as helper for the constructor """

        for a in actors:
            new_actor = self.add_node(a["name"], a["age"], None, a["json_class"])
            self.actors.append(new_actor)
            for m in a["movies"]:
                for movie in movies:
                    if m[0] == movie["name"]:
                        new_movie = self.add_node(movie["name"], movie["year"], movie["gross"], movie["json_class"])
                        self.movies.append(new_movie)
                        self.edges.append(self.add_edge(new_actor, new_movie))

        for m in movies:
            new_movie = self.add_node(m["name"], m["year"], m["gross"], m["json_class"])
            self.movies.append(new_movie)
            for a in m["actors"]:
                for actor in actors:
                    if a[0] == actor["name"]:
                        new_actor = self.add_node(actor["name"], actor["age"], None, actor["json_class"])
                        self.actors.append(new_actor)
                        self.edges.append(self.add_edge(new_actor, new_movie))

    def create_graph(self, data):
        self.actors = data[0]
        self.movies = data[1]

    @staticmethod
    def movie_gross(movie_name, movie_data):
        """ method to retrieve the amount grossed by a given movie
            :param movie_name - the name of the movie to look for
            :param movie_data - the data through which to look for """

        for movie in movie_data:
            if movie["name"] == movie_name:
                return movie["gross"]
            else:
                return None

    @staticmethod
    def movies_with_actor(actor_name, actor_data):
        """ method to retrieve the list of movies that a given actor has been part of
            :param actor_name - the name of the actor to look for
            :param actor_data - the data through which to look for """

        movies = []
        for actor in actor_data:
            if actor["name"] == actor_name:
                movies.append(actor["movies"])
        movies = movies[0]
        return movies

    @staticmethod
    def actors_in_movie(movie_name, movie_data):
        """ method to retrieve the list of actors starring in a given movie
            :param movie_name - the name of the movie to look for
            :param movie_data - the data through which to look for """

        actors = []
        for movie in movie_data:
            if movie["name"] == movie_name:
                actors = movie["cast"]
        return actors

    @staticmethod
    def actors_gross(x, movie_data):
        """ method to retrieve the top x actors with the total most grossing value.
            here it is calculated by taking the first x actors after sorting the
            movies based on grossing value.
            :param x - the number of top actors to return
            :param movie_data - the data through which to look for """

        movie_gross = []
        actors = []
        for movie in movie_data:
            cast_list = movie["cast"]
            cast_names = cast_list
            movie_gross.append([movie["gross"], cast_names])
        movie_gross.sort(key=lambda a: a[0], reverse=True)

        for g in movie_gross:
            for a in range(x):
                actors.append(g[1][a])
        return actors

    @staticmethod
    def oldest_actors(x, actor_data):
        """ method to retrieve the top x oldest actors.
            :param x - the number of top actors to return
            :param actor_data - the data through which to look for """

        actors_ages = []
        for actor in actor_data:
            actors_ages.append([actor["name"], actor["age"]])
        actors_ages.sort(key=lambda a: a[1], reverse=True)
        return actors_ages[:x]

    @staticmethod
    def youngest_actors(x, actor_data):
        """ method to retrieve the top x youngest actors.
            :param x - the number of top actors to return
            :param actor_data - the data through which to look for """

        actors_ages = []
        for actor in actor_data:
            actors_ages.append([actor["name"], actor["age"]])
        actors_ages.sort(key=lambda a: a[1])
        return actors_ages[:x]

    @staticmethod
    def movies_in_year(year, movie_data):
        """ method to retrieve the list of movies release in a given year
            :param year - the year to look for
            :param movie_data - the data through which to look for """

        movies = []
        for movie in movie_data:
            if movie["year"] == year:
                movies.append(movie["name"])
        return movies

    @staticmethod
    def actors_in_year(year, movie_data):
        """ method to retrieve the list of actors who were in a movie released
            in a given year
            :param year - the year to look for
            :param movie_data - the data through which to look for """

        actors = []
        for movie in movie_data:
            if movie["year"] == year:
                cast = movie["cast"]
                actors.append(cast)
        return actors[0]

    def find_hub_actors(self, x):
        """ method to get the top x number of hub actors or actors with the
             most connections with other actors. There is a connection between two
             actors if they have starred in a same movie.
             :param x - the number of top x hub actors to find """

        actors_names = []
        actors_weights = {}
        for a in self.actors:
            actors_names.append(a)

        for a in actors_names:
            connect = 0
            for b in actors_names:
                if str(a) == str(b):
                    continue

                a_movies = self.actors[a]["movies"]
                b_movies = self.actors[b]["movies"]

                if len(a_movies) < len(b_movies):
                    for a_m in a_movies:
                        if a_m in b_movies:
                            connect += 1
                            break
                else:
                    for b_m in b_movies:
                        if b_m in a_movies:
                            connect += 1
                            break

            actors_weights[a] = connect
        result = sorted(actors_weights.items(), key=operator.itemgetter(1), reverse=True)

        return result[0:x]

    def analyze_age_gross(self):
        """ method that calculates the number of actors, and total gross for an age group,
         and normalizes the values to get the average gross for an age group """

        actors_names = []
        actors_ages = {10: [0, 0],
                       20: [0, 0],
                       30: [0, 0],
                       40: [0, 0],
                       50: [0, 0],
                       60: [0, 0],
                       70: [0, 0],
                       80: [0, 0],
                       90: [0, 0],
                       100: [0, 0]}
        actors_ages_normal = {}
        for a in self.actors:
            actors_names.append(a)

        for a in actors_names:
            a_age = self.actors[a]["age"]
            a_gross = self.actors[a]["total_gross"]

            if (a_age >= 0) and (a_age < 11):
                actors_ages[10][0] += 1
                actors_ages[10][1] += a_gross
            if (a_age >= 11) and (a_age < 21):
                actors_ages[20][0] += 1
                actors_ages[20][1] += a_gross
            if (a_age >= 21) and (a_age < 31):
                actors_ages[30][0] += 1
                actors_ages[30][1] += a_gross
            if (a_age >= 31) and (a_age < 41):
                actors_ages[40][0] += 1
                actors_ages[40][1] += a_gross
            if (a_age >= 41) and (a_age < 51):
                actors_ages[50][0] += 1
                actors_ages[50][1] += a_gross
            if (a_age >= 51) and (a_age < 61):
                actors_ages[60][0] += 1
                actors_ages[60][1] += a_gross
            if (a_age >= 61) and (a_age < 71):
                actors_ages[70][0] += 1
                actors_ages[70][1] += a_gross
            if (a_age >= 71) and (a_age < 81):
                actors_ages[80][0] += 1
                actors_ages[80][1] += a_gross
            if (a_age >= 81) and (a_age < 91):
                actors_ages[90][0] += 1
                actors_ages[90][1] += a_gross
            if (a_age >= 91) and (a_age < 100):
                actors_ages[100][0] += 1
                actors_ages[100][1] += a_gross

        for k in actors_ages:
            if actors_ages[k][0] == 0:
                actors_ages_normal[k] = 0
            else:
                actors_ages_normal[k] = actors_ages[k][1]/actors_ages[k][0]

        result = sorted(actors_ages_normal.items(), key=operator.itemgetter(0))
        return result

    def list_all_actors(self):
        """ method to that list all actor nodes """

        return self.actors

    def list_all_films(self):
        """ method to that list all movie nodes """

        return self.movies

    def list_all_edges(self):
        """ method to that list all the edges """

        return self.edges

    @staticmethod
    def write_to_json(data, filename):
        """ write_to_json converts raw data to json file format
            :param data - the data to be stored as json
            :param filename - the filename for the output json """

        with open(filename + '.json', 'w') as fpA:
            json.dump(data, fpA, sort_keys=True, indent=2)

    @staticmethod
    def read_from_json(filename):
        """ read_from_json converts a json file format into raw data
            :param filename - the filename for the output data """

        with open(filename, 'r') as file:
            return json.load(file)


if __name__ == '__main__':
    graph = Graph()

    data_path = os.path.dirname(__file__)
    data_file = os.path.join(os.path.abspath(os.path.join(data_path, os.pardir)), "data/data.json")
    data = Graph().read_from_json(data_file)
    graph.create_graph(data)

    # hub actors
    top_x = 20
    hub_actors = graph.find_hub_actors(top_x)
    print hub_actors

    # age gross
    age_gross = graph.analyze_age_gross()
    print age_gross

    # plot hub actors
    x = list(range(top_x))
    x = np.array(x)
    y = [a[1] for a in hub_actors]

    x_labels = [str(a[0]) for a in hub_actors]
    fig, ax = plt.subplots()
    plt.xticks(x, x_labels)
    plt.plot(x, y, color="b", marker="o")
    ax.xaxis_date()
    fig.autofmt_xdate()

    # plot age gross
    x = list(range(len(age_gross)))
    x = np.array(x)
    y = [a[1] for a in age_gross]

    x_labels = [a[0] for a in age_gross]
    fig, ax = plt.subplots()
    plt.xticks(x, x_labels)
    plt.plot(x, y, color="b", marker="o")
    ax.xaxis_date()
    fig.autofmt_xdate()
    plt.show()
