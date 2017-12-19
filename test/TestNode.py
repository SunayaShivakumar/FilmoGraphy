import unittest

from graphlibrary.Node import Node


class TestNode(unittest.TestCase):
    """ test class for unit testing the Node class """

    def setUp(self):
        """ sets up a node for testing """

        self.node = Node("x", "y", 1, "actor")

    def tearDown(self):
        """ resets a node after testing """

        self.node = None

    def testInit(self):
        """ unit test for the node constructor """

        self.assertIsNotNone(self)
