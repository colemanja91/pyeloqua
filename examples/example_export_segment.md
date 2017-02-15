# Introduction

This tutorial will show how to use pyeloqua to export a contact segment via the Bulk API.

# Setup

Please follow example_setup.md for instructions on properly setting up Python with pyeloqua.

# Defining an export

## Logging in

Start by calling the `Bulk` object and telling it we are creating a new export:

```python
from pyeloqua import Bulk

# set up a "session" with our Eloqua instance
bulk = Bulk(company='mycompany', username='myusername', password='mypassword')
# specify that we want an export of contact records:
bulk.exports('contacts')
```

## Filter by segment

Now we specify to filter contact records by those only in a particular segment:

```python
bulk.asset_exists('segments', asset_id=12345)
```

The segment ID is in the URL when you open it through the Eloqua interface:

*Note*: you can specify a segment by `name`, but since you can have duplicate segment names in Eloqua, using the ID is safer.

## Add fields

Add the fields that we want. You can do this by the field's display name (what you see in the interface) or by the database name:

```python
field_set = ['C_EmailAddress', 'contactID', 'createdAt', 'C_FirstName']

bulk.add_fields(field_set)
```
In this case, we are adding two *system fields* (`contactID` and `createdAt`) which are always available on the contact. We're also adding two standard contact fields, `C_EmailAddress` and `C_FirstName`.

## Send export definition to Eloqua

Now that we've defined what we want in the export, we pass that along to Eloqua to create an *export definition*:

```python
bulk.create_def('my export') # send export info to Eloqua

print(bulk.job_def) # show on-screen the definition as Eloqua interprets it to make sure it is correct
```

# Getting export data

## Sync export definition

Right now, Eloqua just has a definition of what we want to export - it hasn't actually exported our data yet. To do that, we need to *sync* it to tell Eloqua to prepare the data so we can get it:

```python
bulk.sync()
```

If it works, we should see `success` printed on the screen.

## Retrieve synced data

Now that the data is ready, we can get it!

```python
contact_records = bulk.get_export_data()
```

If we want to look at the first record:

```python
print(contact_records[0])
```

If we want to see *all* the records:

```python
for contact in contact_records:
    print(contact)
```

## Writing the data to a file

Normally, if we're using Python to automate some sort of data process, we won't need to put our data in a "flat file" - we would just process it and re-import back to Eloqua.

If we do need to write it to a file, there are several tutorials online that show how to export to a CSV or JSON file. 
