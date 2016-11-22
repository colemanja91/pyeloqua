contactFieldsResponse = {
  "items": [
    {
      "name": "Email Address",
      "internalName": "C_EmailAddress",
      "dataType": "emailAddress",
      "hasReadOnlyConstraint": False,
      "hasNotNullConstraint": False,
      "hasUniquenessConstraint": True,
      "statement": "{{Contact.Field(C_EmailAddress)}}",
      "uri": "/contacts/fields/100001",
      "createdAt": "1900-01-01T05:00:00.0000000Z",
      "updatedBy": "testing.mctestface",
      "updatedAt": "2011-01-01T08:00:00.0000000Z"
    },
    {
      "name": "First Name",
      "internalName": "C_FirstName",
      "dataType": "string",
      "hasReadOnlyConstraint": False,
      "hasNotNullConstraint": False,
      "hasUniquenessConstraint": False,
      "statement": "{{Contact.Field(C_FirstName)}}",
      "uri": "/contacts/fields/100002",
      "createdAt": "1900-01-01T05:00:00.0000000Z",
      "updatedBy": "testing.mctestface",
      "updatedAt": "2011-01-01T08:00:00.0000000Z"
    },
    {
      "name": "Last Name",
      "internalName": "C_LastName",
      "dataType": "string",
      "hasReadOnlyConstraint": False,
      "hasNotNullConstraint": False,
      "hasUniquenessConstraint": False,
      "statement": "{{Contact.Field(C_LastName)}}",
      "uri": "/contacts/fields/100003",
      "createdAt": "1900-01-01T05:00:00.0000000Z",
      "updatedBy": "testing.mctestface",
      "updatedAt": "2011-01-01T08:00:00.0000000Z"
    },
    {
      "name": "Company",
      "internalName": "C_Company",
      "dataType": "string",
      "hasReadOnlyConstraint": False,
      "hasNotNullConstraint": False,
      "hasUniquenessConstraint": False,
      "statement": "{{Contact.Field(C_Company)}}",
      "uri": "/contacts/fields/100004",
      "createdAt": "1900-01-01T05:00:00.0000000Z",
      "updatedBy": "testing.mctestface",
      "updatedAt": "2011-01-01T08:00:00.0000000Z"
    }
 ]
}

contactFieldsResult = [
  {
    "name": "Email Address",
    "internalName": "C_EmailAddress",
    "dataType": "emailAddress",
    "hasReadOnlyConstraint": False,
    "hasNotNullConstraint": False,
    "hasUniquenessConstraint": True,
    "statement": "{{Contact.Field(C_EmailAddress)}}",
    "uri": "/contacts/fields/100001",
    "createdAt": "1900-01-01T05:00:00.0000000Z",
    "updatedBy": "testing.mctestface",
    "updatedAt": "2011-01-01T08:00:00.0000000Z"
  },
  {
    "name": "First Name",
    "internalName": "C_FirstName",
    "dataType": "string",
    "hasReadOnlyConstraint": False,
    "hasNotNullConstraint": False,
    "hasUniquenessConstraint": False,
    "statement": "{{Contact.Field(C_FirstName)}}",
    "uri": "/contacts/fields/100002",
    "createdAt": "1900-01-01T05:00:00.0000000Z",
    "updatedBy": "testing.mctestface",
    "updatedAt": "2011-01-01T08:00:00.0000000Z"
  },
  {
    "name": "Last Name",
    "internalName": "C_LastName",
    "dataType": "string",
    "hasReadOnlyConstraint": False,
    "hasNotNullConstraint": False,
    "hasUniquenessConstraint": False,
    "statement": "{{Contact.Field(C_LastName)}}",
    "uri": "/contacts/fields/100003",
    "createdAt": "1900-01-01T05:00:00.0000000Z",
    "updatedBy": "testing.mctestface",
    "updatedAt": "2011-01-01T08:00:00.0000000Z"
  },
  {
    "name": "Company",
    "internalName": "C_Company",
    "dataType": "string",
    "hasReadOnlyConstraint": False,
    "hasNotNullConstraint": False,
    "hasUniquenessConstraint": False,
    "statement": "{{Contact.Field(C_Company)}}",
    "uri": "/contacts/fields/100004",
    "createdAt": "1900-01-01T05:00:00.0000000Z",
    "updatedBy": "testing.mctestface",
    "updatedAt": "2011-01-01T08:00:00.0000000Z"
  }
]
