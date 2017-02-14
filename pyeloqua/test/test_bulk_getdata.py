""" all methods of GETting data for Eloqua.Bulk """

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

RETURN_DATA = {
    "items": [
        {
            "contactID": "12345",
            "createdAt": "2017-01-01 00:00:00",
            "updatedAt": "2017-01-01 00:00:00"
        }
    ],
    "totalResults": 2,
    "limit": 1000,
    "offset": 0,
    "count": 2,
    "hasMore": False
}

###############################################################################
# grab some datas
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_get_data_call(mock_get):
    """ get data from an endpoint - api call """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(RETURN_DATA)
    bulk.get_data(endpoint='/dummyurl')
    mock_get.assert_called_with(url=bulk.bulk_base + '/dummyurl?limit=1000&offset=0',
                                auth=bulk.auth)


@patch('pyeloqua.bulk.requests.get')
def test_get_data_return(mock_get):
    """ get data from an endpoint - return data """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.job_def = EXPORT_JOB_DEF
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = deepcopy(RETURN_DATA)
    return_data = bulk.get_data(endpoint='/dummyurl')
    assert return_data == RETURN_DATA['items']
