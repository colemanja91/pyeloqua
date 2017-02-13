""" Bulk API class """
from __future__ import print_function
from datetime import datetime
from copy import deepcopy
from json import dumps
import requests

from .pyeloqua import Eloqua
from .system_fields import ACTIVITY_FIELDS, CONTACT_SYSTEM_FIELDS, ACCOUNT_SYSTEM_FIELDS
from .error_handling import _elq_error_

############################################################################
# Constant definitions
############################################################################

POST_HEADERS = {'Content-Type': 'application/json'}

BLANK_JOB = {
    'filters': [],
    'fields': [],
    'job_type': None,
    'elq_object': None,
    'obj_id': None,
    'act_type': None,
    'options': {}
}

OBJECT_REQ_ID = ['customobjects', 'events']

OBJECT_REQ_TYPE = ['activities']

ELQ_OBJECTS = ['accounts', 'activities', 'contacts', 'customobjects',
               'emailaddresses', 'events']

############################################################################
# Bulk class
############################################################################


class Bulk(Eloqua):
    """ Extension for Bulk API operations """

    def __init__(self, username=None, password=None, company=None, test=False):
        """
        Initialize bulk class:

        Arguments:

        :param string username: Eloqua username
        :param string password: Eloqua password
        :param string company: Eloqua company instance
        :param bool test: Sets up test instance; does not connect to Eloqua
        :return: Bulk object
        """
        Eloqua.__init__(self, username, password, company, test)
        self.job = deepcopy(BLANK_JOB)
        self.job_def = {}

    def reset(self):
        """ reset job """
        self.job = deepcopy(BLANK_JOB)
        self.job_def = {}

    def _setup_(self, job_type, elq_object, obj_id=None, act_type=None):
        """
        setup a job

        Arguments:

        :param string job_type: 'imports' or 'exports'
        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        :param string act_type: Activity type
        """
        if elq_object not in ELQ_OBJECTS:
            raise Exception('invalid elq_object \'$s\'' % elq_object)
        # check if requires obj_id
        if elq_object in OBJECT_REQ_ID and obj_id is None:
            raise Exception('obj_id required for \'%s\'' % elq_object)
        if elq_object in OBJECT_REQ_TYPE and act_type is None:
            raise Exception('act_type required for \'%s\'' % elq_object)

        self.job['job_type'] = job_type
        self.job['elq_object'] = elq_object
        self.job['obj_id'] = obj_id
        self.job['act_type'] = act_type

    def imports(self, elq_object, obj_id=None, act_type=None):
        """
        setup a job with job_type == 'imports'

        Arguments:

        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        :param string act_type: Activity type
        """
        self._setup_(job_type='imports', elq_object=elq_object, obj_id=obj_id,
                     act_type=act_type)

    def exports(self, elq_object, obj_id=None, act_type=None):
        """
        setup a job with job_type == 'exports'

        Arguments:

        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        :param string act_type: Activity type
        """
        self._setup_(job_type='exports', elq_object=elq_object, obj_id=obj_id,
                     act_type=act_type)

    ###########################################################################
    # Helper methods
    ###########################################################################

    def get_fields(self, elq_object=None, obj_id=None, act_type=None):
        """
        retrieve all fields for specified Eloqua object in job setup;
        useful if unsure what fields are available

        Arguments:

        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        :param string act_type: Activity type
        :return list: field definitions
        """
        # handle inputs vs Bulk.job
        if elq_object is None:
            elq_object = self.job['elq_object']
            obj_id = self.job['obj_id']
            act_type = self.job['act_type']
        # handle activity fields
        if elq_object == 'activities':
            return ACTIVITY_FIELDS[act_type]

        if elq_object in OBJECT_REQ_ID:
            url_base = self.bulk_base + '/{obj}/{id}/fields?limit=1000'.format(
                obj=elq_object,
                id=obj_id
            )
            url_base += '&offset={offset}'
        else:
            url_base = self.bulk_base + '/{obj}/fields?limit=1000'.format(
                obj=elq_object
            )
            url_base += '&offset={offset}'

        if elq_object == 'contacts':
            fields = deepcopy(CONTACT_SYSTEM_FIELDS)
        elif elq_object == 'accounts':
            fields = deepcopy(ACCOUNT_SYSTEM_FIELDS)
        else:
            fields = []

        has_more = True

        offset = 0

        while has_more:
            url = url_base.format(offset=offset)
            req = requests.get(url=url, auth=self.auth)
            _elq_error_(req)
            fields.extend(req.json()['items'])
            offset += 1
            has_more = req.json()['hasMore']

        return fields

    def add_fields(self, field_input=None):
        """
        retrieve all specified fields and add to job setup

        Arguments:

        :param list field_input: fields to add by DB name or Display Name
        """

        fields = self.get_fields()

        if field_input is None:
            self.job['fields'].extend(fields)
            return True

        fields_output = fields_intersect(fields, field_input)

        self.job['fields'].extend(fields_output)


    def add_linked_fields(self, lnk_obj, field_input):
        """
        add fields from linked objects

        :param string lnk_obj: linked object
        :param list field_input: fields to add by name
        """

        fields = self.get_fields(elq_object=lnk_obj)

        fields_output = fields_intersect(fields, field_input)

        for field in fields_output:
            if lnk_obj == 'contacts':
                if self.job['elq_object'] == 'customobjects':
                    field['statement'] = field['statement'].replace(
                        'Contact.', 'CustomObject[%s].Contact.' % self.job['obj_id'])
                elif self.job['elq_object'] == 'events':
                    field['statement'] = field['statement'].replace(
                        'Contact.', 'Event[%s].Contact.' % self.job['obj_id'])
            elif lnk_obj == 'accounts':
                field['statement'] = field['statement'].replace(
                    'Account.', 'Contact.Account.')

        self.job['fields'].extend(fields_output)

    def add_leadscore_fields(self, model_id=None, name=None):
        """
        add fields from a lead score model

        :param string name: name of lead score model
        :param int model_id: id of lead score model
        """

        if model_id is not None:
            url = self.bulk_base + \
                '/contacts/scoring/models/{0}'.format(model_id)
            req = requests.get(url=url, auth=self.auth)
            _elq_error_(req)

            self.job['fields'].extend(req.json()['fields'])
        elif name is not None:
            url = self.bulk_base + \
                '/contacts/scoring/models?q="name={name}"'.format(
                    name=name.replace(' ', '*'))
            req = requests.get(url=url, auth=self.auth)
            _elq_error_(req)

            self.job['fields'].extend(req.json()['items'][0]['fields'])
        else:
            raise Exception('model_id or name required')

    def asset_exists(self, asset, asset_id=None, name=None):
        """
        add filter statement for asset

        :param string asset: Eloqua asset type: lists, segments, filters
        :param int asset_id: id of asset
        :param string name: name of asset
        """

        exists_temp = " EXISTS('{statement}') "

        if asset_id is not None:
            url = self.bulk_base + '/{obj}/{asset}/{asset_id}'.format(
                obj=self.job['elq_object'],
                asset=asset,
                asset_id=asset_id
            )

            req = requests.get(url=url, auth=self.auth)

            _elq_error_(req)

            self.job['filters'].append(exists_temp.format(
                statement=req.json()['statement']))
        elif name is not None:
            url = self.bulk_base + '/{obj}/{asset}?q="name={name}"'.format(
                obj=self.job['elq_object'],
                asset=asset,
                name=name.replace(' ', '*')
            )

            req = requests.get(url=url, auth=self.auth)

            _elq_error_(req)

            self.job['filters'].append(exists_temp.format(
                statement=req.json()['items'][0]['statement']))
        else:
            raise Exception('asset_id or name required')

    def filter_date(self, field, start=None, end=None):
        """
        add a filter by start or end date

        :param string field: Field name on which to filter
        :param string start: Datetime string for date >=
        :param string end: Datetime string for date <=
        :param datetime start: Datetime object for date >=
        :param datetime end: Datetime object for date <=
        """

        field_stmt = fields_intersect(self.get_fields(), [field])[0]['statement']

        if start is not None:

            if isinstance(start, str):
                try:
                    datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    raise Exception('invalid start value')
            elif isinstance(start, datetime):
                start = start.strftime('%Y-%m-%d %H:%M:%S')

            filter_str = " '{statement}' >= '{start}' ".format(
                statement=field_stmt,
                start=start
            )
        elif end is not None:

            if isinstance(end, str):
                try:
                    datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    raise Exception('invalid end value')
            elif isinstance(end, datetime):
                end = end.strftime('%Y-%m-%d %H:%M:%S')

            filter_str = " '{statement}' <= '{end}' ".format(
                statement=field_stmt,
                end=end
            )

        self.job['filters'].append(filter_str)

    def filter_equal(self, field, value):
        """
        add filter statement for field equals value

        :param string field: Field name on which to filter
        :param string value: Field value
        """

        field_stmt = fields_intersect(self.get_fields(), [field])[0]['statement']

        filter_str = " '{statement}' = '{value}' ".format(
            statement=field_stmt,
            value=value
        )

        self.job['filters'].append(filter_str)

    def create_def(self, name):
        """
        create an import definition based on current object attributes

        :param str name: name of import/export definition
        """

        if self.job['elq_object'] in OBJECT_REQ_ID:
            url = self.bulk_base + '/{obj}/{id}/{job_type}'.format(
                obj=self.job['elq_object'],
                id=self.job['obj_id'],
                job_type=self.job['job_type']
            )
        else:
            url = self.bulk_base + '/{obj}/{job_type}'.format(
                obj=self.job['elq_object'],
                job_type=self.job['job_type']
            )

        req_data = {
            'name': name,
            'fields': {},
            'filters': 'AND'.join(self.job['filters'])
        }

        for field in self.job['fields']:
            if 'internalName' in field.keys():
                req_data['fields'][field['internalName']] = field['statement']
            else:
                req_data['fields'][field['name']] = field['statement']

        req = requests.post(url=url, auth=self.auth, data=dumps(req_data))

        _elq_error_(req)


###############################################################################
# Helper functions
###############################################################################

def fields_intersect(field_set, field_input):
    """ Return field set given input set of names and input set of fields """
    fields_output = []

    for field_name in field_input:
        match = False
        for field in field_set:
            if 'internalName' in field.keys():
                if field_name == field['internalName'] or field_name == field['name']:
                    fields_output.append(field)
                    match = True
            else:
                if field_name == field['name']:
                    fields_output.append(field)
                    match = True
        if not match:
            raise Exception('field not found: %s' % field_name)

    return fields_output
