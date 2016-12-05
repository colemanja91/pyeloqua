from nose.tools import *
from mock import patch, Mock

import requests
from pyeloqua import Eloqua
from .test_successfulInit import elqLogin
from .test_Eloqua_CreateDef_response import export_activity, export_contacts, export_accounts, export_customobjects, import_contacts, import_accounts, import_customobjects

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_BadDefType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='bad', entity='contacts', fields={'test': 'test'})

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_NoFields(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='contacts', fields={})

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ImportsTooManyFields(mock_get):
    fields = dict((i, i) for i in range(101))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='imports', entity='contacts', fields=fields)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_BadEntity(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='bad', fields={'test': 'test'})

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_BadActivitySyncAction(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='activities', fields={'test': 'test'}, syncActions=range(11))

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ExportsTooManySyncAction(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='contacts', fields={'test': 'test'}, syncActions=range(11))

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ImportsTooManySyncAction(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='imports', entity='contacts', fields={'test': 'test'}, syncActions=range(2))

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_CdoTooManyFields(mock_get):
    fields = dict((i, i) for i in range(101))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='customObjects', fields=fields, cdoID=1)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ContactsTooManyFields(mock_get):
    fields = dict((i, i) for i in range(251))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='contacts', fields=fields)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_AccountsTooManyFields(mock_get):
    fields = dict((i, i) for i in range(101))
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='accounts', fields=fields)

@patch('pyeloqua.pyeloqua.requests.get')
@raises(Exception)
def test_CreateDef_ActivitiesMissingType(mock_get):
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    x = elq.CreateDef(defType='exports', entity='activities', fields={'test': 'test'})

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_Activities(mock_post, mock_get):
    fields = {"ActivityId":"{{Activity.Id}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_activity
    x = elq.CreateDef(defType='exports', entity='activities', defName='test', activityType='EmailSend', fields=fields)
    assert x['uri']=="/activities/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_Contacts(mock_post, mock_get):
    fields = {"EmailAddress": "{{Contact.Field(C_EmailAddress)}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_contacts
    x = elq.CreateDef(defType='exports', entity='contacts', defName='test', fields=fields)
    assert x['uri']=="/contacts/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_Accounts(mock_post, mock_get):
    fields = {"AccountName":"{{Account.Field(M_CompanyName)}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_accounts
    x = elq.CreateDef(defType='exports', entity='accounts', defName='test', fields=fields)
    assert x['uri']=="/accounts/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_CustomObjects(mock_post, mock_get):
    fields = {"ID":"{{CustomObject[1].ExternalId}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_customobjects
    x = elq.CreateDef(defType='exports', entity='customObjects', cdoID=1, defName='test', fields=fields)
    assert x['uri']=="/customObjects/1/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_Filter_Contacts(mock_post, mock_get):
    fields = {"EmailAddress": "{{Contact.Field(C_EmailAddress)}}"}
    filters = " '{{Contact.Field(C_EmailAddress)}}' = 'test@test.com' "
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_contacts
    x = elq.CreateDef(defType='exports', entity='contacts', defName='test', fields=fields, filters=filters)
    assert x['uri']=="/contacts/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_Filter_Accounts(mock_post, mock_get):
    fields = {"AccountName":"{{Account.Field(M_CompanyName)}}"}
    filters = " '{{Account.Field(M_CompanyName)}}' = 'Test company' "
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_accounts
    x = elq.CreateDef(defType='exports', entity='accounts', defName='test', fields=fields, filters=filters)
    assert x['uri']=="/accounts/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Export_Filter_CustomObjects(mock_post, mock_get):
    fields = {"ID":"{{CustomObject[1].ExternalId}}"}
    filters = " '{{CustomObject[1].ExternalId}}' = '1234' "
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = export_customobjects
    x = elq.CreateDef(defType='exports', entity='customObjects', cdoID=1, defName='test', fields=fields, filters=filters)
    assert x['uri']=="/customObjects/1/exports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Import_Contacts(mock_post, mock_get):
    fields = {"EmailAddress": "{{Contact.Field(C_EmailAddress)}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = import_contacts
    x = elq.CreateDef(defType='imports', entity='contacts', defName='test', fields=fields)
    assert x['uri']=="/contacts/imports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Import_Accounts(mock_post, mock_get):
    fields = {"AccountName":"{{Account.Field(M_CompanyName)}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = import_accounts
    x = elq.CreateDef(defType='imports', entity='accounts', defName='test', fields=fields)
    assert x['uri']=="/accounts/imports/1234"

@patch('pyeloqua.pyeloqua.requests.get')
@patch('pyeloqua.pyeloqua.requests.post')
def test_CreateDef_Import_CustomObjects(mock_post, mock_get):
    fields = {"ID":"{{CustomObject[1].ExternalId}}"}
    mock_get.return_value = Mock(ok=True, status_code=200)
    mock_get.return_value.json.return_value = elqLogin
    elq = Eloqua(company = 'test', username = 'test', password = 'test')
    mock_post.return_value = Mock(ok=True, status_code=201)
    mock_post.return_value.json.return_value = import_customobjects
    x = elq.CreateDef(defType='imports', entity='customObjects', cdoID=1, defName='test', fields=fields)
    assert x['uri']=="/customObjects/1/imports/1234"


# @patch('pyeloqua.pyeloqua.requests.get')
# def test_GetCdoId_OneMatchFound(mock_get):
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = elqLogin
#     elq = Eloqua(company = 'test', username = 'test', password = 'test')
#     mock_get.return_value = Mock(ok=True, status_code=200)
#     mock_get.return_value.json.return_value = cdoResultOne
#     x = elq.GetCdoId(cdoName='test')
#     assert x==123
