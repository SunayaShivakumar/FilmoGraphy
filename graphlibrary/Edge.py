class Edge(object):
    """ edge object represents the connection between movies and actors in a graph """

    def __init__(self, actor="", movie=""):
        """ edge constructor for the edge object
            :param actor - the actor node for the edge
            :param movie - the movie node for the edge """

        self.actor = actor
        self.movie = movie
