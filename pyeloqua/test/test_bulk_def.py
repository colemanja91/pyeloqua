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

DATA_EXPORTS_CONTACTS = {
    'name': 'test name',
    'filters': " '{{Contact.Id}}' = '12345' AND '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' ",
    'fields': {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}",
        "isSubscribed": "{{Contact.Email.IsSubscribed}}",
        "isBounced": "{{Contact.Email.IsBounced}}",
        "emailFormat": "{{Contact.Email.Format}}"
    }
}

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

DATA_IMPORTS_CONTACTS = {
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
}

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
                                 data=dumps(DATA_EXPORTS_CONTACTS))


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
                                 data=dumps(DATA_IMPORTS_CONTACTS))


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
