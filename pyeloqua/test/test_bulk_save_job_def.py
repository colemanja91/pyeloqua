""" save job def for later re-use """

from mock import patch

from pyeloqua import Bulk, CONTACT_SYSTEM_FIELDS

###############################################################################
# Constants
###############################################################################

JOB_EXPORTS_CONTACTS = {
    'filters': [" '{{Contact.Id}}' = '12345' ",
                " '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' "],
    'fields': CONTACT_SYSTEM_FIELDS,
    'job_type': 'exports',
    'elq_object': 'contacts',
    'obj_id': None,
    'act_type': None,
    'options': {}
}

###############################################################################
# export job defs from pyeloqua
###############################################################################

@patch('pyeloqua.bulk.dump')
def test_writebulkjob(mock_dump):
    """ ensure job def calls json.dump """
    bulk = Bulk(test=True)
    bulk.job = JOB_EXPORTS_CONTACTS
    mock_dump.return_value = None
    bulk.write_job('/tmp/pyeloqua_test_bulk_write.json')
    assert mock_dump.called

###############################################################################
# export job defs from pyeloqua
###############################################################################

def test_readbulkjob():
    """ import correctly sets Bulk.job """
    bulk1 = Bulk(test=True)
    bulk1.job = JOB_EXPORTS_CONTACTS
    bulk1.write_job('/tmp/pyeloqua_test_bulk_write.json')
    bulk2 = Bulk(test=True)
    bulk2.read_job('/tmp/pyeloqua_test_bulk_write.json')
    assert bulk2.job == bulk1.job
