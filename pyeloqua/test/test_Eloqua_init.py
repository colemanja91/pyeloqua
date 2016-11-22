from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin

# Test basic functions around Eloqua class
@raises(Exception)
def test_EloquaInit_MissingUsername():
    elq = Eloqua(company = 'test', password = 'test')

@raises(Exception)
def test_EloquaInit_MissingCompany():
    elq = Eloqua(username = 'test', password = 'test')

@raises(Exception)
def test_EloquaInit_MissingPassword():
    elq = Eloqua(company = 'test', username = 'test')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(ValueError)
def test_EloquaInit_NotAuthenticated(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = "Not authenticated."
    elq = Eloqua(company = 'test', username = 'test', password = 'badtest')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_EloquaInit_UnknownAPIError(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=500)
    elq = Eloqua(company = 'test', username = 'test', password = 'test')

@patch('pyeloqua.pyeloqua.requests.get')
def test_EloquaInit_SetUsername(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    assert elq.username == 'test'

@patch('pyeloqua.pyeloqua.requests.get')
def test_EloquaInit_SetCompany(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    assert elq.company == 'test'

@patch('pyeloqua.pyeloqua.requests.get')
def test_EloquaInit_SetPassword(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    assert elq.password == 'test'

@patch('pyeloqua.pyeloqua.requests.get')
def test_EloquaInit_SetAuth(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    assert elq.auth == ('test\\test', 'test')
