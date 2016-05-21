from datetime import datetime
import requests
import json
import time
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
                    else:
                        if item['internalName'] in fields:
                            fieldsReturn.append(item)

                if (len(fieldsReturn)<len(fields)):

                    warnings.warn("Not all fields could be found") ## TODO: fix this

            else:

                fieldsReturn = req.json()['items']

            return fieldsReturn

        else:

            raise Exception("Failure getting fields: " + str(req.status_code))

    def CreateFieldStatement(self, entity, fields = '', cdoID = 0, useInternalName=True, addSystemFields=[],
                             addActivityFields=[], activityType='', leadScoreModelId = 0):

        """
            Given a set of field names, create a "fields" statement for use in Bulk import/export definitions

            Arguments:

            * entity -- one of: contacts, customObjects, accounts, activities
            * fields -- list of specific fields to retrieve, either by 'Display Name' or 'Database Name'; optional
            * cdoID -- identifier of specific CDO; required if entity = 'customObjects'; use method GetCdoId to retrieve
            * useInternalName -- If True, import / export defined field names use 'Database Name'
            * addSystemFields -- list of system fields to include in statement; see CONTACT_SYSTEM_FIELDS
            * addActivityFields -- List of activity fields to include; required if entity = 'activities'; see ACTIVITY_FIELDS
            * activityType -- export type
            * leadScoreModelId -- add lead score model fields to contact export

        """

        if (fields == '' and len(addSystemFields)==0):
            raise Exception('Please specify one or more entity or system fields')

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
                    raise ValueError("Please specify activity fields")
            else:
                raise ValueError("Invalid activity type: " + activityType)
        else:
            fieldSet = self.GetFields(entity = entity, fields = fields, cdoID = cdoID)

            if len(addSystemFields)>0:
                for field in addSystemFields:
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

            * name --
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

    def CreateDef(self, defType, entity, fields, cdoID=0, filters='', defName=str(datetime.now()), identifierFieldName='', isSyncTriggeredOnImport=False):

        """
            Create an import/export definition

            Arguments:

            * defType -- One of: 'imports', 'exports'
            * entity --  one of: contacts, customObjects, or accounts
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

        if entity not in ['contacts', 'customObjects', 'accounts']:
            raise Exception("Please choose a valid 'entity' value: 'contacts', 'accounts', 'customObjects'")

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

    def CheckSyncStatus(self, syncObject={}, syncURI='', timeout=500):

        """
            Get the current status of an existing sync

            Arguments:

            * syncObject -- JSON object returned from CreateSync; optional if syncURI is provided
            * syncURI -- URI of pre-existing sync; optional if syncObject is provided
            * timeout -- seconds to check sync

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
            if (status == 'success'):
                return 'success'
            elif (status in ['warning', 'error']):
                raise Exception("Sync finished with status 'warning' or 'error': " + uri)
            elif (waitTime<timeout):
                waitTime += 10
                time.sleep(10)
            else:
                raise Exception("Export not finished syncing after " + str(waitTime) + " seconds: " + uri)

    def GetSyncedData(self, defObject={}, defURI='', limit=50000):

        """
            Retrieve data from a synced export

            Arguments:

            * defObject -- JSON object returned from CreateDef; optional if defURI is provided
            * defURI -- URI of pre-existing import/export definition; optional if defObject is provided
            * limit -- max number of records to retrieve (Eloqua max = 50,000)

        """
        if ('uri' not in defObject):
            if (len(defURI)==0):
                raise Exception("Must include a valid defObject or defURI")
            else:
                uri = defURI
        else:
            uri = defObject['uri']

        offset = 0

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

    def PostSyncData(self, data, defObject={}, defURI='', maxPost=20000, syncCount=80000):

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

        while (hasMore):
            for x in range(offset, min(offset+maxPost, dataLen), 1):
                sendSet.append(data[x])

            req = requests.post(url, data = json.dumps(sendSet), headers = POST_HEADERS, auth = self.auth)

            if req.status_code == 204:

                syncOffset += maxPost

                if (syncOffset >= syncCount or offset+maxPost>=dataLen):
                    syncOffset = 0
                    importSync = self.CreateSync(defObject=defObject, defURI=defURI)
                    syncStatus = self.CheckSyncStatus(syncObject=importSync)

                if offset+maxPost>=dataLen:
                    hasMore = False
                    return 'success'
                else:
                    offset += maxPost
                    sendSet = []
            else:
                raise Exception(req.json()['failures'][0]) #### TODO: Fix this error handling
