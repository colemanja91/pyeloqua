from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_GetCdoId_response import cdoResultOne, cdoResultNone, cdoResultMany

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetDef_NoArgs(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.GetDef()

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetDef_BadDefType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.GetDef(defType='bad')
