""" Example: Export a set of contacts through the Bulk API """

# Import python packages
from pyeloqua import Bulk # Load in the Bulk class from pyeloqua


# Setup our bulk "session"

bulk = Bulk(company='mycompany', username='myusername', password='mypassword')

# Setup a new export job

bulk.exports('contacts')

# list out what contact fields we want

field_set = ['C_EmailAddress', 'contactID', 'createdAt', 'C_FirstName',
             'isSubscribed', 'isBounced']

# we could get the same set of fields like this:

field_set = ['Email Address', 'contactID', 'createdAt', 'First Name',
             'isSubscribed', 'isBounced']

# Now add them to our job

bulk.add_fields(field_set)

# Add a filter which will only give us contacts in our segment (using the ID from the segment URL)

bulk.asset_exists('segments', asset_id=12345)

# we could also get it like this, assuming the segment name is 'My Segment':

bulk.asset_exists('segments', name='My Segment')

# Now we're ready to export the data

bulk.create_def('my export')

bulk.sync() # creates a sync which tells Eloqua to prepare the data

contact_records = bulk.get_export_data() # retrieve the prepared data

# Let's take a look at our data:

for contact in contact_records:
    print(contact)
