from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_FilterExists_response import filterResultOne, filterResultNone, filterResultMany

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_FilterDateRange_StartEndBlank(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.FilterDateRange(entity='contacts', field='CreatedAt')

# @patch('pyeloqua.pyeloqua.requests.get')
# def test_FilterExists_OneMatchFound(mock_get):
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = elqLogin
#     elq = Eloqua(company = 'test', username = 'test', password = 'test')
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = filterResultOne
#     x = elq.FilterExists(name='test', existsType='ContactList')
#     assert x=="EXISTS('{{ContactList[1]}}')"
