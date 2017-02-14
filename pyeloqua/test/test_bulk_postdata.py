""" POST data to a defined endpoint """

from json import dumps
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################

IMPORT_JOB_DEF = {
    "name": "test name",
    "fields": {
        "contactID": "{{Contact.Id}}",
        "createdAt": "{{Contact.CreatedAt}}",
        "updatedAt": "{{Contact.UpdatedAt}}"
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

IMPORT_TEST_DATA = [
    {
        "contactID": "12345",
        "createdAt": "2017-01-01 00:00:00",
        "updatedAt": "2017-01-01 00:00:00"
    }
]

###############################################################################
# testing the things
###############################################################################

@patch('pyeloqua.bulk.requests.post')
def test_post_data_call(mock_post):
    """ post data to an import definition """
    bulk = Bulk(test=True)
    bulk.imports('contacts')
    bulk.job_def = IMPORT_JOB_DEF
    mock_post.return_value = Mock(ok=True, status_code=201)
    bulk.post_data(IMPORT_TEST_DATA)
    mock_post.assert_called_with(url=bulk.bulk_base + '/contacts/imports/1/data',
                                 auth=bulk.auth,
                                 data=dumps(IMPORT_TEST_DATA))
