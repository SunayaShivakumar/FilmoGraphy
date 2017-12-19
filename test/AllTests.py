from unittest import TestLoader, TextTestRunner, TestSuite

from test.TestNode import TestNode
from test.TestEdge import TestEdge
from test.TestGraph import TestGraph
from test.TestApi import TestApi

if __name__ == "__main__":
    """ main method to run all the unit tests in the test directory """

    # https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(TestNode),
        loader.loadTestsFromTestCase(TestEdge),
        loader.loadTestsFromTestCase(TestGraph),
        loader.loadTestsFromTestCase(TestApi)
    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
