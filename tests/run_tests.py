
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath("tests"))

def run_all_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_all_tests()
