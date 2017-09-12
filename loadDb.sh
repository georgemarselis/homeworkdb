#!/bin/bash

./make_clean.sh && ./getDisgenetData.py && ./getUniprotData.sh && ./loadPezDb.py && ./loadPezData.py
