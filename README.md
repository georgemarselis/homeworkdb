# homeworkdb
PEZ2015 homework

Directly what's on the tin.

HOW TO RUN THIS MESS:

1. GET THE DATA YOU WILL NEED:

1.1 DisGeNet:
	*  Run getDisgenetData.py
		It will connect to disgenet and get you the list of genes you want. 
   		The result will be printed on the output, and written to a file called disgenet/disgenet_data.tsv. Output will be about 15 lines. 
   		Secondary output is the 'listOfGenes.tsv' file: it drives the Uniprot script bellow.

1.2 Uniprot:
 	* Run getUniprotData.sh
 		Depends on getDisgenetData.py;
 			You cannot run it without having run the above at least once
 		Downloads the list of candidate proteins and isomorphs
   		Uses GNU parallel for a significant speedup in download time.
 			Takes a minute or two.
 			Used to take 20-30 minutes.

1.3 Hintkb2:
	* Hintkb2 data are being wrangled directly from the 'loadPezData.py'
		Run 'loadPezData.py', after creating the schema.


LOADING THE DATABASE:

************************************************************************************************************
* Essentially, to load the database, type in the command line:
*     ./make_clean.sh && ./getDisgenetData.py && ./getUniprotData.sh && ./loadPezDb.py && ./loadPezData.py
************************************************************************************************************


2. Use the 'loadPezDb.py' python script to create the db. The 'loadPezDb.py' script is the pythonized version of pez_project2501.sql file
	Make sure you change the host IP, should you need to.

	2.1. If any of the connection details do not match, alter the ./loadConfiguration.sh script and execute it. 
		It exports the enviromental variables:
			PEZ_HOST
			PEZ_DATABASE
			PEZ_USER
			PEZ_PASSWORD

3. ./loadPezData.py: loads the data from disk to the database
	***********************************************************************************
	* Run this to load the data to the database, without having to REAQUIRE the data
	***********************************************************************************
	Disgenet goes first
	Uniprot second
	Hintkb data are being wrangled on the spot
		Takes about 20 minutes














NOTES

1. The script was automatically downloaded from the disgenet site, by following the instructions from the assignment and then clicking on the "download" link. You will be presented with an option to download the entire script

Description of additional fields used can be aquired from the DisGeNET RDF

Version 4.0 is at http://www.disgenet.org/web/DisGeNET/menu/rdf

Note: looks like the RDF changed ever since the last time I did the homework. The original question does not work: There is no /data/gene_roles any more. Solution is to resubmit the search and get a new python script.s


The rest of the scripts in the directory are sample scripts