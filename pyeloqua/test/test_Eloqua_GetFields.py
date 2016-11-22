from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetFields_EntityException(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.GetFields(entity='bad')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetFields_CdoIdException(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.GetFields(entity='customObjects')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetFields_BadStatusException(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=500)
    x = elq.GetFields(entity='contacts')
