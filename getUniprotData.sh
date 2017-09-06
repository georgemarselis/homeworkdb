#!/opt/local/bin/bash

rm -f ./uniprot/fasta/*.fasta
rm -f ./uniprot/proteins/*.tsv

# get the proteins associated with the genes
for gene in $( < ./listOfGenes.tsv ) ; 
    do  wget --no-verbose --output-document=uniprot/proteins/${gene}.tsv http://www.uniprot.org/uniprot/\?query=gene:${gene}\&sort=score\&columns=id,entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab ; done

rm -f ./listOfProteins.tsv

# create the list of proteins; that list will be fed to uniprot to pass back the fasta files and the isoforms
for file in uniprot/proteins/*.tsv; do cat $file | cut -f 1 | grep -v 'Entry' | sort | uniq -ui >> ./listOfProteins.tsv; done

# get rid of some classes of proteins
cat ./listOfProteins.tsv | sort | uniq -ui | grep -v -e '^[AGH]'> out && mv out ./listOfProteins.tsv

#get the fasta files
for protein in $( < ./listOfProteins.tsv );
	do wget --no-verbose --output-document=uniprot/fasta/${protein}.fasta http://www.uniprot.org/uniprot/${protein}.fasta\?include=yes; done

# For some reason, some filescome up empty consistently, when running the shell script. Probably timeout from the website.
# Run them here manually
for emptyfasta in $( find uniprot/fasta -size 0);
	do wget --no-verbose --output-document=uniprot/fasta/${emptyfasta}.fasta http://www.uniprot.org/uniprot/${emptyfasta}.fasta\?include=yes; done

# cleanup; not sure it is still needed
# rm -f uniprot/fasta/{B9VTE0.fasta,E3M4K9.fasta,P49792.fasta,P54252.fasta,P80668.fasta,Q05567.fasta,Q09298.fasta,Q15645.fasta,Q16342.fasta,Q47129.fasta,Q4P782.fasta,Q556K3.fasta,Q66GQ6.fasta,Q6NUN9.fasta,Q7SAM0.fasta,Q6AX34.fasta,Q8IXI2.fasta,Q8IZ52.fasta,Q99IB8.fasta,Q9Y3I1.fasta,Q9Z2Q6.fasta,U3NGQ0.fasta,W4YQE2.fasta,W4Z7Z7.fasta}

#	wget --no-verbose --output-document=- 'http://www.uniprot.org/uniprot/?query=gene:SNCA+AND+reviewed:yes&sort=score&columns=id,entry%20name,protein%20names,reviewed,genes(PREFERRED),sequence&format=tab'