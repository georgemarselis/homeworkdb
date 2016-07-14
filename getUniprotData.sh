#!/opt/local/bin/bash


for gene in $( < ./listOfGenes.tsv ) ; 
    do  wget --no-verbose --output-document=uniprot/proteins/${gene}.tsv http://www.uniprot.org/uniprot/\?query=gene:${gene}+AND+reviewed:yes\&sort=score\&columns=id,entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab ; done

rm -f ./listOfProteins.tsv

for file in uniprot/proteins/*.tsv; do cat $file | cut -f 1 | grep -v 'Entry' | sort | uniq -ui >> ./listOfProteins.tsv; done

cat ./listOfProteins.tsv | sort | uniq -ui | grep -v -e '^[AGH]'> out && mv out ./listOfProteins.tsv

for protein in $( < ./listOfProteins.tsv );
	do wget --no-verbose --output-document=uniprot/fasta/${protein}.fasta http://www.uniprot.org/uniprot/${protein}.fasta\?include=yes; done

rm -f uniprot/fasta/{P49792.fasta,P54252.fasta,P80668.fasta,Q05567.fasta,Q09298.fasta,Q15645.fasta,Q16342.fasta,Q47129.fasta,Q4P782.fasta,Q556K3.fasta,Q66GQ6.fasta,Q6NUN9.fasta,Q7SAM0.fasta,Q8IXI2.fasta,Q8IZ52.fasta,Q99IB8.fasta,Q9Y3I1.fasta,Q9Z2Q6.fasta}

#	wget --no-verbose --output-document=- 'http://www.uniprot.org/uniprot/?query=gene:SNCA+AND+reviewed:yes&sort=score&columns=id,entry%20name,protein%20names,reviewed,genes(PREFERRED),sequence&format=tab'