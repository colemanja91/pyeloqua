""" Eloqua.Bulk class initialization """
from pyeloqua import Bulk, Eloqua

###############################################################################
# basic init
###############################################################################

def test_bulk_init():
    """ bulk class initializes """
    assert Bulk(test=True) is not None

def test_bulk_iselq():
    """ Is an Eloqua instance """
    bulk = Bulk(test=True)
    assert isinstance(bulk, Eloqua)

###############################################################################
# Nested class init
###############################################################################

def test_import_init():
    """ import class initializes """
    bulk = Bulk(test=True)
    assert bulk.Import() is not None
