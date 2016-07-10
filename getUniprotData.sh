#!/opt/local/bin/bash

for protein in $( < listOfProteins.csv ) ; do wget --output-document=uniprot/${protein}.fasta http://www.uniprot.org/uniprot/${protein}.fasta?include=yes ; wget --output-document=uniprot/${protein} http://www.uniprot.org/uniprot/${protein}.txt ;done

