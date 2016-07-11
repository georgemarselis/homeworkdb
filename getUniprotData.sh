#!/opt/local/bin/bash


for gene in $( < listOfGenes.tsv ) ; 
    do  wget --no-verbose --output-document=uniprot/${gene}.tsv http://www.uniprot.org/uniprot/\?query=${gene}\&sort=score\&columns=entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab ; done

