from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua

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
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = "Not authenticated."
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
