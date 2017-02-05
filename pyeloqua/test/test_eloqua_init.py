""" Eloqua class initialization """
from nose.tools import raises
from mock import patch, Mock

from requests.exceptions import HTTPError
from pyeloqua import Eloqua

###############################################################################
# constant definitions
###############################################################################

ELQ_LOGIN = {
    "site": {
        "id": 1234,
        "name": "test"
    },
    "user": {
        "id": 111,
        "username": "test",
        "displayName": "testing mctestface",
        "firstName": "testing",
        "lastName": "mctestface",
        "emailAddress": "test@test.com"
    },
    "urls": {
        "base": "https://secure.p01.eloqua.com",
        "apis": {
            "soap": {
                "standard":
                "https://secure.p01.eloqua.com/API/{version}/Service.svc",
                "dataTransfer":
                "https://secure.p01.eloqua.com/API/{version}/DataTransferService.svc",
                "email":
                "https://secure.p01.eloqua.com/API/{version}/EmailService.svc",
                "externalAction":
                "https://secure.p01.eloqua.com/API/{version}/ExternalActionService.svc"
            },
            "rest": {
                "standard": "https://secure.p01.eloqua.com/API/REST/{version}/",
                "bulk": "https://secure.p01.eloqua.com/API/Bulk/{version}/"
            }
        }
    }
}

###############################################################################
# exceptions
###############################################################################


@raises(Exception)
def test_elq_no_user():
    """ username required """
    Eloqua(company='test', password='test')


@raises(Exception)
def test_elq_no_company():
    """ company required """
    Eloqua(username='test', password='test')


@raises(Exception)
def test_elq_no_pwd():
    """ password required """
    Eloqua(company='test', username='test')


@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_elq_invalid_auth(mock_get):
    """ exception raised on bad credentials """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = "Not authenticated."
    Eloqua(company='test', username='test', password='badtest')


@patch('pyeloqua.pyeloqua.requests.get')
@raises(HTTPError)
def test_elq_unknown_error(mock_get):
    """ exception raised on non-200 status code """
    mock_response = Mock()
    http_error = HTTPError()
    mock_response.raise_for_status.side_effect = http_error
    mock_get.return_value = mock_response
    Eloqua(company='test', username='test', password='test')

###############################################################################
# object values set
###############################################################################

@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_user(mock_get):
    """ set username """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.username == 'test'


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_company(mock_get):
    """ set company """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.company == 'test'


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_password(mock_get):
    """ set password """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.password == 'test'


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_auth(mock_get):
    """ set auth tuple """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.auth == ('test\\test', 'test')


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_userid(mock_get):
    """ set user ID """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.userId == 111


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_userdisplay(mock_get):
    """ set user display name """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.userDisplay == 'testing mctestface'


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_url_base(mock_get):
    """ set URL base """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.urlBase == 'https://secure.p01.eloqua.com'


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_siteid(mock_get):
    """ set site ID """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.siteId == 1234


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_rest_base(mock_get):
    """ set REST API base """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.restBase == 'https://secure.p01.eloqua.com/API/REST/2.0/'


@patch('pyeloqua.pyeloqua.requests.get')
def test_elq_set_bulk_base(mock_get):
    """ set Bulk API base """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = ELQ_LOGIN
    elq = Eloqua(company='test', username='test', password='test')
    assert elq.bulkBase == 'https://secure.p01.eloqua.com/API/Bulk/2.0/'

# make sure test mode for authentication works (useful for other unit tests)


def test_elq_test():
    """ test mode for authentication """
    elq = Eloqua(test=True)
    assert elq.auth == ('test\\test', 'test')
