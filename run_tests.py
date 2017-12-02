import unittest

"""
This code ran every test case present inside ./murpy/tests/ and named test*.py
"""

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = './murpy/tests/'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
