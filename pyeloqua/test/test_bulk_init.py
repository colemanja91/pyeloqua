""" Eloqua.Bulk class initialization """
from pyeloqua import Bulk

###############################################################################
# basic init
###############################################################################

def test_bulk_init():
    """ bulk class initializes """
    assert Bulk(test=True) is not None
