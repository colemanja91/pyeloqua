from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_FilterDateRange_response import dateType, notDateType

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_StartEndBlank(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='CreatedAt')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_FieldBlank(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_InvalidEntity(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='bad', field='CreatedAt', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_StartBadFormat(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='CreatedAt', start='something random', end='2016-10-11 01:00:00')

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_EndBadFormat(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='CreatedAt', start='2016-10-10 01:00:00', end='something random')

@patch('pyeloqua.pyeloqua.requests.get')
def test_FilterDateRange_Activity(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='activities', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')
    assert x==" '{{Activity.CreatedAt}}' >= '2016-10-10 01:00:00'  AND  '{{Activity.CreatedAt}}' <= '2016-10-11 01:00:00' "

@patch('pyeloqua.pyeloqua.requests.get')
def test_FilterDateRange_ActivityNoStart(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='activities', end='2016-10-11 01:00:00')
    assert x==" '{{Activity.CreatedAt}}' <= '2016-10-11 01:00:00' "

@patch('pyeloqua.pyeloqua.requests.get')
def test_FilterDateRange_ActivityNoEnd(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='activities', start='2016-10-10 01:00:00')
    assert x==" '{{Activity.CreatedAt}}' >= '2016-10-10 01:00:00' "

@patch('pyeloqua.pyeloqua.requests.get')
def test_FilterDateRange_ContactsCreatedAt(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='createdAt', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')
    assert x==" '{{Contact.CreatedAt}}' >= '2016-10-10 01:00:00'  AND  '{{Contact.CreatedAt}}' <= '2016-10-11 01:00:00' "

@patch('pyeloqua.pyeloqua.requests.get')
def test_FilterDateRange_ContactsUpdatedAt(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='updatedAt', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')
    assert x==" '{{Contact.UpdatedAt}}' >= '2016-10-10 01:00:00'  AND  '{{Contact.UpdatedAt}}' <= '2016-10-11 01:00:00' "

@patch('pyeloqua.pyeloqua.requests.get')
def test_FilterDateRange_ContactsDateType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = dateType
    x = elq.FilterDateRange(entity='contacts', field='Date Type', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')
    assert x==" '{{Contact.Field(C_Date_Type)}}' >= '2016-10-10 01:00:00'  AND  '{{Contact.Field(C_Date_Type)}}' <= '2016-10-11 01:00:00' "

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_ContactsNotDateType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = notDateType
    x = elq.FilterDateRange(entity='contacts', field='Email Address', start='2016-10-10 01:00:00', end='2016-10-11 01:00:00')
