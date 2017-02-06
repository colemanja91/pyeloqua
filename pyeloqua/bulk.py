""" Bulk API class """

from .pyeloqua import Eloqua

############################################################################
# Constant definitions
############################################################################

POST_HEADERS = {'Content-Type': 'application/json'}

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

    class Import(object):
        """ Extension to deal with Bulk Imports """

        def __init__(self, )
