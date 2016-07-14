#!/opt/local/bin/bash


for gene in $( < ./listOfGenes.tsv ) ; 
    do  wget --no-verbose --output-document=uniprot/proteins/${gene}.tsv http://www.uniprot.org/uniprot/\?query=gene:${gene}+AND+reviewed:yes\&sort=score\&columns=id,entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab ; done

rm -f ./listOfProteins.tsv

for file in uniprot/proteins/*.tsv; do cat $file | cut -f 1 | grep -v 'Entry' | sort | uniq -ui >> ./listOfProteins.tsv; done

cat ./listOfProteins.tsv | sort | uniq -ui | grep -v -e '^[AGH]'> out && mv out ./listOfProteins.tsv

for protein in $( < ./listOfProteins.tsv );
	do wget --no-verbose --output-document=uniprot/fasta/${protein}.fasta http://www.uniprot.org/uniprot/${protein}.fasta\?include=yes; done

#	wget --no-verbose --output-document=- 'http://www.uniprot.org/uniprot/?query=gene:SNCA+AND+reviewed:yes&sort=score&columns=id,entry%20name,protein%20names,reviewed,genes(PREFERRED),sequence&format=tab'