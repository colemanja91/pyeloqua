""" Eloqua.Bulk sync functions """

from copy import deepcopy
from json import dumps
from nose.tools import raises
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

IMPORT_JOB_DEF = {
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

SYNC_RESPONSE = {
    "syncedInstanceUri": "/contacts/exports/1",
    "status": "pending",
    "createdAt": "2015-09-25T18:08:32.3485942Z",
    "createdBy": "testuser",
    "uri": "/syncs/1"
}

SYNC_RESPONSE_ACTIVE = {
    "syncStartedAt": "2013-07-22T22:17:59.6730000Z",
    "status": "active",
    "createdAt": "2015-09-25T18:08:32.3485942Z",
    "createdBy": "testuser",
    "uri": "/syncs/1"
}

SYNC_RESPONSE_SUCCESS = {
    "syncStartedAt": "2013-07-22T22:17:59.6730000Z",
    "syncEndedAt": "2013-07-22T22:18:07.6430000Z",
    "status": "success",
    "createdAt": "2015-09-25T18:08:32.3485942Z",
    "createdBy": "testuser",
    "uri": "/syncs/1"
}


SYNC_RESPONSE_WARNING = {
    "syncStartedAt": "2013-07-22T22:17:59.6730000Z",
    "syncEndedAt": "2013-07-22T22:18:07.6430000Z",
    "status": "warning",
    "createdAt": "2015-09-25T18:08:32.3485942Z",
    "createdBy": "testuser",
    "uri": "/syncs/1"
}

SYNC_RESPONSE_ERROR = {
    "syncStartedAt": "2013-07-22T22:17:59.6730000Z",
    "syncEndedAt": "2013-07-22T22:18:07.6430000Z",
    "status": "error",
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
    mock_post.return_value = Mock(ok=True, status_code=200)
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
    mock_post.return_value = Mock(ok=True, status_code=200)
    mock_post.return_value.json.return_value = deepcopy(SYNC_RESPONSE)
    bulk.start_sync()
    assert bulk.job_sync == SYNC_RESPONSE


@patch('pyeloqua.bulk.requests.post')
@raises(Exception)
def test_start_sync_export_nodef(mock_post):
    """ except when no job_def """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_post.return_value = Mock(ok=True, status_code=200)
    mock_post.return_value.json.return_value = deepcopy(SYNC_RESPONSE)
    bulk.start_sync()


###############################################################################
# check on the status of those syncs
###############################################################################

@patch('pyeloqua.bulk.requests.get')
def test_check_sync_call(mock_get):
    """ check on status of 'active' sync - api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_ACTIVE
    bulk.check_sync()
    mock_get.assert_called_with(url=bulk.bulk_base + '/syncs/1',
                                auth=bulk.auth)

@patch('pyeloqua.bulk.requests.get')
def test_check_sync_update(mock_get):
    """ check on status of 'active' sync - update job_sync """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_ACTIVE
    bulk.check_sync()
    assert bulk.job_sync == SYNC_RESPONSE_ACTIVE


@patch('pyeloqua.bulk.requests.get')
def test_check_sync_notfinished(mock_get):
    """ check on status of 'active' sync - return False """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_ACTIVE
    status = bulk.check_sync()
    assert status is False


@patch('pyeloqua.bulk.requests.get')
def test_check_sync_success(mock_get):
    """ check on status of 'success' sync - return True """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_SUCCESS
    status = bulk.check_sync()
    assert status is True


@patch('pyeloqua.bulk.requests.get')
def test_check_sync_warning(mock_get):
    """ check on status of 'warning' sync - return True """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_WARNING
    status = bulk.check_sync()
    assert status is True


@patch('pyeloqua.bulk.requests.get')
def test_check_sync_error(mock_get):
    """ check on status of 'error' sync - return True """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_sync = SYNC_RESPONSE
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_ERROR
    status = bulk.check_sync()
    assert status is True


###############################################################################
# do all the sync needful
###############################################################################

@patch('pyeloqua.bulk.requests.post')
@patch('pyeloqua.bulk.requests.get')
def test_run_sync(mock_get, mock_post):
    """ fcn to run a sync end-to-end until finished """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_post.return_value = Mock(ok=True, status_code=200)
    mock_post.return_value.json.return_value = deepcopy(SYNC_RESPONSE)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = SYNC_RESPONSE_SUCCESS
    status = bulk.sync()
    assert status == 'success'
