#!/opt/local/bin/bash

for protein in $( < listOfProteins.tsv ) ; do wget --no-verbose --output-document=- http://hintkb.ceid.upatras.gr/api/ppi/byprotein/${protein} | gunzip -c > hintkb/${protein}; done
