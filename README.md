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
	* Run this to load the data to the database, without having to REAQUIRE the data:
	* 		./loadPezDb.py && ./loadPezData.py
	* 	You need ./loadPezDb.py to re-init the database
	***********************************************************************************
	Disgenet goes first
	Uniprot second
	Hintkb data are being wrangled on the spot
		Currently runs for about 6'30" 
			Largest part is HintKB2, but I am trying to thread that part, so I speed it up


	************************************************************************************************************
	*
	* DANGER DANGER DANGER
	*
	* There are two issues?bugs? running multithreaded code from  MacOSX
	* 	1. urllib.error.URLError: <urlopen error [Errno 8] nodename nor servname provided, or not known>
	*		Solution: edit /etc/hosts, insert ip and hostname ( wintermute wintermute.local )
	*			per StackOverflow: https://stackoverflow.com/questions/24812752/nodename-nor-servname-provided-or-not-known
	* 			Looks like some sort of lookup issue
	*
	*	2. Little Snitch does not have a rule/code signature for python performing http/https requests.
	*		Set Little Snitch to "silent permissive", and edit the rule later.
	* 
	*	3. Do not run lots of processes in the pool for HintKB2
	*		It is probably a VM with low resources, so it might die
	*		Currently using 40 processes
	*		Also the mac mini chokes
	*
	************************************************************************************************************


TODO:
	1. Multithread all the things:
		* sql inserts 
		* http requests
		* writing to disk?
	* Get back result from url call
[]	* counter on hintkb http requests
	* be able to run each part of the loading independently
		* functions for now
			* objects later
			__SINGLETHREADED__ = 0 #turn this into an Debug member variable

	* pretty print list of disregarded proteins under uniprot
	* tabulate/pretty print queries as columns on output (sprintf?()?)
	* write sql to files, for revire or dump.
	* use termcap/screen capabilities, in order to have a small counter at the bottom incrementing the status
	* maybe write the HintKB2 URLs to disk, just in case we need them later.
	* use SQL objects instead of naked statements 
		still be able to output full statements with color
	* import plot, graph perfomance data after run




NOTES

1. The script was automatically downloaded from the disgenet site, by following the instructions from the assignment and then clicking on the "download" link. You will be presented with an option to download the entire script

Description of additional fields used can be aquired from the DisGeNET RDF

Version 4.0 is at http://www.disgenet.org/web/DisGeNET/menu/rdf

Note: looks like the RDF changed ever since the last time I did the homework. The original question does not work: There is no /data/gene_roles any more. Solution is to resubmit the search and get a new python script.s

2. THey asked to see the restrictions and cardinality. Need a visual way of doing so.