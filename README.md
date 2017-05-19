# pyeloqua

Python wrapper functions for Eloqua APIs, tested with Python 2.7 and Python 3.3 - 3.6.

Documentation is your friend (http://docs.oracle.com/cloud/latest/marketingcs_gs/OMCAC/index.html) - if you can't do it in the API, you can't do it with this module.

**NOTICE** I'm in the middle of a rebuild that will result in breaking changes to existing uses. This is to facilitate better unit testing and meet coding standards and best practices. Right now, if you upgrade to the latest version (release v0.4.0), you will receive warnings when attempting to use the old methods. After a few minor version releases, when the new code is stabilized, the deprecated code will be removed entirely. Please continue using release v0.3.5 until you have updated your code.

Please feel free to let me know of any problems by filing an issue on Github.

**What can the API do?** The Eloqua APIs are for the import and export of data from an existing Eloqua instance.

# Examples
##Getting started

You need an Eloqua user account with at least *Advanced Marketing User* or *API User* permissions.

To work with the bulk API, we start with the `Bulk` class:

```python
from pyeloqua import Bulk

bulk = Bulk(company='mycompany', username='myusername', password='mypassword')
```

We can even view some basic information about our Eloqua instance:

```python
bulk.site_id # Eloqua site ID
bulk.user_display # Your displayed username
```

To work with small batches of form data, use the `Form` class
*NOTE: for large batches of form data that do not need to be close to realtime,
use Bulk for an Activity export*
```python
from pyeloqua import Form

form = Form(company='mycompany', username='myusername', password='mypassword',
            form_id=1234)
```

## More examples

There are examples in the `/examples` directory:

- Export a segment of contacts (Walkthrough, Code)
- Import a set of contacts (Walkthrough, Code )
- Export a set of event data records
- Import a set of event data records
- Export a set of custom object data records
- Import a set of custom object data records
- Export a set of activity data
- Export form submission data via REST API (with the `Form` class)

## Youtube tutorials

*Coming soon!*

# Feature requests

To request a new feature in this package, please open a new issue on the Github repo.
To report problems, please open a new issue on the Github repo.

# Contribution

Pull requests are welcomed! All pull requests must have the following:
- OK global score from pylint using PEP8 standards
  - This one is a bit loose for now given that the old code is still a mess; once the renovation is complete, we will implement a minimum passing pylint score
- Passing unit tests (`nosetests`) that cover the included use cases and pass the current `tox` config
