# homeworkdb
PEZ2015 homework

Directly what's on the tin.

HOW TO RUN THIS MESS:

1. GET THE DATA YOU WILL NEED:

1.1 DisGeNet:
	*  Run getDisgenetData.py
		Tt will connect to disgenet and get you the list of genes you want. 
   		The result will be printed on the output, and written to a file called disgenet/disgenet_data.tsv. Output will be about 15 lines. 
   		After saving disGenet.out, data will be processed and the list of relevant genes will be saved in listOfGenes.tsv, in the same directory as the rest of the files. Output should be around 6 lines
1.2 Hintkb2:
	* Run 




***** need more to get the data proper ******







2. Use the loadPezDb.py python script to create the db. The loadPez.py script is the pythonized version of pez_project2501.sql file

Make sure you change the host IP.

3. If any of the connection details do not match, alter the ./loadConfiguration.sh script and execute it. It exports the variables

4. ./loadPezData.py: loads the data from disk to the database
















NOTES

1. The script was automatically downloaded from the disgenet site, by following the instructions from the assignment and then clicking on the "download" link. You will be presented with an option to download the entire script

Description of additional fields used can be aquired from the DisGeNET RDF

Version 4.0 is at http://www.disgenet.org/web/DisGeNET/menu/rdf

Note: looks like the RDF changed ever since the last time I did the homework. The original question does not work: There is no /data/gene_roles any more. Solution is to resubmit the search and get a new python script.s


The rest of the scripts in the directory are sample scripts