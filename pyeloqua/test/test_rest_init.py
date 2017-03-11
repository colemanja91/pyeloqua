""" Eloqua.Rest class initialization """
from pyeloqua import Rest, Eloqua

###############################################################################
# basic init
###############################################################################


def test_rest_init():
    """ rest class initializes """
    assert Rest(test=True) is not None


def test_rest_iselq():
    """ Is an Eloqua instance """
    rest = Rest(test=True)
    assert isinstance(rest, Eloqua)
