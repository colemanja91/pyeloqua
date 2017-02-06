""" Bulk API class """
from __future__ import print_function
from copy import deepcopy

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
        """ set job_type to imports """
        if elq_object in OBJECT_REQ_ID and obj_id is None:
            raise Exception('cdo_id required for customobjects')
        self.job['job_type'] = job_type
        self.job['elq_object'] = elq_object
        self.job['obj_id'] = obj_id
