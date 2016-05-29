# Api Examples

You can use curl, python's urllib, firebug, etc. for making POST requests.
I will use `curl` for all example requests here since that is simple to use from any shell.
You can pass the `-i` option to `curl` if you want to see more info about the response.

## GETting public info

Make a GET request to [/api/](http://localhost:8000/api/) to get an overview of the questions:

    curl http://localhost:8000/api/

```
[
  {
    "title": "Text Editor",
    "text": "Which text editors do you use?",
    "multivote": true,
    "locked": false,
    "show_count": false,
    "options": [
      "Vim",
      "Sublime",
      "Atom",
      "Notepad++",
      "Other"
    ]
  },
  {
    "title": "Operating System",
    "text": "Which is you favorite desktop Operating System?",
    "multivote": false,
    "locked": false,
    "show_count": true,
    "options": [
      "Windows",
      "Linux",
      "Mac",
      "BSD",
      "Other"
    ]
  }
]
```

Don't forget the trailing slash at the end, otherwise you'll get a redirect response (status code 301) instead of the actual response.

Every question has an id (referred to qid from now on) and every option has an id (referred to oid from now on).

To get a list of all questions, make a GET request to [/api/questions/](http://localhost:8000/api/questions/).
This will return a dict with keys are qids and values as questions.

    curl http://localhost:8000/api/questions/

```
{
  "1": {
    "title": "Text Editor",
    "text": "Which text editors do you use?",
    "multivote": true,
    "locked": false,
    "show_count": false
  },
  "2": {
    "title": "Operating System",
    "text": "Which is you favorite desktop Operating System?",
    "multivote": false,
    "locked": false,
    "show_count": true
  }
}
```

You can get a similar list of all options at [/api/options/](http://localhost:8000/api/options/).
Every option will have a key called `question`, which will have the qid of the question it belongs to.

    curl http://localhost:8000/api/options/

```
{
  "1": {
    "question": 1,
    "text": "Vim",
    "count": null
  },
  "2": {
    "question": 1,
    "text": "Sublime",
    "count": null
  },
  "3": {
    "question": 1,
    "text": "Atom",
    "count": null
  },
  "4": {
    "question": 1,
    "text": "Notepad++",
    "count": null
  },
  "5": {
    "question": 1,
    "text": "Other",
    "count": null
  },
  "6": {
    "question": 2,
    "text": "Windows",
    "count": 0
  },
  "7": {
    "question": 2,
    "text": "Linux",
    "count": 0
  },
  "8": {
    "question": 2,
    "text": "Mac",
    "count": 0
  },
  "9": {
    "question": 2,
    "text": "BSD",
    "count": 0
  },
  "10": {
    "question": 2,
    "text": "Other",
    "count": 0
  }
}
```

## Authentication

You need to register to vote and view your votes.

To register send your username and password in a POST request to [/api/register/](http://localhost:8000/api/register/).
You can send data in either urlencoded form or as JSON by setting an appropriate `Content-Type`.

    curl http://localhost:8000/api/register/ -d username=user1 -d password=pass1

or

    curl http://localhost:8000/api/register/ -H 'Content-Type:application/json' \
    --data-binary '{"username": "user2", "password": "pass2"}'

This will give output `success`.

To vote, you can send a POST request at [/api/vote/](http://localhost:8000/api/vote/).
However, you need to be authenticated to do that.
2 auth methods are supported, the first using sessions and the second using basic auth.

To use sessions, you need to get a session cookie by sending a POST request to [/api/login/](http://localhost:8000/api/login/).

    curl -i http://localhost:8000/api/login/ -d username=user1 -d password=pass1

```
HTTP/1.0 200 OK
Date: Sun, 29 May 2016 16:39:38 GMT
Server: WSGIServer/0.2 CPython/3.4.3+
Content-Type: text/plain
X-Frame-Options: DENY
Vary: Cookie
Set-Cookie:  sessionid=csmdrzr8hisonw4uih5i3m1k70vhfprl; expires=Sun, 12-Jun-2016 16:39:38 GMT; HttpOnly; Max-Age=1209600; Path=/
Set-Cookie:  csrftoken=JKJJVh8mEqhaPjXI9hQsxxM3GF1PK0xX; expires=Sun, 28-May-2017 16:39:38 GMT; Max-Age=31449600; Path=/

success

```

You'll get a cookie (`sessionid=csmdrzr8hisonw4uih5i3m1k70vhfprl` in this example) in the response.

Finally, to vote, you should send auth info (either session cookie or a basic auth header)
in a POST request to [/api/vote/](http://localhost:8000/api/vote/).
You should send the option ids of the options you want to vote for in the request.

* Basic auth: `curl http://localhost:8000/api/vote/ --data-binary '[1, 3, 7]' -H 'Content-Type: application/json' -u 'user1:pass1'`
* Session auth: `curl http://localhost:8000/api/vote/ --data-binary '[1, 3, 7]' -H 'Content-Type: application/json' -b 'sessionid=csmdrzr8hisonw4uih5i3m1k70vhfprl'`

You will not get any output on a successful request.
Check the status code to find that out; 200 means success.

You can check the options you have voted for by sending a GET request at [/api/my-choices/](http://localhost:8000/api/my-choices/)

* Basic auth: `curl http://localhost:8000/api/my-choices/ -u 'user1:pass1'`
* Session auth: `curl http://localhost:8000/api/my-choices/ -b sessionid=csmdrzr8hisonw4uih5i3m1k70vhfprl`

```
[
  1,
  3,
  7
]
```
