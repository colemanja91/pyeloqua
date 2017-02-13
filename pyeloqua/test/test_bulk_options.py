""" Eloqua.Bulk setup methods (add job options) """

from nose.tools import raises
from mock import patch, Mock

from pyeloqua import Bulk

###############################################################################
# Constants
###############################################################################



###############################################################################
# Add some options!
###############################################################################

def test_option_add():
    """ add a random option """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_options(identifierFieldName='C_EmailAddress')
    assert bulk.job['options']['identifierFieldName'] == 'C_EmailAddress'


def test_option_add_all():
    """ add several random options """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_options(identifierFieldName='C_EmailAddress',
                     areSystemTimestampsInUTC=True)
    assert len(bulk.job['options']) == 2

###############################################################################
# Add some sync actions!!
###############################################################################

def test_syncact_add():
    """ add sync action with specified destination and action """
    bulk = Bulk(test=True)
    bulk.exports('contacts')
    bulk.add_syncaction(action='add',
                        destination='{{ContactList[12345]}}')
    bulk.job['options']['syncActions'][0] = {
        "action": "add",
        "destination": "{{ContactList[12345]}}"
    }
