#!/bin/sh

gunicorn -b :5000 --access-logfile - --error-logfile - src.app:app --workers=4

