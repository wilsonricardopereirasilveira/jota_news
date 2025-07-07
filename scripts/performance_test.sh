#!/bin/bash
locust -f locustfile.py --headless -u 100 -r 10 -t1m
