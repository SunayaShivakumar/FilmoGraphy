from flask import abort
from flask import Flask
from flask import jsonify
from flask import request

import json
import os.path

app = Flask(__name__)
data_path = os.path.dirname(__file__)
data_file = os.path.join(os.path.abspath(os.path.join(data_path, os.pardir)), "data/data.json")
with open(data_file, 'r') as file:
    data = json.load(file)

actors = []
movies = []

all_actors = data[0]
all_movies = data[1]

for a in all_actors:
    actors.append(a)
for m in all_movies:
    movies.append(m)


""" GET REQUESTS """


@app.route("/actors/<string:attr>/<string:attr_value>", methods=["GET"])
def filter_actors(attr, attr_value):
    """ GET request to search for any value in the actors data set,
        given an existing attribute within said data set """

    result = []
    sample = actors[0]
    if attr in all_actors[sample]:
        for actor in actors:
            if isinstance(all_actors[actor][attr], basestring):
                if attr_value in all_actors[actor][attr]:
                    result.append(all_actors[actor])
            else:
                if attr_value in str(all_actors[actor][attr]):
                    result.append(all_actors[actor])

    if not result:
        abort(400)
    else:
        return jsonify({"_HTTP_": 200, "results": result})


@app.route("/movies/<string:attr>/<string:attr_value>", methods=["GET"])
def filter_movies(attr, attr_value):
    """ GET request to search for any value in the movies data set,
        given an existing attribute within said data set """

    result = []
    sample = movies[0]
    if attr in all_movies[sample]:
        for movie in movies:
            if isinstance(all_movies[movie][attr], basestring):
                if attr_value in all_movies[movie][attr]:
                    result.append(all_movies[movie])
            else:
                if attr_value in str(all_movies[movie][attr]):
                    result.append(all_movies[movie])

    if not result:
        abort(400)
    else:
        return jsonify({"_HTTP_": 200, "results": result})


@app.route("/actors/<string:name>", methods=["GET"])
def get_actor(name):
    """ GET request to search any actor in the actors data set,
        given the name of the actor """

    if name in actors:
        for actor in actors:
            if name == all_actors[actor]["name"]:
                return jsonify({"_HTTP_": 200, name: all_actors[actor]})
    else:
        abort(400)


@app.route("/movies/<string:name>", methods=["GET"])
def get_movie(name):
    """ GET request to search any movie in the movies data set,
        given the name of the movie """

    if name in movies:
        for movie in movies:
            if name == all_movies[movie]["name"]:
                return jsonify({"_HTTP_": 200, name: all_movies[movie]})
    else:
        abort(400)


""" PUT REQUESTS """


@app.route("/actors/<string:name>", methods=["PUT"])
def edit_actor(name):
    """ PUT request to edit any actor attribute in the actors data set,
        given the name of the actor """

    if not request.json:
        abort(400)

    if name in actors:
        for attr in request.json:
            if attr in all_actors[name]:
                all_actors[name][attr] = request.json[attr]
                return jsonify({"_HTTP_": 200, name: all_actors[name]})
            else:
                abort(400)
    else:
        abort(400)


@app.route("/movies/<string:name>", methods=["PUT"])
def edit_movie(name):
    """ PUT request to edit any movie attribute in the movies data set,
        given the name of the movie """

    if not request.json:
        abort(400)

    if name in movies:
        for attr in request.json:
            if attr in all_movies[name]:
                all_movies[name][attr] = request.json[attr]
                return jsonify({"_HTTP_": 200, name: all_movies[name]})
            else:
                abort(400)
    else:
        abort(400)


""" POST REQUESTS """


@app.route("/actors", methods=["POST"])
def add_actor():
    """ POST request to add an actor to the actors data set,
        given the data in a json format """

    if request.json:
        if "name" in request.json:
            key = request.json["name"]
            if key in actors:
                abort(400)

            all_actors[key] = request.json
            actors.append(key)
            return jsonify({"_HTTP_": 201, key: all_actors[key]})
        else:
            abort(400)
    else:
        abort(400)


@app.route("/movies", methods=["POST"])
def add_movie():
    """ POST request to add a movie to the movies data set,
        given the data in a json format """

    if request.json:
        if "name" in request.json:
            key = request.json["name"]
            if key in movies:
                abort(400)

            all_movies[key] = request.json
            movies.append(key)
            return jsonify({"_HTTP_": 201, key: all_movies[key]})
        else:
            abort(400)
    else:
        abort(400)


""" DELETE REQUESTS """


@app.route("/actors/<string:name>", methods=["DELETE"])
def remove_actor(name):
    """ DELETE request to delete an actor to the actors data set,
        given the name of the actor to delete """

    if name in actors:
        del all_actors[name]
        actors.remove(name)
        return jsonify({"_HTTP_": 200, "results": all_actors})
    else:
        abort(400)


@app.route("/movies/<string:name>", methods=["DELETE"])
def remove_movie(name):
    """ DELETE request to delete a movie to the movies data set,
        given the name of the movie to delete """

    if name in movies:
        del all_movies[name]
        movies.remove(name)
        return jsonify({"_HTTP_": 200, "results": all_movies})
    else:
        abort(400)


if __name__ == '__main__':
    app.run(port=8080)
