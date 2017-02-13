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

GOOD_LIST_NAME = {
    "items": [
        {
            "name": "Test List 1",
            "count": 1,
            "statement": "{{ContactList[1]}}",
            "uri": "/contacts/lists/1",
            "createdBy": "testuser",
            "createdAt": "2010-09-29T22:06:02.7430000Z",
            "updatedBy": "testuser",
            "updatedAt": "2013-09-24T13:13:41.4370000Z"
        }
    ],
    "totalResults": 1,
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "hasMore": False
}

###############################################################################
# Filter exists by asset
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_asset_exists_list_id(mock_get):
    """ add exists filter - Shared List by ID """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_ID)
    bulk.asset_exists(asset='lists', asset_id=1)
    assert bulk.job['filters'][0] == " EXISTS('{{ContactList[1]}}') "


@patch('pyeloqua.bulk.requests.get')
def test_asset_exists_list_id_call(mock_get):
    """ add exists filter - Shared List by ID, api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_ID)
    bulk.asset_exists(asset='lists', asset_id=1)
    mock_get.assert_called_with(url=bulk.bulk_base + '/contacts/lists/1',
                                auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_asset_exists_list_name(mock_get):
    """ add exists filter - Shared List by Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_NAME)
    bulk.asset_exists(asset='lists', name='Test List 1')
    assert bulk.job['filters'][0] == " EXISTS('{{ContactList[1]}}') "


@patch('pyeloqua.bulk.requests.get')
def test_asset_exists_list_nm_call(mock_get):
    """ add exists filter - Shared List by Name, api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_NAME)
    bulk.asset_exists(asset='lists', name='Test List 1')
    mock_get.assert_called_with(url=bulk.bulk_base + '/contacts/lists?q="name=Test*List*1"',
                                auth=bulk.auth)

@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_asset_exists_list_none(mock_get):
    """ add exists filter - exception on no params """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_LIST_NAME)
    bulk.asset_exists(asset='lists')


###############################################################################
# Filter field by date range
###############################################################################

@raises(Exception)
def test_filter_date_start(mock_get):
    """ add field filter by stating date """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD)
    bulk.filter_date(field='createdAt', start='2017-01-01 00:00:00')
    assert bulk.job['filters'][0] == " '{{Contact.Field(CreatedAt)}}' >= '2017-01-01 00:00:00' "
