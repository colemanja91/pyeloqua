""" Eloqua.Bulk job setup methods (filters) """

from copy import deepcopy
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################

GOOD_LIST_ID = {
    "name": "Test List 1",
    "count": 1,
    "statement": "{{ContactList[1]}}",
    "uri": "/contacts/lists/1",
    "createdBy": "testuser",
    "createdAt": "2010-09-29T22:06:02.7430000Z",
    "updatedBy": "testuser",
    "updatedAt": "2013-09-24T13:13:41.4370000Z"
}

###############################################################################
# Filter exists by list, filter, or segment
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_filter_exists_list_id(mock_get):
    """ add exists filter - Shared List """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_ID)
    bulk.filter_exists_list(list_id=1)
    assert bulk.job['filters'][0] == " EXISTS('{{ContactList[1]}}') "

@patch('pyeloqua.bulk.requests.get')
def test_filter_exists_list_id_call(mock_get):
    """ add exists filter - Shared List, api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_ID)
    bulk.filter_exists_list(list_id=1)
    mock_get.assert_called_with(url=bulk.bulk_base + '/contacts/lists/1',
                                auth=bulk.auth)
