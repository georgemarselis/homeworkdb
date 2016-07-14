#!/opt/local/bin/bash

for protein in $( < listOfProteins.csv ) ; do wget --output-document=- http://hintkb.ceid.upatras.gr/api/ppi/byprotein/${protein} | gunzip -c > hintkb/${protein}; done
