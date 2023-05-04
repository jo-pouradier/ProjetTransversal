#!/bin/bash

sudo chmod 777 /dev/ttyACM0
python -m flask --app ./Site/flaskr/main run --host=0.0.0.0 