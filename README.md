# AppDev---HackChallenge2021
## API Specification
### Base Endpoint: 

### 1) Register User


<code>POST</code> /api/register/

Request
```
{
  "name": <USER INPUT>,
  "password": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [],
      "public_lists": []
    }
  ]
}
```

### 2) Login

<code>POST</code> /api/login/

Request
```
{
  "name": <USER INPUT>,
  "password": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIENDS>],
      "public_lists": [<SERIALIZED PUBLIC LISTS>]
    }
  ]
}
```

### 3) Get Friends List

<code>GET</code> /api/{id}/friends_lists/

Response
```
{
  "success": true,
  "data": [
    {
      "friends": [<SERIALIZED FRIENDS>]
    }
  ]
}
```

### 4) Get All the User's Lists

<code>GET</code> /api/{id}/lists/

Response
```
{
  "success": true,
  "data": [
    {
      "lists": [<SERIALIZED LISTS>]
    }
  ]
}
```

### 5) Get User's List by List ID

<code>GET</code> /api/{id}/lists/{list_id}/

Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
     "list_name": <USER INPUT>, 
     "is_public": <USER INPUT>,
     "events": [<SERIALIZED EVENTS>]    
     }
  ]
}
```

### 6) Create a List

<code>POST</code> /api/{int}/lists/

Request
```
{
  "list_name": <USER INPUT>,
  "is_public": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
     "list_name": <USER INPUT>, 
     "is_public": <USER INPUT>,
     "events": []
    }
  ]
}
```

### 7) Get Event from Specific List by ID

<code>GET</code> /api/{id}/lists/{list_id}/events/{event_id}/

Response
```
{
  "success": true,
  "data": [
    {
     "id": <ID>,
      "company": <COMPANY>,
      "position": <POSITION>,
      "reminder": <REMINDER>
    }
  ]
}
```

### 8) Edit Specific Event's Details

<code>POST</code> /api/{id}/lists/{list_id}/events/{event_id}/

Request
```
{
  "company": <USER INPUT>,
  "position": <USER INPUT>,
  "reminder": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "company": <COMPANY>,
      "position": <POSITION>,
      "reminder": <REMINDER>    
    }
  ]
}
```

### 9) Add a Friend
Send a friend request to the user whose ID is in the body.

<code>POST</code> /api/{id}/friends/add/

Request
```
{
  "id": <USER INPUT>
}
```
Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIENDS>],
      "public_lists": [<SERIALIZED PUBLIC LISTS>]
    }
  ]
}
```

### 10) Accept Friend Request from Friend ID

<code>POST</code> /api/{id}/friends/accept/{friend_id}/

Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIENDS>],
      "public_lists": [<SERIALIZED PUBLIC LISTS>]
    }
  ]
}
```

### 11) Reject Friend Request from Friend ID

<code>POST</code> /api/{id}/friends/reject/{friend_id}/

Response
```
{
  "success": true,
  "data": [
    {
      "id": <ID>,
      "name": <NAME>,
      "friends": [<SERIALIZED FRIENDS>],
      "public_lists": [<SERIALIZED PUBLIC LISTS>]
    }
  ]
}
```
