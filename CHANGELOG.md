## 2017-02-15 v0.4.0
- MAJOR FEATURE: New `Bulk` class for interacting with Bulk API; see README and examples for more info
- DEPRECATION: Old Bulk API methods in `Eloqua` now give deprecation warnings

## 2017-02-02 v0.3.5
- BUGFIX: fix dependency install by switching around where `__version__` was stored (now in setup.py)
- FEATURE: add `updateRule` optional argument to `CreateDef`

## 2017-01-25 v0.3.4
- FEATURE: add parameter to `Eloqua` class; adding `test=True` creates a dummy instance which can be used in context of other unit testing

## 2017-01-19 v0.3.3
- FEATURE: add method `GetAsset`, which returns dict of asset info (list, filter, and segment)

## 2016-11-17 v0.3.2
- BUGFIX: Now `CreateFieldStatement` works in many circumstances, passing a single field as string, a dict of fields, or a list of fields, or passing a blank value `''` and specifying `addAll=True`
- FEATURE: added `GetAssetSize` method which returns current count of a contact shared list

## 2016-11-14 v0.3.1
- BUGFIX: fixed `CreateFieldStatement`

## 2016-11-01 v0.3.0
- BUGFIX: `CreateFieldStatement` now allows creation of field statements passing only `addSystemContactFields` or `addLinkedContactFields`
- FEATURE: new parameter for `CreateFieldStatement`, `addAll` - adds all fields from entity to output field set (default=`False`)
- FEATURE: new parameter for `CreateFieldStatement`, `addLinkedAccountFields` - adds specified account fields to export of contact data
- FEATURE: `CreateFieldStatement` now allows passing `fields` as a dict, providing custom import/export field names

## 2016-10-07 v0.2.91
- HOTFIX: Set "ensure_ascii" parameter of json.dumps = False and encode = 'utf8'; was causing problems with imports

## 2016-10-06 v0.2.8
- Added exception handling for PostSyncData status codes

## 2016-09-28 v0.2.7
- Added functionality for syncActions in import/export definitions

## 2016-09-20 v0.2.6
- Fixed sync count that gets return in data post

## 2016-09-18 v0.2.5
- Added functionality to export a max # of rows

## 2016-09-15 v0.2.4
- Fixed some issues around code that got changed for form posts

## 2016-08-15 v0.2.2
- Fixed dependency requirement for requests

## 2016-08-02 v0.2.0
- Added export functionality for activities
- Added ability to create field statements for CDO exports that include linked contact fields
- Deprecated ```addSystemFields``` in ```CreateFieldStatement```; begin using ```addSystemContactFields``` instead

## 2016-06-27 v0.1.0
- fixed FilterDateRange to allow for filtering on system fields createdAt, updatedAt, on contacts and accounts

## 2016-06-23 v0.0.9 hotfix
- fixed GetSyncedRecordCount

## 2016-06-17 v0.0.8
- Added sync status to PostSyncData output

## 2016-06-16 v0.0.7
- Added deletion functionality for contact, account, and CDO records
- Improved some inline documentation
- bug fix for GetSyncedRecordCount
- added import sync error handling (GetSyncRejectedRecords)
- updated PostSyncData to output a summary of sync URIs, send count, and reject count

## 2016-06-13 v0.0.5
- hotfix for post data to form (was sending all data as query string params)

## 2016-06-11 v0.0.4
- Added functions for posting data to Eloqua forms
