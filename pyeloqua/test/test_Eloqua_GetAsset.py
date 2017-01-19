from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin

listReturn = {
  "type": "ContactList",
  "currentStatus": "active",
  "id": "1",
  "createdAt": "1290186929",
  "createdBy": "1",
  "depth": "complete",
  "description": "",
  "folderId": "260",
  "name": "testList",
  "permissions": [
    "Retrieve",
    "SetSecurity",
    "Delete",
    "Update"
  ],
  "updatedAt": "1290186929",
  "updatedBy": "1",
  "count": "400",
  "dataLookupId": "",
  "scope": "global"
}

@patch('pyeloqua.pyeloqua.requests.get')
def test_GetAsset_ReturnNone(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=404)
    mock_get.return_value.json.return_value = {}
    x = elq.GetAsset(assetType='list', assetId=10000000)
    assert not x

@patch('pyeloqua.pyeloqua.requests.get')
def test_GetAsset_ReturnList(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = listReturn
    x = elq.GetAsset(assetType='list', assetId=1)
    print(x)
    assert x == listReturn

@patch('pyeloqua.pyeloqua.requests.get')
@raises(ValueError)
def test_GetAsset_BadType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.GetAsset(assetType='bad', assetId=10000000)
