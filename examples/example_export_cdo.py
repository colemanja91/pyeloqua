""" Example: Export a set of CDO records through Bulk API """

# Import python packages
from pyeloqua import Bulk # Load in the Bulk class from pyeloqua


# Setup our bulk "session"

bulk = Bulk(company='mycompany', username='myusername', password='mypassword')

# Setup a new export job

bulk.exports('customobjects', obj_id=123)

# list out what CDO fields we want

field_set = ['Email Address', 'DatacardExtID', 'First Name']

# filter records to a specific email address

bulk.filter_equal(field='Email Address', value='jecolema@redhat.com')

# Now we're ready to export the data

bulk.create_def('my export')

bulk.sync() # creates a sync which tells Eloqua to prepare the data

cdo_records = bulk.get_export_data() # retrieve the prepared data

# Let's take a look at our data:

for datacard in cdo_records:
    print(datacard)
