import unittest

from graphlibrary.Edge import Edge


class TestEdge(unittest.TestCase):
    """ test class for unit testing the Edge class """

    def setUp(self):
        """ sets up an edge for testing """

        self.edge = Edge("x", "y")

    def tearDown(self):
        """ resets an edge after testing """

        self.node = None

    def testInit(self):
        """ unit test for the edge constructor """

        self.assertIsNotNone(self)
