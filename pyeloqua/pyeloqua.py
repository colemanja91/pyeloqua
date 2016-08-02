from datetime import datetime
import requests
import json
import time
import warnings
from . import system_fields

API_VERSION = '2.0'

POST_HEADERS = {'Content-Type':'application/json'}

class Eloqua(object):

    """ Eloqua instance:
            Wraps an Eloqua session to more easily access base API URLs and make instance and user info available.
            User must have at least 'Advanced Marketing User' or 'API User' permissions
            Any contact level security labels will also apply through the API
    """

    def __init__(self, username=None, password=None, company=None, bulk_api_version = API_VERSION,
                 rest_api_version = API_VERSION):

        """
        Create an Eloqua session given the following arguments:

        Arguments:

        * username -- Eloqua username to authenticate against
        * password -- Password associated with above user
        * company -- Company/Instance name for above user
        * bulk_api_version -- Version of Eloqua Bulk API to use; defaults to 2.0
        * rest_api_version -- Version of Eloqua REST API to use; defaults to 2.0
        """

        if all(arg is not None for arg in (username, password, company)):

            url = 'https://login.eloqua.com/id'
            req = requests.get(url, auth=(company + '\\' + username, password))
            if req.status_code==200:
                if req.json()=='Not authenticated.':
                    raise ValueError('Invalid login credentials')
                else:
                    self.username = username
                    self.password = password
                    self.company = company
                    self.auth = (company + '\\' + username, password)
                    self.userId = req.json()['user']['id']
                    self.userDisplay = req.json()['user']['displayName']
                    self.urlBase = req.json()['urls']['base']
                    self.siteId = req.json()['site']['id']

                    restBase = req.json()['urls']['apis']['rest']['standard']
                    self.restBase = restBase.replace('{version}', rest_api_version)

                    bulkBase = req.json()['urls']['apis']['rest']['bulk']
                    self.bulkBase = bulkBase.replace('{version}', bulk_api_version)
            else:
                raise Exception('Unknown authentication error')
        else:
            raise ValueError('Please enter all required login details: company, username, password')

    '''
        ###################################################
        Bulk API 2.0
        ###################################################
    '''

    def GetFields(self, entity, cdoID=0, fields=[]):

        """
            Retrieve all fields for a specified entitiy

            Arguments:

            * entity -- one of: contacts, customObjects, or accounts
            * cdoID -- identifier of specific CDO; required if entity = 'customObjects'; use method GetCdoId to retrieve
            * fields -- list of specific fields to retrieve, either by 'Display Name' or 'Database Name'; optional
        """

        if entity not in ['contacts', 'customObjects', 'accounts']:
            raise ValueError("Please choose a valid 'entity' value: 'contacts', 'accounts', 'customObjects'")

        if entity == 'customObjects':
            if cdoID==0:
                raise ValueError("Please specify a cdoID")

            url = self.bulkBase + '/customobjects/' + str(cdoID) + '/fields'
        else:
            url = self.bulkBase + entity + '/fields'

        req = requests.get(url, auth = self.auth)

        fieldsReturn = []

        if req.status_code == 200:

            if len(fields)>0:

                for item in req.json()['items']:

                    if item['name'] in fields:
                        fieldsReturn.append(item)
                    elif item['internalName'] in fields:
                        fieldsReturn.append(item)

            else:

                fieldsReturn = req.json()['items']

            return fieldsReturn

        else:

            raise Exception("Failure getting fields: " + str(req.status_code))

    def CreateFieldStatement(self, entity, fields = '', cdoID = 0, useInternalName=True, addSystemFields=[],
                             addActivityFields=[], activityType='', leadScoreModelId = 0, addSystemContactFields=[],
                             addLinkedContactFields=[]):

        """
            Given a set of field names, create a "fields" statement for use in Bulk import/export definitions

            Arguments:

            * entity -- one of: contacts, customObjects, accounts, activities
            * fields -- list of specific fields to retrieve, either by 'Display Name' or 'Database Name'; optional
            * cdoID -- identifier of specific CDO; required if entity = 'customObjects'; use method GetCdoId to retrieve
            * useInternalName -- If True, import / export defined field names use 'Database Name'
            * addSystemFields -- DEPRECATED: Use addSystemContactFields instead. List of system fields to include in statement; see CONTACT_SYSTEM_FIELDS
            * addActivityFields -- List of activity fields to include; required if entity = 'activities'; see ACTIVITY_FIELDS
            * activityType -- export type
            * leadScoreModelId -- add lead score model fields to contact export
            * addSystemContactFields -- List of system fields to include in statement relative to [linked] contacts; see CONTACT_SYSTEM_FIELDS
            * addLinkedContactFields -- List of fields to add in CDO record exports

        """

        if (entity in ['contacts', 'customObjects', 'accounts'] and fields == '' and len(addSystemFields)==0):
            raise Exception('Please specify one or more entity or system fields')

        if (len(addSystemFields)>0):
            warnings.warn("The addSystemFields parameter has been deprecated. Please use addSystemContactFields")
            for field in addSystemFields:
                if field not in addSystemContactFields:
                    addSystemContactFields.append(field)

        if (len(addLinkedContactFields)>0 and entity!='customObjects'):
            raise Exception('Linked contact fields may only be included for CDO exports')

        fieldStatement = {}

        if (entity=='contacts' and leadScoreModelId>0):
            fieldStatement['Rating'] = '{{Contact.LeadScore.Model[%s].Rating}}' % leadScoreModelId
            fieldStatement['Profile'] = '{{Contact.LeadScore.Model[%s].ProfileScore}}' % leadScoreModelId
            fieldStatement['Engagement'] = '{{Contact.LeadScore.Model[%s].EngagementScore}}' % leadScoreModelId
        elif(entity!='contacts' and leadScoreModelId>0):
            raise TypeError("Lead Scoring fields can only be included with contact exports")

        if (entity == 'activities'):
            if activityType in ('EmailSend', 'EmailOpen', 'EmailClickthrough', 'FormSubmit', 'Subscribe',
                                'Unsubscribe', 'Bounceback', 'WebVisit', 'PageView'):
                if len(addActivityFields)>0:
                    for field in addActivityFields:
                        if field in system_fields.ACTIVITY_FIELDS[activityType]:
                            fieldStatement[field] = system_fields.ACTIVITY_FIELDS[activityType][field]
                        else:
                            raise ValueError("Activity field not recognized: " + field)
                else:
                    fieldStatement = system_fields.ACTIVITY_FIELDS[activityType]
            else:
                raise ValueError("Invalid activity type: " + activityType)
        else:
            fieldSet = self.GetFields(entity = entity, fields = fields, cdoID = cdoID)

            if len(addSystemFields)>0:
                for field in addSystemContactFields:
                    if field in system_fields.CONTACT_SYSTEM_FIELDS:
                        fieldStatement[field] = system_fields.CONTACT_SYSTEM_FIELDS[field]
                    else:
                        raise ValueError("System field not recognized: " + field)

            if len(fieldSet)>0:
                for field in fieldSet:
                    if useInternalName:
                        fieldStatement[field['internalName']] = field['statement']
                    else:
                        fieldStatement[field['name']] = field['statement']
            else:
                raise Exception("No fields found")

        if len(addLinkedContactFields)>0:

            linkedContactFields = self.CreateFieldStatement(entity='contacts', fields=addLinkedContactFields)

            for field in linkedContactFields:
                linkedContactFields[field] = linkedContactFields[field].replace('{{Contact.', '{{CustomObject[%s].Contact.') % cdoID
                fieldStatement.update(linkedContactFields)

        return fieldStatement

    def GetCdoId(self, cdoName):

        """
            Get a Custom Data Object's ID given it's name

            Arguments:

            * cdoName -- verbatim name of CDO; case insensitive

        """

        cdoName = cdoName.replace(' ', '*')

        url = self.bulkBase + '/customobjects?q="name=' + str(cdoName) + '"'

        req = requests.get(url, auth = self.auth)

        if req.json()['totalResults']==1:
            cdoUri = req.json()['items'][0]['uri']
            cdoId = int(cdoUri.replace('/customObjects/', ''))
            return cdoId
        elif req.json()['totalResults']>1:
            raise Exception("Multiple CDOs with matching name")
            raise Exception("WTF?")
        else:
            raise Exception("No matching CDOs found")

    def getLeadScoreModelId(self, modelName):
        '''
            Returns model ID for a given lead score model
        '''

        modelName = modelName.replace(' ', '*')

        url = self.bulkBase + '/contacts/scoring/models?q="name=' + modelName + "'"

        req = requests.get(url, auth = self.auth)

        if req.json()['totalResults']==1:
            modelId = req.json()['items'][0]['id']
            return modelId
        elif req.json()['totalResults']>1:
            raise Exception("Multiple models found")
        else:
            raise Exception("No matching models found")

    def FilterExists(self, name, existsType):

        """
            Given an object name, create an "EXISTS" statement (Eloqua Bulk equivalent of "in")

            Arguments:

            * name -- Name of object
            * existsType -- type of existence; one of ContactFilter, ContactList, ContactSegment, or AccountList

        """

        name = name.replace(' ', '*')

        if existsType=='ContactFilter':
            url = self.bulkBase + '/contacts/filters?q="name=' + name + '"'
        elif existsType=='ContactSegment':
            url = self.bulkBase + '/contacts/segments?q="name=' + name + '"'
        elif existsType=='ContactList':
            url = self.bulkBase + '/contacts/lists?q="name=' + name + '"'
        elif existsType=='AccountList':
            url = self.bulkBase + '/accounts/lists?q="name=' + name + '"'
        else:
            raise Exception("Please choose a valid 'existsType': 'ContactFilter', 'ContactSegment', 'ContactList', 'AccountList'")

        req = requests.get(url, auth = self.auth)

        if req.json()['totalResults']==1:
            filterStatement = "EXISTS('" + req.json()['items'][0]['statement'] + "')"
            return filterStatement
        elif req.json()['totalResults']>1:
            raise Exception("Multiple " + existsType + "s found")
        else:
            raise Exception("No matching " + existsType + " found")

    def FilterDateRange(self, entity, field='', start='', end='', cdoID=0):

        '''
            Given an Eloqua date field, create a bounded or open date range filter

            Arguments:

            * entity -- one of: contacts, customObjects, accounts, activities
            * field -- field to filter by; must resolve to a date type field
            * start -- beginning of date range
            * end -- end of date range
            * cdoID -- identifier of specific CDO; required if entity = 'customObjects'; use method GetCdoId to retrieve

        '''

        if (start=='' and end==''):
            raise ValueError("Please enter at least one datetime value: start, end")

        if (field=='' and entity!='activities'):
            raise ValueError("Parameter 'field' is required for entity '" + entity + "'")

        if (entity == 'activities'):
            field = 'ActivityDate'

        try:
            test1 = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            test2 = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        except:
            raise ValueError("Invalid datetime format; use 'YYYY-MM-DD hh:mm:ss'")

        if (entity!='activities' or (entity in ['contacts', 'accounts'] and field in ['createdAt', 'updatedAt'])):
            fieldDef = self.GetFields(entity=entity, fields=[field], cdoID=cdoID)

            if (fieldDef[0]['dataType'] != 'date'):
                raise Exception("Field '" + field + "' is not a date field")
            fieldStatement = fieldDef[0]['statement']
        elif (entity=='activities'):
            fieldStatement = system_fields.ACTIVITY_FIELDS['CommonFields']['ActivityDate']
        else:
            fieldStatement = system_fields.CONTACT_SYSTEM_FIELDS[field]

        statement = ''

        if (start!=''):
            statement += " '" + fieldStatement + "' >= '" + start + "' "
        if (start!='' and end!=''):
            statement += ' AND '
        if (end!=''):
            statement += " '" + fieldStatement + "' <= '" + end + "' "

        return statement


    def CreateDef(self, defType, entity, fields, cdoID=0, filters='', activityType='', defName=str(datetime.now()), identifierFieldName='', isSyncTriggeredOnImport=False):

        """
            Create an import/export definition

            Arguments:

            * defType -- One of: 'imports', 'exports'
            * entity --  one of: contacts, customObjects, activities, or accounts
            * fields -- A dictionary of fields to export; see CreateFieldStatement
            * filters -- A valid Bulk filter statement
            * defName -- Export definition name; defaults to current datetime
            * identifierFieldName -- unique identified field; required for imports
            * isSyncTriggeredOnImport -- If True, begin sync upon post of import data

        """

        if (defType not in ['imports', 'exports']):
            raise Exception("Please choose a defType value: 'imports', 'exports'")

        if len(fields)==0:
            raise Exception("Please specify at least one field to export")

        if (defType == 'imports' and len(fields)>100):
            raise Exception("Eloqua Bulk API only supports imports of up to 100 fields")

        if entity not in ['contacts', 'customObjects', 'accounts', 'activities']:
            raise Exception("Please choose a valid 'entity' value: 'contacts', 'accounts', 'customObjects', 'activities'")

        if entity == 'customObjects':
            if cdoID==0:
                raise Exception("Please specify a cdoID")
            if (len(fields)>100):
                raise Exception("Eloqua Bulk API can only export 100 CDO fields at a time")
            url = self.bulkBase + '/customobjects/' + str(cdoID) + '/' + defType

        if entity == 'contacts':
            if (len(fields)>250):
                raise Exception("Eloqua Bulk API can only export 250 contact fields at a time")
            url = self.bulkBase + '/contacts/' + defType

        if entity == 'accounts':
            if len(fields)>100:
                raise Exception("Eloqua Bulk API can only export 100 account fields at a time")
            url = self.bulkBase + '/accounts/' + defType

        if entity == 'activities':
            if len(fields)>100:
                raise Exception("Eloqua Bulk API can only export 100 activity fields at a time")
            if activityType=='':
                raise Exception("Please specify an activity type")
            url = self.bulkBase + '/activities/' + defType

            if filters=='':
                filters = "'{{Activity.Type}}' = '" + activityType + "' "
            else:
                filters = "'{{Activity.Type}}' = '" + activityType + "' AND " + filters

        if (defType=='exports'):

            if (len(filters)>0):

                data = {'name': defName, 'filter': filters, 'fields': fields}

            else:

                data = {'name': defName, 'fields': fields}

        else:

            data = {'name': defName, 'fields': fields, 'identifierFieldName': identifierFieldName, 'isSyncTriggeredOnImport': isSyncTriggeredOnImport}

        req = requests.post(url, data = json.dumps(data), headers = POST_HEADERS, auth = self.auth)

        if req.status_code==201:

            return req.json()

        else:

            raise Exception(req.json()['failures'][0])

    def GetDef(self, defURI='', defType=''):

        '''
            Get a single export/import definition or all

            Arguments:

            * defURI -- URI of pre-existing import/export definition; optional if selecting all
            * defType -- Definition type to retrieve; optional if defURI is provided
        '''

        defs = []

        if defURI!='':
            url = self.bulkBase + defURI

            req = requests.get(url, auth = self.auth)

            if req.status_code==200:
                defs.append(req.json())
            else:
                raise Exception(req.json()['failures'][0])
        elif defType!='':
            if defType in ['exports', 'imports']:
                hasMore = True
                offset = 0

                while hasMore:

                    url = self.bulkBase + defType + '?offset=' + str(offset)

                    req = requests.get(url, auth = self.auth)

                    defs.extend(req.json()['items'])

                    hasMore = req.json()['hasMore']

                    offset += 1000

            else:
                raise ValueError("defType must be one of the following: 'exports', 'imports'")
        else:
            raise ValueError("Must specify one of the following: defURI, defType")

        return defs


    def CreateSync(self, defObject={}, defURI=''):

        """
            Create a sync for a pre-defined import/export

            Arguments:

            * defObject -- JSON object returned from CreateDef; optional if defURI is provided
            * defURI -- URI of pre-existing import/export definition; optional if defObject is provided

        """

        if ('uri' not in defObject):

            if (len(defURI)==0):

                raise Exception("Must include a valid defObject or defURI")

            else:

                uri = defURI

        else:

            uri = defObject['uri']

        url = self.bulkBase + '/syncs'

        data = {'syncedInstanceUri': uri}

        req = requests.post(url, data = json.dumps(data), headers = POST_HEADERS, auth = self.auth)

        if req.status_code==201:

            return req.json()

        else:

            raise Exception("Could not create sync: " + uri)

    def CheckSyncStatus(self, syncObject={}, syncURI='', timeout=500, interval=10):

        """
            Get the current status of an existing sync

            Arguments:

            * syncObject -- JSON object returned from CreateSync; optional if syncURI is provided
            * syncURI -- URI of pre-existing sync; optional if syncObject is provided
            * timeout -- seconds to check sync
            * interval -- wait time between checking status

        """
        if ('uri' not in syncObject):
            if (len(syncURI)==0):
                raise Exception("Must include a valid syncObject or syncURI")
            else:
                uri = syncURI
        else:
            uri = syncObject['uri']

        url = self.bulkBase + uri

        waitTime = 0
        notSynced = True
        while notSynced:
            req = requests.get(url, auth = self.auth)
            if req.status_code != 200: ### TODO: Fix this error handling
                warnings.warn(req.json())
            status = req.json()['status']
            if (status in ['success', 'warning', 'error']):
                return status
            elif (waitTime<timeout):
                waitTime += interval
                time.sleep(interval)
            else:
                raise Exception("Export not finished syncing after " + str(waitTime) + " seconds: " + uri)

    def GetSyncedRecordCount(self, defObject={}, defURI=''):

        '''
            Get number of synced records for an export

            Arguments:

            * defObject -- JSON object returned from CreateDef; optional if defURI is provided
            * defURI -- URI of pre-existing import/export definition; optional if defObject is provided

        '''

        if ('uri' not in defObject):
            if (len(defURI)==0):
                raise Exception("Must include a valid defObject or defURI")
            else:
                uri = defURI
        else:
            uri = defObject['uri']

        url = self.bulkBase + uri + '/data?limit=1&offset=0'

        req = requests.get(url, auth=self.auth)

        totalResults = req.json()['totalResults']

        return totalResults

    def GetSyncRejectedRecords(self, syncObject={}, syncURI='', maxRecords=1000):

        '''
            Returns set of (at most) first 1000 records rejected from import

            Arguments:
            * syncObject -- JSON object returned from CreateSync; optional if syncURI is provided
            * syncURI -- URI of pre-existing sync; optional if syncObject is provided
            * maxRecords -- maximum number of records to query; capped at 1000; use 1 to just get # of rejects
        '''

        if ('uri' not in syncObject):
            if (len(syncURI)==0):
                raise Exception("Must include a valid syncObject or syncURI")
            else:
                uri = syncURI
        else:
            uri = syncObject['uri']

        if (maxRecords>1000):
            raise ValueError("maxRecords must be <= 1000")

        url = self.bulkBase + uri + '/rejects?limit=' + str(maxRecords)

        req = requests.get(url, auth=self.auth)

        rejects = req.json()

        if (rejects['totalResults']>0):

            messages = []

            for row in rejects['items']:

                messages.append(row['message'])

            messageSummary = {}

            for row in messages:
                if row in messageSummary.keys():
                    messageSummary[row] += 1
                else:
                    messageSummary[row] = 1

            rejects['messages'] = messageSummary

        return rejects

    def GetSyncedData(self, defObject={}, defURI='', limit=50000, initOffset=0):

        """
            Retrieve data from a synced export

            Arguments:

            * defObject -- JSON object returned from CreateDef; optional if defURI is provided
            * defURI -- URI of pre-existing import/export definition; optional if defObject is provided
            * limit -- max number of records to retrieve (Eloqua max = 50,000); optional
            * initOffset -- Starting offset to retrieve from; optional

        """
        if ('uri' not in defObject):
            if (len(defURI)==0):
                raise Exception("Must include a valid defObject or defURI")
            else:
                uri = defURI
        else:
            uri = defObject['uri']

        offset = initOffset

        url = self.bulkBase + uri + '/data?'

        results = []

        hasMore = True

        while (hasMore):
            urlWhile = url + 'offset=' + str(offset) + '&limit=' + str(limit)
            req = requests.get(urlWhile, auth=self.auth)
            if 'items' in req.json():
                items = req.json()['items']
                for item in items:
                    results.append(item)
                offset += limit
            hasMore = req.json()['hasMore']

        return results

    def PostSyncData(self, data, defObject={}, defURI='', maxPost=20000, syncCount=80000, timeout=1000, interval = 60):

        """
            Post data to an import definition and sync at regular intervals

            Arguments:

            * data -- list of data to be imported where each record is a dictionary
            * defObject -- JSON object returned from CreateDef; optional if defURI is provided
            * defURI -- URI of pre-existing import/export definition; optional if defObject is provided
            * maxPost -- max count of records to import at once
            * syncCount -- threshold for syncing posted data

        """
        if ('uri' not in defObject):
            if (len(defURI)==0):
                raise Exception("Must include a valid defObject or defURI")
            else:
                uri = defURI
        else:
            uri = defObject['uri']

        if (maxPost>20000):
            raise Exception("It is not recommended to POST more than 20,000 records at a time. Please indicate a different maxPost value")

        if (syncCount>80000):
            raise Exception("It is recommended to sync at least every 80,000 records. Please indicate a different syncCount value")

        if (len(data)==0):
            raise Exception("Input data length is 0")

        hasMore = True
        offset = 0
        syncOffset = 0
        sendSet = []
        dataLen = len(data)
        url = self.bulkBase + uri + '/data'
        syncSet = []

        while (hasMore):
            for x in range(offset, min(offset+maxPost, dataLen), 1):
                sendSet.append(data[x])

            req = requests.post(url, data = json.dumps(sendSet), headers = POST_HEADERS, auth = self.auth)

            if req.status_code == 204:

                syncOffset += maxPost

                if (syncOffset >= syncCount or offset+maxPost>=dataLen):
                    syncOffset = 0
                    importSync = self.CreateSync(defObject=defObject, defURI=defURI)
                    syncStatus = self.CheckSyncStatus(syncObject=importSync, timeout=timeout, interval=interval)
                    syncInfo = {"uri": importSync['uri'], 'status': syncStatus}
                    syncInfo['count'] = len(sendSet)
                    syncInfo['rejectCount'] = self.GetSyncRejectedRecords(syncObject=importSync, maxRecords=1)['totalResults']
                    syncSet.append(syncInfo)

                if offset+maxPost>=dataLen:
                    hasMore = False
                    return syncSet
                else:
                    offset += maxPost
                    sendSet = []
            else:
                raise Exception(req.json()['failures'][0]) #### TODO: Fix this error handling

    '''
        ###################################################
        Eloqua Forms
        ###################################################
    '''

    def GetForm(self, formId=0, formHtmlName='', formName=''):

        '''
            Retreive Eloqua form metadata

            Arguments:
            * formId -- ID key of Eloqua form
            * formHtmlName -- HTML name of Eloqua form
            * formName -- Display name of Eloqua form
        '''

        if (formId==0 and formHtmlName=='' and formName==''):
            raise ValueError("Value required for one of: formId, formHtmlName, formName")
        if ((formId!=0 and (formHtmlName!='' or formName!='')) or (formHtmlName!='' and formName!='')):
            raise ValueError("More than one form identifier entered")

        if (formId!=0):
            url = self.restBase + '/assets/form/' + str(form.id) + '?depth=complete'
        else:
            url = self.restBase + '/assets/forms?depth=complete&search="' + formName + formHtmlName + '"'

        req = requests.get(url, auth=self.auth)

        if (req.status_code==200):
            form = req.json()
            if ('elements' in form.keys()):
                formElem = form['elements']
                form = formElem[0]
            return form
        else:
            raise Exception("Form not found: " + str(formId))

    def ValidateFormFields(self, data, form):

        '''
            Given a single-record dictionary of data to submit, validate that all fields are present in the specified form

            Arguments:
            * data -- dictionary of data to post to an Eloqua form
            * form -- Output from GetForm function
        '''

        formFieldSet = form['elements']
        formFields = []
        formFieldsHtml = []
        formFieldsNotFound = []

        for row in formFieldSet:
            formFields.append(row['name'])
            formFieldsHtml.append(row['htmlName'])

        for row in data.keys():
            if row not in formFields:
                if row not in formFieldsHtml:
                    formFieldsNotFound.append(row)

        if (len(formFieldsNotFound)>0):
            raise Exception("Following fields not found on form: " + ", ".join(formFieldsNotFound))
        else:
            return 1

    def PostToForm(self, data, formId=0, formHtmlName='', formName=''):

        '''
            Post a dictionary of data to an Eloqua form

            Arguments:
            * data -- dictionary of data to submit; can be either a dict (single record), or list of dict (multiple records). Keys must match HTML form names
            * formId -- ID key of Eloqua form
            * formHtmlName -- HTML name of Eloqua form
            * formName -- Display name of Eloqua form
        '''

        form = self.GetForm(formId=formId, formHtmlName=formHtmlName, formName=formName)

        url = 'https://s' + str(self.siteId) + '.t.eloqua.com/e/f2'

        if (isinstance(data, dict)):
            data = [data]

        querystring = {'elqSiteID': self.siteId, 'elqFormName': form['htmlName']}

        successCount = 0
        failCount = 0

        for row in data:
            val = self.ValidateFormFields(data = row, form = form)
            req = requests.post(url, params=querystring, data=row)
            if (req.content==b'\r\n'):
                successCount += 1
            else:
                failCount += 1

        return {'success': successCount, 'failure': failCount}

    '''
        ###################################################
        REST Functions
        ###################################################
    '''

    def DeleteRecord(self, entity, id, cdoID=0):

        '''
            Deletes a given record. Cannot be undone.

            Arguments:
            * entity -- one of: contact, customObject, account
            * id -- ID of record to be deleted. It will be gone forever.
            * cdoID -- identifier of specific CDO; required if entity = 'customObject'; use method GetCdoId to retrieve
        '''

        if entity not in ['contact', 'customObject', 'account']:
            raise ValueError("Please choose a valid 'entity' value: 'contact', 'account', 'customObject'")

        if entity=='customObject' and cdoID==0:
            raise ValueError("Please input a valid cdoID")

        if entity in ['contact', 'account']:
            uri = self.restBase + '/data/' + entity + '/' + str(id)
        else:
            uri = self.restBase + '/data/customObject/' + str(cdoID) + '/instance/' + str(id)

        req = requests.delete(uri, auth=self.auth)

        return req.status_code
