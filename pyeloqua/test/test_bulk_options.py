""" Eloqua.Bulk setup methods (add job options) """

from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################

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
# Add some options!
###############################################################################

def test_option_add():
    """ add a random option """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_options(identifierFieldName='C_EmailAddress')
    assert bulk.job['options']['identifierFieldName'] == 'C_EmailAddress'


def test_option_add_all():
    """ add several random options """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_options(identifierFieldName='C_EmailAddress',
                     areSystemTimestampsInUTC=True)
    assert len(bulk.job['options']) == 2

###############################################################################
# Add some sync actions!!
###############################################################################

def test_syncact_add():
    """ add sync action with specified destination and action """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_syncaction(action='add',
                        destination='{{ContactList[12345]}}')
    assert bulk.job['options']['syncActions'][0] == {
        "action": "add",
        "destination": "{{ContactList[12345]}}"
    }

def test_syncact_add_status():
    """ add sync action with specified destination, action and status """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_syncaction(action='add',
                        destination='{{ActionInstance(f82d).Execution[12345]}}',
                        status='complete')
    assert bulk.job['options']['syncActions'][0] == {
        "action": "add",
        "destination": "{{ActionInstance(f82d).Execution[12345]}}",
        "status": "complete"
    }

def test_syncact_listid():
    """ add sync action with specified action and list_id """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_syncaction_list(action='add', list_id=12345)
    assert bulk.job['options']['syncActions'][0] == {
        "action": "add",
        "destination": "{{ContactList[12345]}}"
    }

@patch('pyeloqua.bulk.requests.get')
def test_syncact_listname(mock_get):
    """ add sync action with specified action and list_name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_LIST_NAME
    bulk.add_syncaction_list(action='add', list_name='Test List 1')
    assert bulk.job['options']['syncActions'][0] == {
        "action": "add",
        "destination": "{{ContactList[1]}}"
    }

@patch('pyeloqua.bulk.requests.get')
def test_syncact_listname_call(mock_get):
    """ api call with specified action and list_name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_LIST_NAME
    bulk.add_syncaction_list(action='add', list_name='Test List 1')
    mock_get.assert_called_with(url=bulk.bulk_base + '/contacts/lists?q="name=Test*List*1"',
                                auth=bulk.auth)
