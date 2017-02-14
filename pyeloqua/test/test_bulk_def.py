""" Eloqua.Bulk job setup methods (create definition) """

from copy import deepcopy
from json import dumps
from nose.tools import raises
from mock import patch, Mock

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

DATA_EXPORTS_CONTACTS = dumps({
    'name': 'test name',
    'fields': {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    },
    'filters': " '{{Contact.Id}}' = '12345' AND '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' "
}, ensure_ascii=False).encode('utf8')

JOB_IMPORTS_CONTACTS = {
    'filters': [],
    'fields': CONTACT_SYSTEM_FIELDS,
    'job_type': 'imports',
    'elq_object': 'contacts',
    'obj_id': None,
    'act_type': None,
    'options': {
        'identifierFieldName': 'contactID'
    }
}

JOB_IMPORTS_CONTACTS_BAD = {
    'filters': [],
    'fields': CONTACT_SYSTEM_FIELDS,
    'job_type': 'imports',
    'elq_object': 'contacts',
    'obj_id': None,
    'act_type': None,
    'options': {}
}

DATA_IMPORTS_CONTACTS = dumps({
    'name': 'test name',
    'fields': {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    },
    'identifierFieldName': 'contactID'
}, ensure_ascii=False).encode('utf8')

EXPORT_JOB_RESPONSE = {
    "name": "test name",
    "fields": {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    },
    "dataRetentionDuration": "PT12H",
    "uri": "/contacts/exports/1",
    "createdBy": "testuser",
    "createdAt": "2017-02-13T16:32:31.7020994Z",
    "updatedBy": "testuser",
    "updatedAt": "2017-02-13T16:32:31.7020994Z"
}

IMPORT_JOB_RESPONSE = {
    "name": "test name",
    "fields": {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    },
    "identifierFieldName": "contactID",
    "isSyncTriggeredOnImport": False,
    "dataRetentionDuration": "P7D",
    "isUpdatingMultipleMatchedRecords": False,
    "uri": "/contacts/imports/1",
    "createdBy": "testuser",
    "createdAt": "2017-02-13T16:38:13.3442894Z",
    "updatedBy": "testuser",
    "updatedAt": "2017-02-13T16:38:13.3442894Z"
}

IMPORT_JOB_RESPONSE_BAD = {
    "failures": [
        {
            "field": "identifierFieldName",
            "constraint":
            "Must be a string value, at least 1 character and at most 100 characters long."
        }
    ]
}

###############################################################################
# Create export definition
###############################################################################


@patch('pyeloqua.bulk.requests.post')
def test_create_exports_call(mock_post):
    """ api call for create export """
    bulk = Bulk(test=True)
    bulk.job = JOB_EXPORTS_CONTACTS
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = deepcopy(EXPORT_JOB_RESPONSE)
    bulk.create_def('test name')
    url = bulk.bulk_base + '/contacts/exports'
    mock_post.assert_called_with(url=url, auth=bulk.auth,
                                 data=DATA_EXPORTS_CONTACTS)


@patch('pyeloqua.bulk.requests.post')
def test_create_imports_call(mock_post):
    """ api call for create import """
    bulk = Bulk(test=True)
    bulk.job = JOB_IMPORTS_CONTACTS
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = deepcopy(IMPORT_JOB_RESPONSE)
    bulk.create_def('test name')
    url = bulk.bulk_base + '/contacts/imports'
    mock_post.assert_called_with(url=url, auth=bulk.auth,
                                 data=DATA_IMPORTS_CONTACTS)


@patch('pyeloqua.bulk.requests.post')
def test_create_exports_setdef(mock_post):
    """ set job_def for create export """
    bulk = Bulk(test=True)
    bulk.job = JOB_EXPORTS_CONTACTS
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = deepcopy(EXPORT_JOB_RESPONSE)
    bulk.create_def('test name')
    assert bulk.job_def == EXPORT_JOB_RESPONSE


@patch('pyeloqua.bulk.requests.post')
def test_create_imports_setdef(mock_post):
    """ set job_def for create import """
    bulk = Bulk(test=True)
    bulk.job = JOB_IMPORTS_CONTACTS
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = deepcopy(IMPORT_JOB_RESPONSE)
    bulk.create_def('test name')
    assert bulk.job_def == IMPORT_JOB_RESPONSE


@patch('pyeloqua.bulk.requests.post')
@raises(Exception)
def test_create_imports_error(mock_post):
    """ raise exception on bad import def """
    bulk = Bulk(test=True)
    bulk.job = JOB_IMPORTS_CONTACTS_BAD
    mock_post.return_value = Mock(ok=True, status_code=400)
    mock_post.return_value.json.return_value = deepcopy(
        IMPORT_JOB_RESPONSE_BAD)
    bulk.create_def('test name')
