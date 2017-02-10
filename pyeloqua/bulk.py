""" Bulk API class """
from __future__ import print_function
from copy import deepcopy
import requests

from .pyeloqua import Eloqua
from .system_fields import ACTIVITY_FIELDS

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

    def reset(self):
        """ reset job """
        self.job = deepcopy(BLANK_JOB)

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

    def get_fields(self):
        """
        retrieve all fields for specified Eloqua object in job setup;
        useful if unsure what fields are available

        Arguments:

        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        :return list: field definitions
        """
        # handle activity fields
        if self.job['elq_object'] == 'activities':
            return ACTIVITY_FIELDS[self.job['act_type']]

        if self.job['elq_object'] in OBJECT_REQ_ID:
            url_base = self.bulk_base + '/{obj}/{id}/fields?limit=1000'.format(
                obj=self.job['elq_object'],
                id=self.job['obj_id']
            )
            url_base += '&offset={offset}'
        else:
            url_base = self.bulk_base + '/{obj}/fields?limit=1000'.format(
                obj=self.job['elq_object']
            )
            url_base += '&offset={offset}'

        fields = []

        has_more = True

        offset = 0

        while has_more:
            url = url_base.format(offset=offset)
            req = requests.get(url=url, auth=self.auth)
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

        fields_output = []

        for field_name in field_input:
            match = False
            for field in fields:
                if field_name == field['internalName'] or field_name == field['name']:
                    fields_output.append(field)
                    match = True
            if not match:
                raise Exception('field not found: %s' % field_name)

        self.job['fields'].extend(fields_output)
