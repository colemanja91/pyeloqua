""" Eloqua.Bulk class initialization """
from pyeloqua import Bulk, Eloqua

###############################################################################
# constants
###############################################################################

BLANK_JOB = {
    'filters': [],
    'fields': [],
    'job_type': None,
    'elq_object': None,
    'obj_id': None,
    'act_type': None,
    'options': {}
}

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


def test_bulkdef_blankjob():
    """ BulkDef sets up 'job' """
    bulk = Bulk(test=True)
    assert bulk.job == BLANK_JOB


def test_reset_job():
    """ reset job params """
    bulk = Bulk(test=True)
    bulk.job['job_type'] = 'imports'
    bulk.reset()
    assert bulk.job == BLANK_JOB
