from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_getLeadScoreModelId_response import leadScoreModelResultOne, leadScoreModelResultNone, leadScoreModelResultMany

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetLeadScoreModelId_ModelNameRequired(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.getLeadScoreModelId()

@patch('pyeloqua.pyeloqua.requests.get')
def test_GetLeadScoreModelId_OneMatchFound(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = leadScoreModelResultOne
    x = elq.getLeadScoreModelId(modelName='test')
    assert x==1

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetLeadScoreModelId_ManyMatchFound(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = leadScoreModelResultMany
    x = elq.getLeadScoreModelId(cdoName='test')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_GetLeadScoreModelId_NoneMatchFound(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = leadScoreModelResultNone
    x = elq.getLeadScoreModelId(cdoName='test')
