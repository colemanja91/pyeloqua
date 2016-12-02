from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_GetCdoId_response import cdoResultOne, cdoResultNone, cdoResultMany

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_BadDefType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='bad', entity='contacts', fields={'test': 'test'})

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_NoFields(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='contacts', fields={})

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ImportsTooManyFields(mock_get):
    fields = dict((i, i) for i in range(101))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='imports', entity='contacts', fields=fields)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_BadEntity(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='bad', fields={'test': 'test'})

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_BadActivitySyncAction(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='activities', fields={'test': 'test'}, syncActions=range(11))

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ExportsTooManySyncAction(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='contacts', fields={'test': 'test'}, syncActions=range(11))

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ImportsTooManySyncAction(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='imports', entity='contacts', fields={'test': 'test'}, syncActions=range(2))

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_CdoTooManyFields(mock_get):
    fields = dict((i, i) for i in range(101))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='customObjects', fields=fields, cdoID=1)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ContactsTooManyFields(mock_get):
    fields = dict((i, i) for i in range(251))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='contacts', fields=fields)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_AccountsTooManyFields(mock_get):
    fields = dict((i, i) for i in range(101))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='accounts', fields=fields)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ActivitiesMissingType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='activities', fields={'test': 'test'})



# @patch('pyeloqua.pyeloqua.requests.get')
# def test_GetCdoId_OneMatchFound(mock_get):
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = elqLogin
#     elq = Eloqua(company = 'test', username = 'test', password = 'test')
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = cdoResultOne
#     x = elq.GetCdoId(cdoName='test')
#     assert x==123
