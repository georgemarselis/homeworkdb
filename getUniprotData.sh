#!/opt/local/bin/bash


for gene in $( < ./listOfGenes.tsv ) ; 
    do  wget --no-verbose --output-document=uniprot/genes/${gene}.tsv http://www.uniprot.org/uniprot/\?query=${gene}\&sort=score\&columns=id,entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab ; done

rm -f ./listofProteins.tsv

for file in uniprot/genes/*.tsv;
	do tail -q -n 1 $file | cut -f 1 >> ./listofProteins.tsv; done


for protein in $( < ./listofProteins.tsv );
	do wget --no-verbose --output-document=uniprot/proteins/${protein}.fasta http://www.uniprot.org/uniprot/${protein}.fasta\?include=yes ; done
