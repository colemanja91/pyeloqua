""" Eloqua.Bulk job setup methods (filters) """

from datetime import datetime
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

GOOD_CONTACT_FIELDS = {
    "items": [
        {
            "name": "Email Address",
            "internalName": "C_EmailAddress",
            "dataType": "emailAddress",
            "hasReadOnlyConstraint": False,
            "hasNotNullConstraint": False,
            "hasUniquenessConstraint": False,
            "statement": "{{Contact.Field(C_EmailAddress)}}",
            "uri": "/contacts/fields/1"
        },
        {
            "name": "First Name",
            "internalName": "C_FirstName",
            "dataType": "text",
            "hasReadOnlyConstraint": False,
            "hasNotNullConstraint": False,
            "hasUniquenessConstraint": False,
            "statement": "{{Contact.Field(C_FirstName)}}",
            "uri": "/contacts/fields/2"
        }
    ],
    "totalResults": 2,
    "limit": 1000,
    "offset": 0,
    "count": 2,
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


@patch('pyeloqua.bulk.requests.get')
def test_filter_date_start(mock_get):
    """ add field filter by stating date """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    bulk.filter_date(field='createdAt', start='2017-01-01 00:00:00')
    assert bulk.job['filters'][
        0] == " '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' "


@patch('pyeloqua.bulk.requests.get')
def test_filter_date_end(mock_get):
    """ add field filter by ending date """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    bulk.filter_date(field='createdAt', end='2017-01-01 00:00:00')
    assert bulk.job['filters'][
        0] == " '{{Contact.CreatedAt}}' <= '2017-01-01 00:00:00' "


@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_filter_date_nofield(mock_get):
    """ exception when bad field passed """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    bulk.filter_date(field='created', start='2017-01-01 00:00:00')


@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_filter_date_badstr_start(mock_get):
    """ exception when bad datetime string passed - start """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    bulk.filter_date(field='created', start='2017-01- 00:00:00')


@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_filter_date_badstr_end(mock_get):
    """ exception when bad datetime string passed - end """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    bulk.filter_date(field='created', end='2017-01- 00:00:00')


@patch('pyeloqua.bulk.requests.get')
def test_filter_datetime_start(mock_get):
    """ add field filter by stating datetime """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    dtime = datetime.strptime('2017-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    bulk.filter_date(field='createdAt', start=dtime)
    assert bulk.job['filters'][
        0] == " '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' "


@patch('pyeloqua.bulk.requests.get')
def test_filter_datetime_end(mock_get):
    """ add field filter by ending datetime """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    dtime = datetime.strptime('2017-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    bulk.filter_date(field='createdAt', end=dtime)
    assert bulk.job['filters'][
        0] == " '{{Contact.CreatedAt}}' <= '2017-01-01 00:00:00' "


@patch('pyeloqua.bulk.requests.get')
def test_filter_datetime_both(mock_get):
    """ add field filter by stating datetime """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    dtime_start = datetime.strptime('2017-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    dtime_end = datetime.strptime('2017-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    bulk.filter_date(field='createdAt', start=dtime_start, end=dtime_end)
    assert bulk.job['filters'][
        0] == " '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' AND '{{Contact.CreatedAt}}' <= '2017-01-01 00:00:00' "


###############################################################################
# Filter field equal to value
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_filter_value_equal(mock_get):
    """ add field filter by value equal """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_CONTACT_FIELDS)
    bulk.filter_equal(field='contactID', value='12345')
    assert bulk.job['filters'][0] == " '{{Contact.Id}}' = '12345' "
