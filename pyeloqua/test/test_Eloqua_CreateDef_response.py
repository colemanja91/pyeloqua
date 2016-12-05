export_activity = {
    "name":"test",
    "fields":{
        "ActivityId":"{{Activity.Id}}"
    },
    "filter":"'{{Activity.Type}}'='EmailSend'",
    "dataRetentionDuration":"P7D",
    "uri":"/activities/exports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}

export_contacts = {
    "name": "test",
    "fields": {
        "EmailAddress": "{{Contact.Field(C_EmailAddress)}}"
    },
    "dataRetentionDuration": "P7D",
    "uri": "/contacts/exports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}
