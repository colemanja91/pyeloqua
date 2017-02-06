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

def test_bulk_hasjob():
    """ Has job which is instance of BulkDef """
    bulk = Bulk(test=True)
    assert isinstance(bulk.job, dict)

###############################################################################
# BulkDef
###############################################################################

def test_bulkdef_filter():
    """ BulkDef sets up 'filters' """
    bulk = Bulk(test=True)
    assert isinstance(bulk.job['filters'], list)

def test_bulkdef_fields():
    """ BulkDef sets up 'fields' """
    bulk = Bulk(test=True)
    assert isinstance(bulk.job['fields'], list)

def test_bulkdef_type():
    """ BulkDef sets up 'type' """
    bulk = Bulk(test=True)
    assert bulk.job['job_type'] is None

def test_bulkdef_object():
    """ BulkDef sets up 'object' """
    bulk = Bulk(test=True)
    assert bulk.job['elq_object'] is None

def test_bulkdef_options():
    """ BulkDef sets up 'options' """
    bulk = Bulk(test=True)
    assert isinstance(bulk.job['options'], dict)

###############################################################################
# Methods to set up job
###############################################################################
