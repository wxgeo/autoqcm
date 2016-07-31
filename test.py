from importlib import reload

import _tests

def test():
    reload(_tests)
    _tests.test1()

