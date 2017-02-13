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


EXPORT_JOB_RESPONSE = {}

###############################################################################
# Create export definition
###############################################################################

@patch('pyeloqua.bulk.requests.post')
def test_create_exports_call(mock_post):
    """ api call for create export """
    bulk = Bulk(test=True)
    bulk.job = JOB_EXPORTS_CONTACTS
    mock_post.return_value = Mock(ok=True, status_code=200)
    mock_post.return_value.json.return_value = deepcopy(EXPORT_JOB_RESPONSE)
    bulk.create_def('test name')
    url = bulk.bulk_base + '/contacts/exports'
    mock_post.assert_called_with(url=url, auth=bulk.auth,
                                 data=dumps(DATA_EXPORTS_CONTACTS))
