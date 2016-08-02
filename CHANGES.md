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
