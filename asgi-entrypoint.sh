#!/bin/sh

until python main.py;
do
    echo "Waiting for database connection..."
    sleep 2
done
