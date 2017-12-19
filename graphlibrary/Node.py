class Node(object):
    """ Node object represents either an actor or a movie as a node in a graph """

    def __init__(self, name="", year=None, gross=None, node_type=None):
        """ constructor for node object
            :param name - name associated with node,
            :param year - year associated with node, age for actors and release year for movies
            :param gross - gross box office for movies,
            :param node_type - either "actor" or "movie" """

        self.name = name
        self.year = year
        self.gross = gross
        self.node_type = node_type
        self.edges = []
