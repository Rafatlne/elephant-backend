#!/bin/bash
python manage.py rqworker --with-scheduler $1
