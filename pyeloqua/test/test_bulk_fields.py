""" Eloqua.Bulk job setup methods (fields) """
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

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
        }
    ],
    "totalResults": 1,
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "hasMore": False
}

###############################################################################
# Methods to add fields to a job
###############################################################################


@patch('pyeloqua.bulk.requests.get')
def test_get_fields_cntcts_call(mock_get):
    """ find all contact fields """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    bulk.get_fields()
    url = bulk.bulk_base + '/contacts/fields?limit=1000&offset=0'
    mock_get.assert_any_call(url=url, auth=bulk.auth)

@patch('pyeloqua.bulk.requests.get')
def test_get_fields_cntcts_return(mock_get):
    """ find all contact fields """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = GOOD_FIELDS
    fields = bulk.get_fields()
    assert fields == GOOD_FIELDS['items']
