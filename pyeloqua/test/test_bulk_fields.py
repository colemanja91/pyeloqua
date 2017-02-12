""" Eloqua.Bulk job setup methods (fields) """

from copy import deepcopy
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

GOOD_FIELDS_ACCOUNT = {
    "items": [
        {
            "name": "Company Name",
            "internalName": "M_CompanyName",
            "dataType": "string",
            "hasReadOnlyConstraint": False,
            "hasNotNullConstraint": True,
            "hasUniquenessConstraint": False,
            "statement": "{{Account.Field(M_CompanyName)}}",
            "uri": "/accounts/fields/100085",
            "createdAt": "1900-01-01T05:00:00.0000000Z",
            "updatedBy": "Greg.Manetti",
            "updatedAt": "2012-10-30T17:59:21.7000000Z"
        },
        {
            "name": "Country",
            "internalName": "M_Country",
            "dataType": "string",
            "hasReadOnlyConstraint": False,
            "hasNotNullConstraint": False,
            "hasUniquenessConstraint": False,
            "statement": "{{Account.Field(M_Country)}}",
            "uri": "/accounts/fields/100088",
            "createdAt": "1900-01-01T05:00:00.0000000Z",
            "updatedAt": "1900-01-01T05:00:00.0000000Z"
        }
    ],
    "totalResults": 2,
    "limit": 1000,
    "offset": 0,
    "count": 2,
    "hasMore": False
}

LINKED_ACCOUNT_FIELDS = [
    {
        "name": "Company Name",
        "internalName": "M_CompanyName",
        "dataType": "string",
        "hasReadOnlyConstraint": False,
        "hasNotNullConstraint": True,
        "hasUniquenessConstraint": False,
        "statement": "{{Contact.Account.Field(M_CompanyName)}}",
        "uri": "/accounts/fields/100085",
        "createdAt": "1900-01-01T05:00:00.0000000Z",
        "updatedBy": "Greg.Manetti",
        "updatedAt": "2012-10-30T17:59:21.7000000Z"
    },
    {
        "name": "Country",
        "internalName": "M_Country",
        "dataType": "string",
        "hasReadOnlyConstraint": False,
        "hasNotNullConstraint": False,
        "hasUniquenessConstraint": False,
        "statement": "{{Contact.Account.Field(M_Country)}}",
        "uri": "/accounts/fields/100088",
        "createdAt": "1900-01-01T05:00:00.0000000Z",
        "updatedAt": "1900-01-01T05:00:00.0000000Z"
    }
]

LINKED_CDO_CONTACT_FIELDS = [
    {
        "name": "Email Address",
        "internalName": "C_EmailAddress",
        "dataType": "emailAddress",
        "hasReadOnlyConstraint": False,
        "hasNotNullConstraint": False,
        "hasUniquenessConstraint": False,
        "statement": "{{CustomObject[1].Contact.Field(C_EmailAddress)}}",
        "uri": "/contacts/fields/1"
    },
    {
        "name": "First Name",
        "internalName": "C_FirstName",
        "dataType": "text",
        "hasReadOnlyConstraint": False,
        "hasNotNullConstraint": False,
        "hasUniquenessConstraint": False,
        "statement": "{{CustomObject[1].Contact.Field(C_FirstName)}}",
        "uri": "/contacts/fields/2"
    }
]

LINKED_EVENT_CONTACT_FIELDS = [
    {
        "name": "Email Address",
        "internalName": "C_EmailAddress",
        "dataType": "emailAddress",
        "hasReadOnlyConstraint": False,
        "hasNotNullConstraint": False,
        "hasUniquenessConstraint": False,
        "statement": "{{Event[1].Contact.Field(C_EmailAddress)}}",
        "uri": "/contacts/fields/1"
    },
    {
        "name": "First Name",
        "internalName": "C_FirstName",
        "dataType": "text",
        "hasReadOnlyConstraint": False,
        "hasNotNullConstraint": False,
        "hasUniquenessConstraint": False,
        "statement": "{{Event[1].Contact.Field(C_FirstName)}}",
        "uri": "/contacts/fields/2"
    }
]

LEADSCORE_MODEL_NAME = {
    "items": [
        {
            "name": "Model1",
            "status": "Active",
            "id": 1,
            "fields": [
                {
                    "name": "Rating",
                    "statement": "{{Contact.LeadScore.Model[1].Rating}}",
                    "dataType": "string"
                },
                {
                    "name": "ProfileScore",
                    "statement": "{{Contact.LeadScore.Model[1].ProfileScore}}",
                    "dataType": "number"
                },
                {
                    "name": "EngagementScore",
                    "statement": "{{Contact.LeadScore.Model[1].EngagementScore}}",
                    "dataType": "number"
                }
            ],
            "uri": "/contacts/scoring/models/1",
            "createdBy": "testuser",
            "updatedBy": "testuser",
            "createdAt": "2015-07-15T20:04:45.1600000Z",
            "updatedAt": "2015-09-16T05:09:09.3570000Z"
        }
    ],
    "totalResults": 1,
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "hasMore": False
}

LEADSCORE_MODEL_ID = {
    "name": "Model1",
    "status": "Active",
    "id": 1,
    "fields": [
        {
            "name": "Rating",
            "statement": "{{Contact.LeadScore.Model[1].Rating}}",
            "dataType": "string"
        },
        {
            "name": "ProfileScore",
            "statement": "{{Contact.LeadScore.Model[1].ProfileScore}}",
            "dataType": "number"
        },
        {
            "name": "EngagementScore",
            "statement": "{{Contact.LeadScore.Model[1].EngagementScore}}",
            "dataType": "number"
        }
    ],
    "uri": "/contacts/scoring/models/1",
    "createdBy": "testuser",
    "updatedBy": "testuser",
    "createdAt": "2015-07-15T20:04:45.1600000Z",
    "updatedAt": "2015-09-16T05:09:09.3570000Z"
}

LEADSCORE_MODEL_FIELDS = [
    {
        "name": "Rating",
        "statement": "{{Contact.LeadScore.Model[1].Rating}}",
        "dataType": "string"
    },
    {
        "name": "ProfileScore",
        "statement": "{{Contact.LeadScore.Model[1].ProfileScore}}",
        "dataType": "number"
    },
    {
        "name": "EngagementScore",
        "statement": "{{Contact.LeadScore.Model[1].EngagementScore}}",
        "dataType": "number"
    }
]

###############################################################################
# Method to get all fields
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_cntcts_call(mock_get):
    """ find all contact fields - correct call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    bulk.get_fields()
    url = bulk.bulk_base + '/contacts/fields?limit=1000&offset=0'
    mock_get.assert_any_call(url=url, auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_events_call(mock_get):
    """ find all event fields """
    bulk = Bulk(test=True)
    bulk.exports('events', 1)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    bulk.get_fields()
    url = bulk.bulk_base + '/events/1/fields?limit=1000&offset=0'
    mock_get.assert_any_call(url=url, auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_cntcts_return(mock_get):
    """ find all contact fields - return correct items """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    fields = bulk.get_fields()
    assert fields == GOOD_FIELDS['items']


def test_get_fields_actvty_return():
    """ find all contact fields - return correct items """
    bulk = Bulk(test=True)
    bulk.exports('activities', act_type='EmailOpen')
    fields = bulk.get_fields()
    assert fields == ACTIVITY_FIELDS['EmailOpen']


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_specify(mock_get):
    """ specify elq_object to return fields for """
    bulk = Bulk(test=True)
    bulk.exports('accounts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    fields = bulk.get_fields(elq_object='contacts')
    assert fields == GOOD_FIELDS['items']

###############################################################################
# Method to get specified object fields
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_add_fields_db(mock_get):
    """ add contact fields to object by DB/API Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    fields = ['C_EmailAddress', 'C_FirstName']
    bulk.add_fields(fields)
    assert bulk.job['fields'] == GOOD_FIELDS['items']


@patch('pyeloqua.bulk.requests.get')
def test_add_fields_display(mock_get):
    """ add contact fields to object by Display Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    fields = ['Email Address', 'First Name']
    bulk.add_fields(fields)
    assert bulk.job['fields'] == GOOD_FIELDS['items']


@patch('pyeloqua.bulk.requests.get')
def test_add_fields_all(mock_get):
    """ add contact fields to object by Display Name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    bulk.add_fields()
    assert bulk.job['fields'] == GOOD_FIELDS['items']


@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_add_fields_notfound(mock_get):
    """ raise exception when field not found """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
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
# Add linked record fields
# CDO -> Contact
# Contact -> Account
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_cntct_lnk_acct_fields(mock_get):
    """ add some linked account fields """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS_ACCOUNT)
    bulk.add_linked_fields('accounts', ['M_CompanyName', 'M_Country'])
    assert bulk.job['fields'] == LINKED_ACCOUNT_FIELDS


@patch('pyeloqua.bulk.requests.get')
def test_cdo_lnk_cntct_fields(mock_get):
    """ add some linked contact fields to cdo """
    bulk = Bulk(test=True)
    bulk.exports('customobjects', 1)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    bulk.add_linked_fields('contacts', ['C_EmailAddress', 'C_FirstName'])
    assert bulk.job['fields'] == LINKED_CDO_CONTACT_FIELDS


@patch('pyeloqua.bulk.requests.get')
def test_event_lnk_cntct_fields(mock_get):
    """ add some linked contact fields to event """
    bulk = Bulk(test=True)
    bulk.exports('events', 1)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(GOOD_FIELDS)
    bulk.add_linked_fields('contacts', ['C_EmailAddress', 'C_FirstName'])
    assert bulk.job['fields'] == LINKED_EVENT_CONTACT_FIELDS

###############################################################################
# Lead Score Model fields
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_leadscore_fields_id(mock_get):
    """ add fields from a lead score model by model id """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(LEADSCORE_MODEL_ID)
    bulk.add_leadscore_fields(model_id=1)
    assert bulk.job['fields'] == LEADSCORE_MODEL_FIELDS

@patch('pyeloqua.bulk.requests.get')
def test_leadscore_fields_name(mock_get):
    """ add fields from a lead score model by model name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(LEADSCORE_MODEL_NAME)
    bulk.add_leadscore_fields(name='Model1')
    assert bulk.job['fields'] == LEADSCORE_MODEL_FIELDS

@patch('pyeloqua.bulk.requests.get')
@raises(Exception)
def test_leadscore_fields_noparams(mock_get):
    """ add fields from a lead score model by model name """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(LEADSCORE_MODEL_NAME)
    bulk.add_leadscore_fields()
