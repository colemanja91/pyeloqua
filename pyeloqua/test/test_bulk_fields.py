""" Eloqua.Bulk job setup methods (fields) """
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Methods to add fields to a job
###############################################################################

@patch('pyeloqua.bulk.requests.get')
def test_get_fields_contacts(mock_get):
    """ find all contact fields """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = {}
    bulk.get_fields()
    url = bulk.bulk_base + '/contacts/fields?limit=1000&offset=0'
    mock_get.assert_any_call(url=url, auth=bulk.auth)
