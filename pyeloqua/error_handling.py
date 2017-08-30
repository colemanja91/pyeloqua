""" generalized error handling """

def _elq_error_(request):
    """
    Deal with error codes on requests
    Eloqua serves 400 on validation errors; otherwise, general Exception
    is good enough

    :param Request request: object output from Requests
    """

    # deal with validation errors
    if request.status_code == 400:
        try:
            content = request.json()
        except Exception: # pylint: disable=broad-except
            content = request.text

        raise EloquaValidationError(request.status_code, content)

    if request.status_code >= 500:
        raise EloquaServerError(request.status_code)

    else:

        request.raise_for_status()

class EloquaSyncError(Exception):
    """ error on Eloqua Bulk Sync """
    pass

class EloquaBulkSyncTimeout(Exception):
    """ Exception class for Bulk sync timeouts """
    pass

class EloquaValidationError(Exception):
    """ Exception class for 400 errors """
    pass

class EloquaServerError(Exception):
    """ Exception class for 5xx errors """
    pass
