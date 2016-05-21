# pyeloqua

Python wrapper functions for Eloqua APIs, tested with Python 2.7, 3.3, and 3.4.

Documentation is your friend (http://docs.oracle.com/cloud/latest/marketingcs_gs/OMCAB/index.html) - if you can't do it in the API, you can't do it with this module.

**What can the API do?** The Eloqua APIs are for the import and export of data from an existing Eloqua instance.

# Examples
## Getting started

You need an Eloqua user account with at least *Advanced Marketing User* or *API User* permissions.

Sessions are managed through the `Eloqua` class:

```python
from pyeloqua import Eloqua
elq = Eloqua(company='MyCompany', username='user', password='password')
```

You can access some basic session info from this object:

```python
elq.siteId ### displays the Eloqua instance Site ID
elq.userId ### displays the current Eloqua user's ID
elq.userDisplay ### Display name of current user
elq.restBase ### Base URL for REST API calls
elq.bulkBase ### Base URL for Bulk API calls
```

The default API version is 2.0, but you can specify a different version on creating an instance. So, to use REST 1.0:

```python
elq = Eloqua(company='MyCompany', username='user', password='password', rest_api_version="1.0")
```

## Exporting contacts

Let's run through a simple example of exporting a set of contacts. Say we have a contact segment, "My Test Segment", that we want to retrieve.
First, we create a filter statement that looks for contacts in our segment:

```python
myFilter = elq.FilterExists(name="My Test Segment", existsType="ContactSegment")
print(myFilter) # "EXISTS('{{ContactSegment[12345]}}')"
```

Then, figure out which fields we want to export. pyeloqua can search for contact, account, and CDO fields by both the "Display Name" seen in your instance and the "Database Name" shown in field setup; also can include system fields (contact ID, created date, subscribe/bounce status), and fields from one lead scoring model.

```python
myFields = elq.CreateFieldStatement(entity='contacts', fields=['Email Address', 'Last Name', 'C_FirstName'],
                                    addSystemFields=['contactID', 'createdAt', 'isSubscribed'],
                                    leadScoreModelId=1)
# returns dictionary of field statements
```

Now we're ready to create an export definition:

```python
myExport = elq.CreateDef(defType='exports', entity='contacts', fields=myFields, filters=myFilter,
                         defName='My Export')
```

then tell the API to start syncing the data into the "staging area" so we can download it, and wait for the sync to finish. The ```CheckSyncStatus``` method with check progress of the sync every 10 seconds until finished, and will raise an exception if there is an error.

```python
mySync = elq.CreateSync(defObject = myExport)
status = elq.CheckSyncStatus(syncObject = mySync)
```

Download the datas!

```python
myData = elq.GetSyncedData(defObject=myExport)
```

# Feature requests

To request a new feature in this package, please open a new issue on the Github repo.
