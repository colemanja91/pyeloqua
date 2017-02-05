""" test exception handler """

from nose.tools import raises
from pyeloqua.util import _exception_hander_

###############################################################################
## Define test variables
###############################################################################

def test_except_valid():
    """ ensure that 200-300 range codes pass """
    assert _exception_hander_(200) is None

@raises(Exception)
def test_except_503():
    """ error raised on timeout """
    _exception_hander_(503)
