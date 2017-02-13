""" Eloqua.Bulk job setup methods (create definition) """

from copy import deepcopy
from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################

JOB_GOOD_CONTACTS = {
    'filters': [" '{{Contact.Id}}' = '12345' ",
                " '{{Contact.CreatedAt}}' >= '2017-01-01 00:00:00' "],
    'fields': [],
    'job_type': 'exports',
    'elq_object': 'contacts',
    'obj_id': None,
    'act_type': None,
    'options': {}
}
