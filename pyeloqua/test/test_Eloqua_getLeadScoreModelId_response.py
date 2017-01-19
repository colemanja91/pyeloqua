leadScoreModelResultOne = {
  "items": [
    {
      "name": "test",
      "status": "Active",
      "id": 1,
      "fields": [
        {
          "name": "Rating",
          "statement": "{{Contact.LeadScore.Model[1].Rating}}",
          "dataType": "string"
        },
        {
          "name": "ProfileScore",
          "statement": "{{Contact.LeadScore.Model[1].ProfileScore}}",
          "dataType": "number"
        },
        {
          "name": "EngagementScore",
          "statement": "{{Contact.LeadScore.Model[1].EngagementScore}}",
          "dataType": "number"
        }
      ],
      "uri": "/contacts/scoring/models/1",
      "createdBy": "Test.User",
      "updatedBy": "Test.User",
      "createdAt": "2015-12-04T16:16:37.2570000Z",
      "updatedAt": "2016-04-18T18:59:55.6570000Z"
    }
  ],
  "totalResults": 1,
  "limit": 1000,
  "offset": 0,
  "count": 1,
  "hasMore": False
}

leadScoreModelResultNone = {
  "items": [],
  "totalResults": 0,
  "limit": 1000,
  "offset": 0,
  "count": 0,
  "hasMore": False
}

leadScoreModelResultMany = {
  "items": [
    {
      "name": "test",
      "status": "Active",
      "id": 1,
      "fields": [
        {
          "name": "Rating",
          "statement": "{{Contact.LeadScore.Model[1].Rating}}",
          "dataType": "string"
        },
        {
          "name": "ProfileScore",
          "statement": "{{Contact.LeadScore.Model[1].ProfileScore}}",
          "dataType": "number"
        },
        {
          "name": "EngagementScore",
          "statement": "{{Contact.LeadScore.Model[1].EngagementScore}}",
          "dataType": "number"
        }
      ],
      "uri": "/contacts/scoring/models/1",
      "createdBy": "Test.User",
      "updatedBy": "Test.User",
      "createdAt": "2015-12-04T16:16:37.2570000Z",
      "updatedAt": "2016-04-18T18:59:55.6570000Z"
    },
    {
      "name": "test2",
      "status": "Active",
      "id": 2,
      "fields": [
        {
          "name": "Rating",
          "statement": "{{Contact.LeadScore.Model[2].Rating}}",
          "dataType": "string"
        },
        {
          "name": "ProfileScore",
          "statement": "{{Contact.LeadScore.Model[2].ProfileScore}}",
          "dataType": "number"
        },
        {
          "name": "EngagementScore",
          "statement": "{{Contact.LeadScore.Model[2].EngagementScore}}",
          "dataType": "number"
        }
      ],
      "uri": "/contacts/scoring/models/2",
      "createdBy": "Test.User",
      "updatedBy": "Test.User",
      "createdAt": "2015-12-04T16:16:37.2570000Z",
      "updatedAt": "2016-04-18T18:59:55.6570000Z"
    }
  ],
  "totalResults": 1,
  "limit": 1000,
  "offset": 0,
  "count": 1,
  "hasMore": False
}
