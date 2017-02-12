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

        raise Exception(request.status_code, content)

    else:

        request.raise_for_status()
