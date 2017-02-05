""" utility functions for Eloqua APIs """

def _exception_hander_(status_code, json=None):
    """ serve up EloquaException based on status code """

    if status_code == 503:
        raise Exception('There was a timeout processing the request')
