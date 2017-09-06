#!/opt/local/bin/bash

# cleanup
rm -f ./uniprot/fasta/*.fasta
rm -f ./uniprot/proteins/*.tsv
rm -f ./listOfProteins.tsv

# setting up
mkdir -p ./uniprot/proteins
mkdir -p ./uniprot/fasta

# get the proteins associated with the genes
#for gene in $( < ./listOfGenes.tsv ) ; 
#   do  wget --no-verbose --output-document=uniprot/proteins/${gene}.tsv http://www.uniprot.org/uniprot/\?query=gene:${gene}\&sort=score\&columns=id,entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab ; done
# GNU parallel version; much much much faster
cat ./listOfGenes.tsv | /opt/local/bin/parallel --progress --bar --eta --jobs 600% 'wget --no-verbose --output-document=uniprot/proteins/{}.tsv http://www.uniprot.org/uniprot/\?query=gene:{.}\&sort=score\&columns=id,entry%20name,protein%20names,reviewed,genes\(PREFERRED\)\&format=tab'

# create the list of proteins; that list will be fed to uniprot to pass back the fasta files and the isoforms
for file in uniprot/proteins/*.tsv; do cat $file | cut -f 1 | grep -v 'Entry' | sort | uniq -ui >> ./listOfProteins.tsv; done

# get rid of some classes of proteins
cat ./listOfProteins.tsv | sort | uniq -ui | grep -v -e '^[AGH]'> out && mv out ./listOfProteins.tsv

#get the fasta files
#for protein in $( < ./listOfProteins.tsv );
#	do wget --no-verbose --output-document=uniprot/fasta/${protein}.fasta http://www.uniprot.org/uniprot/${protein}.fasta\?include=yes; done
# GNU parallel version; much much much faster
cat ./listOfProteins.tsv | /opt/local/bin/parallel --progress --bar --eta --jobs 600% 'wget --no-verbose --output-document=uniprot/fasta/{}.fasta http://www.uniprot.org/uniprot/{.}.fasta\?include=yes'

# For some reason, some filescome up empty consistently, when running the shell script. Probably timeout from the website.
# Run them here manually
for emptyfasta in $( find uniprot/fasta -type f -iname \*.fasta -size 0 );
	do emptyfasta=$(/usr/bin/basename ${emptyfasta}); wget --no-verbose --output-document=uniprot/fasta/"${emptyfasta%.*}".fasta http://www.uniprot.org/uniprot/"${emptyfasta%.*}".fasta\?include=yes; done

for emptyfasta in $( find uniprot/fasta -size 0);
	do echo -e "File $emptyfasta has zero size, still."; done


# cleanup;
# some isoforms do not have the related protein in the table, so they get axed.
# rm -f ./uniprot/fasta/{B1AKC3,B1AWI3,B5A5T2,B5DF30,B6E506,D4A6U0,D5M8S2,E3M4K9,E7F5W0,F1MND2,F1MNT6,F1NYQ3,F1QHY5,F1STB6,F6WDS3,F6X525,F6X965,F6X975,F6XBY5,F6ZI77,F6ZR94,F7D2A3,F7EPW4,F7ETU7,F7FQX2,F7GB62,F7GLB8,F7GRM5,F7H1I4,F7H1J0,F7HL19,F8W598,F8W624,I3J4B9,I3J4C0,I3K565,I3M5Q7,J9P6J8,K7FYC8,M1S0Z2,M1SQS2,M3WHI6,M3X8P2,M3XE54,M3Y230,M3YZ74,M4AR44,O16580,O16581,O60260}.fasta
# rm -f ./uniprot/fasta/{P0DI69,P0DI70,P0DI71,P80668,P97265}.fasta
# rm -f ./uniprot/fasta/{Q09298,Q0V997,Q20611,Q47129,Q502A1,Q556K3,Q5M868,Q5RF65,Q5W7N7,Q66J37,Q69ZF3,Q6AX34,Q6GUQ5,Q7SYW2,Q8H0L8,Q8IMY3,Q8QHK5,Q969N8,Q96TC2,Q9H227,Q9HCG7,Q9IA99,Q9JK66,Q9UB00,Q9VCJ4,Q9WVS6}.fasta
# rm -f ./uniprot/fasta/{S4Z0H1,S4Z225,S5M602}.fasta
# rm -f ./uniprot/fasta/{T2M517,U3CTH3,U3JHQ3,U3NGQ0,V5G1H9,V9Q378,V9Q384,V9Q389,V9Q393,V9Q399,V9Q3A4,V9Q3A9,V9Q3B4,V9Q3C0,V9Q3C5,V9Q3C9,V9Q3D5,V9Q3E0,V9Q3E5,V9Q3E8,V9Q3F5,V9Q3I0,V9Q3I4,V9Q3I9,V9Q3J4,V9Q3J9,V9Q3K1,V9Q3K6,V9Q3L1,V9Q3L4,V9Q3L7,V9Q3M0,V9Q3M5,V9Q3N0,V9Q3N4,V9Q3N8}.fasta
