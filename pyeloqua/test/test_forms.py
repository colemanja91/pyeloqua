""" Eloqua.Form unit tests """

from json import dump, load
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Form

###############################################################################
# Constants
###############################################################################

POST_HEADERS = {'Content-Type': 'application/json'}

FORM_SAMPLE = {
    'type': 'Form',
    'currentStatus': 'Draft',
    'id': '18',
    'createdAt': '1435261611',
    'createdBy': '19',
    'depth': 'complete',
    'folderId': '7',
    'name': 'Test Form',
    'permissions': 'fullControl',
    'updatedAt': '1435261612',
    'updatedBy': '19',
    'elements': [
        {
            'type': 'FormField',
            'id': '174',
            'name': 'Email Address',
            'createdFromContactFieldId': '100001',
            'dataType': 'text',
            'displayType': 'text',
            'fieldMergeId': '1',
            'htmlName': 'emailAddress'
        },
        {
            'type': 'FormField',
            'id': '175',
            'name': 'First Name',
            'createdFromContactFieldId': '100002',
            'dataType': 'text',
            'displayType': 'text',
            'fieldMergeId': '1',
            'htmlName': 'firstName'
        },
        {
            'type': 'FormField',
            'id': '176',
            'name': 'Submit',
            'dataType': 'text',
            'displayType': 'submit',
            'htmlName': 'submit'
        }
    ]
}

FORM_FIELDS = {
    '174': 'emailAddress',
    '175': 'firstName',
    '176': 'submit'
}

TEST_DATA = {
    'elements': [
        {
            'id': '1',
            'submittedAt': '1234567899',
            'fieldValues': [
                {
                    'id': '174',
                    'value': 'test1@test.com'
                },
                {
                    'id': '175',
                    'value': 'john'
                }
            ]
        },
        {
            'id': '2',
            'submittedAt': '1234567899',
            'fieldValues': [
                {
                    'id': '174',
                    'value': 'test2@test.com'
                },
                {
                    'id': '175'
                }
            ]
        }
    ],
    'page': 1,
    'pageSize': 1000,
    'total': 2
}

PARSED_DATA = [
    {
        'id': '1',
        'submittedAt': '1234567899',
        'emailAddress': 'test1@test.com',
        'firstName': 'john'
    },
    {
        'id': '2',
        'submittedAt': '1234567899',
        'emailAddress': 'test2@test.com'
    }
]

###############################################################################
# Tests - initialization
###############################################################################


@patch('pyeloqua.forms.requests.get')
def test_f_instance(mock_get):
    """ Initialize Form via form_id """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = FORM_SAMPLE
    assert isinstance(Form(test=True, form_id=1), Form)


@patch('pyeloqua.forms.requests.get')
def test_f_init_id(mock_get):
    """ Init Form instance with form_id """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = FORM_SAMPLE
    assert Form(test=True, form_id=1) is not None


def test_f_init_path():
    """ Init Form instance with form_path """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    assert Form(test=True, form_path=fpath) is not None


def test_f_init_path_id():
    """ Init Form instance with form_path and sets id """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    assert Form(test=True, form_path=fpath).form_id == '18'


def test_f_init_schema():
    """ Init form, set schema """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    assert Form(test=True, form_path=fpath).schema == FORM_SAMPLE


def test_f_init_fields():
    """ Init form, set fields """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    assert Form(test=True, form_path=fpath).fields == FORM_FIELDS


@raises(ValueError)
def test_f_id_path_req():
    """ Init form requires form_id or form_path """
    Form(test=True)


###############################################################################
# Tests - helpers
###############################################################################

def test_f_writeform():
    """ Init Form instance with form_path """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    form = Form(test=True, form_path=fpath)
    form.write_form('/tmp/pyeloqua_test_f_writeform.json')
    ofile = load(open('/tmp/pyeloqua_test_f_writeform.json', 'r'))
    assert ofile == form.schema


@patch('pyeloqua.forms.requests.get')
def test_f_get_form_calls(mock_get):
    """ _get_form calls API correctly """
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = FORM_SAMPLE
    form = Form(test=True, form_id=1)
    url = form.rest_base + 'assets/form/1?depth=complete'
    mock_get.assert_called_with(url=url, auth=form.auth)


def test_f_parse_data():
    """ _parse_data returns expected dict """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    form = Form(test=True, form_path=fpath)
    out = form._parse_data(TEST_DATA['elements'])
    assert out == PARSED_DATA


@patch('pyeloqua.forms.requests.get')
def test_f_get_data_parse(mock_get):
    """ get_data returns complete parsed data """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    form = Form(test=True, form_path=fpath)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = TEST_DATA
    out = form.get_data(start='123456789', end='987654321')
    assert out == PARSED_DATA


@patch('pyeloqua.forms.requests.get')
def test_f_get_data_calls(mock_get):
    """ get_data calls correct endpoint """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    form = Form(test=True, form_path=fpath)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = TEST_DATA
    form.get_data(start='123456789', end='987654321')
    url = form.rest_base + 'data/form/18?startAt=123456789&endAt=987654321&page=1'
    mock_get.assert_called_with(url=url, auth=form.auth)


@patch('pyeloqua.forms.requests.get')
def test_f_get_count_return(mock_get):
    """ get_count returns correct record count """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    form = Form(test=True, form_path=fpath)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = TEST_DATA
    out = form.get_count(start='123456789', end='987654321')
    assert out == 2


@patch('pyeloqua.forms.requests.get')
def test_f_get_count_calls(mock_get):
    """ get_count calls correct endpoint """
    fpath = '/tmp/pyeloqua_test_f_init_path.json'
    dump(FORM_SAMPLE, open(fpath, 'w'))
    form = Form(test=True, form_path=fpath)
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = TEST_DATA
    form.get_count(start='123456789', end='987654321')
    url = form.rest_base + 'data/form/18?startAt=123456789&endAt=987654321&count=1'
    mock_get.assert_called_with(url=url, auth=form.auth)
