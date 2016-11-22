from nose.tools import *
from mock import patch, Mock
from pyeloqua import Eloqua

# Test basic functions around Eloqua class
@raises(Exception)
def test_EloquaInit_MissingUsername():
    elq = Eloqua(company = 'test', password = 'test')

@raises(Exception)
def test_EloquaInit_MissingCompany():
    elq = Eloqua(username = 'test', password = 'test')

@raises(Exception)
def test_EloquaInit_MissingPassword():
    elq = Eloqua(company = 'test', username = 'test')
