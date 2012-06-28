#!/bin/sh

./manage.py sqlclear addresses | ./manage.py dbshell
./manage.py syncdb

./manage.py runserver

