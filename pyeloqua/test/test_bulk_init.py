""" Eloqua.Bulk class initialization """
from pyeloqua import Bulk, Eloqua

###############################################################################
# basic init
###############################################################################

def test_bulk_init():
    """ bulk class initializes """
    assert Bulk(test=True) is not None

def test_bulk_elqinit():
    """ Is an Eloqua instance """
    bulk = Bulk(test=True)
    assert isinstance(bulk, Eloqua)

###############################################################################
# config options
###############################################################################
