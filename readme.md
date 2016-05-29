# Poller

An API-based app for polling. I have made if for testing purposes.

This runs on both Python 2 and 3.

## About the app

There are multiple questions on a site.
Each question has various options which users can vote for.
A user can also unvote options previously voted for.

Users can vote or unvote only when a question is unlocked.
Admins can lock or unlock a question any time.
Admins can also control whether vote count for an option is visible.

Users have to register to vote.
Currently only username and password are required.
The admin can turn registrations on/off.

Some questions can have multivote support, that is, users can vote multiple distinct options of the same question.
When multivoting is disabled for a particular question, only one option can be chosen for that question.
If the user votes for option A and later votes for option B for a non-multivote question, B will be selected but not A.

## Directories

* `project_conf` - settings and configuration
* `main` - django app
* `lib` - reusable code
* `devel` - developer tools

## Get the server running

    python manage.py runserver

This is enough to run a server.
However, you might want to customize it.

The settings are stored in `project_conf/settings/`.
To modify your settings, copy contents of `default.py` to `local.py` and make modifications to `local.py`.

This app supports Django's admin interface.
Visit http://localhost:8000/admin/ to view it.
You will need a superuser account to access it.
You can create it using:

    python manage.py createsuperuser

## Using the API

See `docs/api_examples.md` for example usage.

See `docs/api_ref.md` for API endpoint reference.

## License

Copyright 2016 - Eklavya Sharma

Licensed under [GNU GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt)
