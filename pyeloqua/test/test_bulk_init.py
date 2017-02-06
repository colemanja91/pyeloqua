""" Eloqua.Bulk class initialization """
from nose.tools import raises
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

###############################################################################
# Methods to set up job
###############################################################################


def test_reset_job():
    """ reset job params """
    bulk = Bulk(test=True)
    bulk.job['job_type'] = 'imports'
    bulk.reset()
    assert bulk.job == BLANK_JOB


def test_setup_type():
    """ setup set job_type """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'contacts')  # pylint: disable=W0212
    assert bulk.job['job_type'] == 'imports'


def test_setup_object():
    """ setup set object """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'contacts')  # pylint: disable=W0212
    assert bulk.job['elq_object'] == 'contacts'


@raises(Exception)
def test_setup_cdo_id_req():
    """ setup obj_id required for customobjects """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'customobjects')  # pylint: disable=W0212


def test_setup_cdo():
    """ setup sets obj_id """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'customobjects', 1)  # pylint: disable=W0212
    assert bulk.job['obj_id'] == 1


@raises(Exception)
def test_setup_event_id_req():
    """ setup obj_id required for events """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'events')  # pylint: disable=W0212


def test_setup_event():
    """ setup sets obj_id """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'events', 1)  # pylint: disable=W0212
    assert bulk.job['obj_id'] == 1


@raises(Exception)
def test_setup_bad_obj():
    """ setup obj_id required for events """
    bulk = Bulk(test=True)
    bulk._setup_('imports', 'bad')  # pylint: disable=W0212


def test_imports_job_type():
    """ imports() sets job_type """
    bulk = Bulk(test=True)
    bulk.imports('contacts')
    assert bulk.job['job_type'] == 'imports'


def test_exports_job_type():
    """ exports() sets job_type """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    assert bulk.job['job_type'] == 'exports'
