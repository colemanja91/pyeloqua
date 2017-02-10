""" Eloqua.Bulk job setup methods (fields) """

from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk, ACTIVITY_FIELDS, CONTACT_SYSTEM_FIELDS, ACCOUNT_SYSTEM_FIELDS

###############################################################################
# Constants
###############################################################################

GOOD_FIELDS = {
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
# Method to get all fields
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_cntcts_call(mock_get):
    """ find all contact fields - correct call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    bulk.get_fields()
    url = bulk.bulk_base + '/contacts/fields?limit=1000&offset=0'
    mock_get.assert_any_call(url=url, auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_events_call(mock_get):
    """ find all event fields """
    bulk = Bulk(test=True)
    bulk.exports('events', 1)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    bulk.get_fields()
    url = bulk.bulk_base + '/events/1/fields?limit=1000&offset=0'
    mock_get.assert_any_call(url=url, auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_cntcts_return(mock_get):
    """ find all contact fields - return correct items """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    fields = bulk.get_fields()
    assert fields == GOOD_FIELDS['items']


def test_get_fields_actvty_return():
    """ find all contact fields - return correct items """
    bulk = Bulk(test=True)
    bulk.exports('activities', act_type='EmailOpen')
    fields = bulk.get_fields()
    assert fields == ACTIVITY_FIELDS['EmailOpen']

###############################################################################
# Method to get specified object fields
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_add_fields_db(mock_get):
    """ add contact fields to object by DB/API Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    fields = ['C_EmailAddress', 'C_FirstName']
    bulk.add_fields(fields)
    assert bulk.job['fields'] == GOOD_FIELDS['items']


@patch('pyeloqua.bulk.requests.get')
def test_add_fields_display(mock_get):
    """ add contact fields to object by Display Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    fields = ['Email Address', 'First Name']
    bulk.add_fields(fields)
    assert bulk.job['fields'] == GOOD_FIELDS['items']


@patch('pyeloqua.bulk.requests.get')
def test_add_fields_all(mock_get):
    """ add contact fields to object by Display Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    bulk.add_fields()
    assert bulk.job['fields'] == GOOD_FIELDS['items']


@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_add_fields_notfound(mock_get):
    """ raise exception when field not found """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    fields = ['C_EmailAddress', 'C_FirstName', 'C_LastName']
    bulk.add_fields(fields)


def test_add_fields_actvty_all():
    """ add all activity fields """
    bulk = Bulk(test=True)
    bulk.exports('activities', act_type='EmailOpen')
    bulk.add_fields()
    assert bulk.job['fields'] == ACTIVITY_FIELDS['EmailOpen']


def test_add_fields_actvty():
    """ add some activity fields """
    bulk = Bulk(test=True)
    bulk.exports('activities', act_type='EmailOpen')
    fields = ['ActivityId', 'AssetId']
    bulk.add_fields(fields)
    assert len(bulk.job['fields']) == 2

###############################################################################
# Add system fields
###############################################################################


def test_cntct_system_fields_all():
    """ add all contact system fields """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_system_fields()
    assert bulk.job['fields'] == CONTACT_SYSTEM_FIELDS


def test_accnt_system_fields_all():
    """ add all account system fields """
    bulk = Bulk(test=True)
    bulk.exports('accounts')
    bulk.add_system_fields()
    assert bulk.job['fields'] == ACCOUNT_SYSTEM_FIELDS


def test_cntct_system_fields_set():
    """ add some contact system fields """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_system_fields(['contactID', 'createdAt'])
    assert len(bulk.job['fields']) == 2

def test_accnt_system_fields_set():
    """ add some account system fields """
    bulk = Bulk(test=True)
    bulk.exports('accounts')
    bulk.add_system_fields(['accountID', 'createdAt'])
    assert len(bulk.job['fields']) == 2

###############################################################################
# Add linked contact fields
###############################################################################




###############################################################################
# Add linked account fields
###############################################################################
