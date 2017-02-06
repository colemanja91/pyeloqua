""" Eloqua.Bulk job setup methods (imports/exports) """
from nose.tools import raises
from pyeloqua import Bulk

###############################################################################
# Methods to set up job
###############################################################################

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
