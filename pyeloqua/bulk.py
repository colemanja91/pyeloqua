""" Bulk API class """
from __future__ import print_function
from copy import deepcopy
import requests

from .pyeloqua import Eloqua

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
    'options': {}
}

OBJECT_REQ_ID = ['customobjects', 'events']

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
        """
        Eloqua.__init__(self, username, password, company, test)
        self.job = deepcopy(BLANK_JOB)

    def reset(self):
        """ reset job """
        self.job = deepcopy(BLANK_JOB)

    def _setup_(self, job_type, elq_object, obj_id=None):
        """
        setup a job

        Arguments:

        :param string job_type: 'imports' or 'exports'
        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        """
        if elq_object not in ELQ_OBJECTS:
            raise Exception('invalid elq_object \'$s\'' % elq_object)
        # check if requires obj_id
        if elq_object in OBJECT_REQ_ID and obj_id is None:
            raise Exception('obj_id required for \'%s\'' % elq_object)

        self.job['job_type'] = job_type
        self.job['elq_object'] = elq_object
        self.job['obj_id'] = obj_id

    def imports(self, elq_object, obj_id=None):
        """
        setup a job with job_type == 'imports'

        Arguments:

        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        """
        self._setup_(job_type='imports', elq_object=elq_object, obj_id=obj_id)

    def exports(self, elq_object, obj_id=None):
        """
        setup a job with job_type == 'exports'

        Arguments:

        :param string elq_object: target Eloqua object
        :param int obj_id: parent ID for events or customobjects
        """
        self._setup_(job_type='exports', elq_object=elq_object, obj_id=obj_id)

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
        """

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
