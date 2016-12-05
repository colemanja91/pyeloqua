from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_FilterExists_response import filterResultMany, filterResultNone, filterResultOne
from .test_Eloqua_CreateSyncAction_response import contact_addList, contact_removeList, account_addList, account_removeList, AccountListResultOne

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateSyncAction_SetStatus_MissingDestination(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateSyncAction(action='setStatus')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateSyncAction_Add_MissingDestination(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateSyncAction(action='add')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateSyncAction_Remove_MissingDestination(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateSyncAction(action='remove')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateSyncAction_Add_Contacts_ListMultiple(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = filterResultMany
    x = elq.CreateSyncAction(action='add', listName='test', listType='contacts')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateSyncAction_Add_Contacts_ListNone(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = filterResultNone
    x = elq.CreateSyncAction(action='add', listName='test', listType='contacts')

@patch('pyeloqua.pyeloqua.requests.get')
def test_CreateSyncAction_Add_Contacts_ListOne(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = filterResultOne
    x = elq.CreateSyncAction(action='add', listName='test', listType='contacts')
    assert x==contact_addList

@patch('pyeloqua.pyeloqua.requests.get')
def test_CreateSyncAction_Remove_Contacts_ListOne(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = filterResultOne
    x = elq.CreateSyncAction(action='remove', listName='test', listType='contacts')
    assert x==contact_removeList

@patch('pyeloqua.pyeloqua.requests.get')
def test_CreateSyncAction_Add_Accounts_ListOne(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = AccountListResultOne
    x = elq.CreateSyncAction(action='add', listName='test', listType='accounts')
    assert x==account_addList

@patch('pyeloqua.pyeloqua.requests.get')
def test_CreateSyncAction_Remove_Accounts_ListOne(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = AccountListResultOne
    x = elq.CreateSyncAction(action='remove', listName='test', listType='accounts')
    assert x==account_removeList
