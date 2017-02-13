""" Eloqua.Bulk sync functions """

from copy import deepcopy
from json import dumps
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################

EXPORT_JOB_DEF = {
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

SYNC_RESPONSE = {
    "syncedInstanceUri": "/contacts/exports/1",
    "status": "pending",
    "createdAt": "2015-09-25T18:08:32.3485942Z",
    "createdBy": "testuser",
    "uri": "/syncs/1"
}

###############################################################################
# You sync'd my data ship!
###############################################################################


@patch('pyeloqua.bulk.requests.post')
def test_start_sync_export(mock_post):
    """ start syncing an export - api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = deepcopy(SYNC_RESPONSE)
    bulk.start_sync()
    mock_post.assert_called_with(url=bulk.bulk_base + '/syncs',
                                 auth=bulk.auth,
                                 data=dumps(
                                     {
                                         "syncedInstanceUri": "/contacts/exports/1"
                                     }
                                 ))


@patch('pyeloqua.bulk.requests.post')
def test_start_sync_export_add(mock_post):
    """ start syncing an export - add to Bulk """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = deepcopy(SYNC_RESPONSE)
    bulk.start_sync()
    assert bulk.job_sync == SYNC_RESPONSE
