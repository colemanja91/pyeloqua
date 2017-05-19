"""
Use the Form object to export form data via REST API
Use case: working with small batches of Form Submission data, or
close-to-realtime data pulls
For large batches, or data pulls that do not need to be close-to-realtime, use
Bulk API.
"""

from datetime import datetime
from pyeloqua import Form

# Initialize form class
# parameter form_id can be found by looking at the URL within the Eloqua UI:
# EX.
# https://secure.p01.eloqua.com/Main.aspx#forms&id=1234
# Here, our form_id=1234
FORM = Form(company='mycompany', username='myusername', password='mypassword',
            form_id=1234)

# write out form for later use
# If planning to use this functionality in an automated process, you should write
# out and load the form definition to/from a flat json file
# This saves on API calls, which are limited by Eloqua

FORM.write_form('/my/directory/my_form.json')

# to load it back in later:

FORM = Form(company='mycompany', username='myusername', password='mypassword',
            form_path='/my/directory/my_form.json')


# REST API uses unixtime, so we need to set our datetime parameters then convert
# In production use, these would be some sort of parameter set by our program
# NOTE: this particular conversion method only works in Python 3.X
START = datetime(2017, 5, 19, 7, 00, 00)
END = datetime(2017, 5, 19, 7, 30, 00)

# First, let's get the count of form submit records available
COUNT = FORM.get_count(start=START.timestamp(), end=END.timestamp())

print(COUNT) # show count of form submits

# Now export individual rows
DATA = FORM.get_data(start=START.timestamp(), end=END.timestamp())

# look at output form submissions
for row in DATA:
    print(DATA)
