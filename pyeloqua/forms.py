""" Forms class (via REST) """
from __future__ import print_function
from datetime import datetime
from copy import deepcopy
from json import dumps, dump, load
import requests

from .pyeloqua import Eloqua
from .error_handling import _elq_error_, EloquaBulkSyncTimeout

############################################################################
# Constant definitions
############################################################################

POST_HEADERS = {'Content-Type': 'application/json'}

############################################################################
# Form class
############################################################################

class Form(Eloqua):
    """ Extension for Form operations via REST API """

    def __init__(self, form_id, username=None, password=None, company=None,
                 test=False):
        """
        Initialize form class:

        Arguments:
        :param int form_id: Eloqua Form ID
        :param string username: Eloqua username
        :param string password: Eloqua password
        :param string company: Eloqua company instance
        :param bool test: Sets up test instance; does not connect to Eloqua
        :return: Bulk object
        """
        Eloqua.__init__(self, username, password, company, test)
        self.form_id = form_id
        self.schema = self._get_form(form_id)


    def _get_form(self, form_id):
        """ retrieve complete form definition """

        url = self.rest_base + '/assets/form/{id}?depth=complete'.format(
            id=form_id
        )

        req = requests.get(url, auth=self.auth)

        return req.json()


    def _get_fields(self):
        """ get id-to-field mapping """
        fmap = {}
        for field in self.schema['elements']:
            fmap[field['id']] = field['htmlName']

        return fmap


    def _load_form(self, form_path):
        """ load form definition from json file """


    def write_form(self, form_path):
        """ write form definition to json file """


    def parse_data(self, data):
        """ parse data set to pythonic list of dict """

        #


    def get_data(self, start, end):
        """
        retrieve form submission data

        :param datetime start: filter start datetime
        :param datetime end: filter end datetime
        """

        url = self.rest_base + '/data/form/{id}?startAt={start}&endAt={end}&page={page}'

        has_more = True
        page = 1
        results = []

        while has_more:

            url_page = url.format(
                id=self.form_id,
                start=start,
                end=end,
                page=page
            )

            req = requests.get(url_page, auth=self.auth)

            results.append(self.parse_data(req.json()))

            page += 1
            has_more = len(results) < req.json()['total']

        return results
