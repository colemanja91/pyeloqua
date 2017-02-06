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
# BulkDef
###############################################################################

def test_bulkdef_init():
    """ BulkDef class initializes """
    bulk = Bulk(test=True)
    assert bulk.BulkDef() is not None

def test_bulkdef_filter():
    """ BulkDef sets up 'filters' """
    bulkdef = Bulk(test=True).BulkDef()
    assert isinstance(bulkdef.filters, list)

def test_bulkdef_fields():
    """ BulkDef sets up 'fields' """
    bulkdef = Bulk(test=True).BulkDef()
    assert isinstance(bulkdef.fields, list)

def test_bulkdef_type():
    """ BulkDef sets up 'type' """
    bulkdef = Bulk(test=True).BulkDef()
    assert bulkdef.type is None

def test_bulkdef_object():
    """ BulkDef sets up 'object' """
    bulkdef = Bulk(test=True).BulkDef()
    assert bulkdef.elq_object is None

def test_bulkdef_options():
    """ BulkDef sets up 'options' """
    bulkdef = Bulk(test=True).BulkDef()
    assert isinstance(bulkdef.options, dict)
