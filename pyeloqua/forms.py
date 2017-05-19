""" Forms class (via REST) """
from json import dump, load
import requests

from .pyeloqua import Eloqua
from .error_handling import _elq_error_

############################################################################
# Constant definitions
############################################################################

POST_HEADERS = {'Content-Type': 'application/json'}

############################################################################
# Form class
############################################################################


class Form(Eloqua):
    """ Extension for Form operations via REST API """

    def __init__(self, username=None, password=None, company=None,
                 test=False, form_id=None, form_path=None):
        """
        Initialize form class:

        Arguments:
        :param string username: Eloqua username
        :param string password: Eloqua password
        :param string company: Eloqua company instance
        :param bool test: Sets up test instance; does not connect to Eloqua
        :param int form_id: Eloqua Form ID; optional
        :param string form_path: Path to JSON file with Eloqua Form definition
        :return: Forms object
        """
        Eloqua.__init__(self, username, password, company, test)

        if form_id is None and form_path is None:
            raise ValueError('One of form_id or form_path is required')
        elif form_id is not None:
            self.form_id = form_id
            self.schema = self._get_form()
        elif form_path is not None:
            self.schema = self._load_form(form_path)
            self.form_id = self.schema['id']

        self.fields = self._get_fields()

    def _get_form(self):
        """ retrieve complete form definition """

        url = self.rest_base + 'assets/form/{id}?depth=complete'.format(
            id=self.form_id
        )

        req = requests.get(url=url, auth=self.auth)

        _elq_error_(req)

        return req.json()

    def _get_fields(self):
        """ get id-to-field mapping """
        fmap = {}
        # using this infernal if/then structure because more than fields are
        # included in 'elements'
        for field in self.schema['elements']:
            if isinstance(field, dict):
                if 'type' in field and field['type'] == 'FormField':
                    fmap[field['id']] = field['htmlName']

        return fmap

    def _load_form(self, form_path):
        """ load form definition from json file """

        return load(open(form_path, 'r'))

    def write_form(self, form_path):
        """ write form definition to json file """

        dump(self.schema, open(form_path, 'w'))

    def _parse_data(self, data):
        """ parse data set to pythonic list of dict """

        out_data = []

        for row in data:

            prow = {}

            for field in row['fieldValues']:

                if 'value' in field.keys():

                    prow[self.fields[field['id']]] = field['value']

            prow['id'] = row['id']
            prow['submittedAt'] = row['submittedAt']

            out_data.append(prow)

        return out_data


    def get_count(self, start, end):
        """
        retrieve count of form submissions

        :param datetime start: filter start unixtime
        :param datetime end: filter end unixtime
        """

        url = self.rest_base + \
            'data/form/{id}?startAt={start}&endAt={end}&count=1'.format(
                id=self.form_id,
                start=start,
                end=end
            )

        req = requests.get(url=url, auth=self.auth)

        _elq_error_(req)

        return req.json()['total']


    def get_data(self, start, end):
        """
        retrieve form submission data

        :param datetime start: filter start unixtime
        :param datetime end: filter end unixtime
        """

        url = self.rest_base + \
            'data/form/{id}?startAt={start}&endAt={end}&page={page}'

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

            req = requests.get(url=url_page, auth=self.auth)

            _elq_error_(req)

            results.extend(self._parse_data(req.json()['elements']))

            page += 1
            has_more = len(results) < req.json()['total']

        return results
