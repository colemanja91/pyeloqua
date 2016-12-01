from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_GetCdoId_response import cdoResultOne, cdoResultNone, cdoResultMany

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetCdoId_CdoNameRequired(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.GetCdoId()
#
# @patch('pyeloqua.pyeloqua.requests.get')
# def test_GetCdoId_OneMatchFound(mock_get):
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = elqLogin
#     elq = Eloqua(company = 'test', username = 'test', password = 'test')
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = cdoResultOne
#     x = elq.GetCdoId(cdoName='test')
#     assert x==123
#
# @patch('pyeloqua.pyeloqua.requests.get')
# @raises(Exception)
# def test_GetCdoId_ManyMatchFound(mock_get):
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = elqLogin
#     elq = Eloqua(company = 'test', username = 'test', password = 'test')
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = cdoResultMany
#     x = elq.GetCdoId(cdoName='test')
#
# @patch('pyeloqua.pyeloqua.requests.get')
# @raises(Exception)
# def test_GetCdoId_NoneMatchFound(mock_get):
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = elqLogin
#     elq = Eloqua(company = 'test', username = 'test', password = 'test')
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = cdoResultNone
#     x = elq.GetCdoId(cdoName='test')
