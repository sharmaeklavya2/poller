# Api Examples

You can use curl, python's urllib, firebug, etc. for making POST requests.
I will use `curl` for all example requests here since that is simple to use from any shell.
You can pass the `-i` option to `curl` if you want to see more info about the response.

## GETting public info

Make a GET request to [{url_index}]({full_url_index}) to get an overview of the questions:

    curl {full_url_index}

```
{output_index}
```

Don't forget the trailing slash at the end, otherwise you'll get a redirect response (status code 301) instead of the actual response.

Every question has an id (referred to qid from now on) and every option has an id (referred to oid from now on).

To get a list of all questions, make a GET request to [{url_questions}]({full_url_questions}).
This will return a dict with keys are qids and values as questions.

    curl {full_url_questions}

```
{output_questions}
```

You can get a similar list of all options at [{url_options}]({full_url_options}).
Every option will have a key called `question`, which will have the qid of the question it belongs to.

    curl {full_url_options}

```
{output_options}
```

## Authentication

You need to register to vote and view your votes.

To register send your username and password in a POST request to [{url_register}]({full_url_register}).
You can send data in either urlencoded form or as JSON by setting an appropriate `Content-Type`.

    curl {full_url_register} -d username=user1 -d password=pass1

or

    curl {full_url_register} -H 'Content-Type:application/json' \
    --data-binary '{{"username": "user2", "password": "pass2"}}'

This will give output `success`.

To vote, you can send a POST request at [{url_vote}]({full_url_vote}).
However, you need to be authenticated to do that.
2 auth methods are supported, the first using sessions and the second using basic auth.

To use sessions, you need to get a session cookie by sending a POST request to [{url_login}]({full_url_login}).

    curl -i {full_url_login} -d username=user1 -d password=pass1

```
{output_login}
```

You'll get a cookie (`{cookie}` in this example) in the response.

Finally, to vote, you should send auth info (either session cookie or a basic auth header)
in a POST request to [{url_vote}]({full_url_vote}).
You should send the option ids of the options you want to vote for in the request.

* Basic auth: `curl {full_url_vote} --data-binary '{option_ids}' -H 'Content-Type: application/json' -u 'user1:pass1'`
* Session auth: `curl {full_url_vote} --data-binary '{option_ids}' -H 'Content-Type: application/json' -b '{cookie}'`

You will not get any output on a successful request.
Check the status code to find that out; 200 means success.

You can check the options you have voted for by sending a GET request at [{url_my_choices}]({full_url_my_choices})

* Basic auth: `curl {full_url_my_choices} -u 'user1:pass1'`
* Session auth: `curl {full_url_my_choices} -b {cookie}`

```
{output_my_choices}
```
