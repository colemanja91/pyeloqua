contact_addList = {
    "action": "add",
    "destination": "{{ContactList[1]}}"
}

contact_removeList = {
    "action": "remove",
    "destination": "{{ContactList[1]}}"
}

account_addList = {
    "action": "add",
    "destination": "{{AccountList[1]}}"
}

account_removeList = {
    "action": "remove",
    "destination": "{{AccountList[1]}}"
}

AccountListResultOne = {
  "items": [
    {
      "name": "test",
      "count": 0,
      "statement": "{{AccountList[1]}}",
      "uri": "/accounts/lists/1",
      "createdBy": "Test.User",
      "createdAt": "2016-09-28T19:02:39.5330000Z",
      "updatedBy": "Test.User",
      "updatedAt": "2016-11-29T18:31:49.1800000Z"
    }
  ],
  "totalResults": 1,
  "limit": 1000,
  "offset": 0,
  "count": 1,
  "hasMore": False
}

dest_setStatus = {
    "action": "setStatus",
    "status": "no",
    "destination": "{{DecisionInstance(abcdefghijklmnopqrstuvwxyz).Execution[12345]}}"
}
