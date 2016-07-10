#

for protein in $( < listOfProteins.csv ) ; do wget --output-document=- http://hintkb.ceid.upatras.gr/api/ppi/byprotein/${protein} | gunzip -c > ${protein}; done
