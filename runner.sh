#!/bin/bash
# Run the webserver, run the tests and kill the webserver!
python handler.py &
ID=$!
python freetests.py
python not-free-tests.py
kill $ID
#pkill -P $$
