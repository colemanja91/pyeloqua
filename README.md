# pyeloqua

Python wrapper functions for Eloqua APIs, tested with Python 2.7, 3.3, and 3.4.

Documentation is your friend (http://docs.oracle.com/cloud/latest/marketingcs_gs/OMCAB/index.html) - if you can't do it in the API, you can't do it with this module.

**What can the API do?** The Eloqua APIs are for the import and export of data from an existing Eloqua instance.

# Examples
## Getting started

You need an Eloqua user account with at least *Advanced Marketing User* or *API User* permissions.

Sessions are managed through the `Eloqua` class:

```
from pyeloqua import Eloqua

elq = Eloqua(company='MyCompany', username='user', password='password')

```

# Feature requests

To request a new feature in this package, please open a new issue on the Github repo.
