#!/opt/local/bin/python3.4

import pymysql
import csv
import os
import sys
import xml.etree.ElementTree
import re
import glob
import time
import urllib.request
import json
import random
import getopt
import multiprocessing
from io  import StringIO
from Bio import SeqIO
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from clint.textui import colored, puts


def usage( ):
	print( 
"""
These aint the droids you are looking for.

-h, --help          You are looking at it.

-v, --verbose       Turn on any extra verbosity we got

-f, --test-function <function1, function2, function3 > 	

                    Tell the program to only run only those 
                    subfunctions. Used in testing or to
                    reload data.

                    Available functions are:
                        disgenet
                        uniprot
                        hintkb2

-d, --debug [1, 2, 3]
                    Set debug flag. Requires --test-function
                    If no debug level is explicitly set,
                        it assumes 1.
                    Higher level of debugging enable extra 
                    debugging in the uniprot function:
                    Debug level 2: run up to the end of the 
                    SQL INSERT INTO PROTEIN statments and stop.
                        Assumes 1.
                    Debug level 3: run up to the end of the
                    SQL INSERT INTO ISOMORTH statements and stop.
                        Assumes 1. Cannot be used in conjuction with 2.

""")

def callHintkb( selectResult ):
	hintkbURL = "http://hintkb.ceid.upatras.gr/api/functions/byprotein/"
	URL = hintkbURL + selectResult[0]  # protein is a list of lists, actually
	time.sleep(0.1 + random.uniform( 0.1, 0.8 ) ) # stager
	response = urllib.request.urlopen( "http://google.com" )
	counter = 5500

	try:
		response = urllib.request.urlopen( URL )
	except urllib.error.URLError as e:
 		print( colored.red(  "Failed: " + hintkbURL + selectResult[0] ) + colored.magenta( "\t( " + str( counter ) + " / " + str( len( selectResult ) ) + " )" ) )
	else:
 		print( colored.green(  "\t" + hintkbURL + selectResult[0] ) + colored.magenta( "\t( " + str( counter ) + " / " + str( len( selectResult ) ) + " )" ) )

	restResult = response.read( ) 
	# {"function_id":17269,"go_term":"0033603","function_name":"positive regulation of dopamine secretion","function_namespace":"biological_process"}
	result = restResult.decode( 'UTF-8' ) 
	return result



def disgenet( ):
	print( colored.yellow( "\n########################################### DISGENET -- DISGENET -- DISGENET -- ###########################################\n" ) )

	# # connect to db
	host, user, password, db = connection_details( )
	conn = pymysql.connect( host, user, password )
	if conn != -1 :
		print( colored.green( 'database connection established' ) )
	else:
		print( colored.red ('Houston we have a problem' ) )
		sys.exit( 255 )

	conn.begin( )
	cursor = conn.cursor( )
	# select our database
	cursor.execute( "use " + db )
	conn.commit( )

	## disgenet
	###########################################
	disgenetDataFile = 'disgenet/disgenet_data.tsv'
	disgenetFieldNames = [ 'c1.diseaseId', 'c1.OMIM', 'c2.symbol', 'c2.geneId', 'c2.uniprotId', 'c2.description', 'c2.pantherName', 'c0.score', 'c0.Npmids', 'c0.Nsnps', 'c3.Ndiseases' ]
	restkey    = 'unknownkey';
	restval    = 'uknownvalue';
	dialect    = 'excel-tab';

	# read payload
	###########################################
	disgenetCsvfile = open( disgenetDataFile )
	disgenetReader = csv.DictReader( disgenetCsvfile, disgenetFieldNames, restkey, restval, dialect );

	kot = 0
	counter = 1
	disgenetReaderLength = len( list ( disgenetReader ) ) - 1 # -1 for the header

	disgenetCsvfile = open( disgenetDataFile )
	disgenetReader = csv.DictReader( disgenetCsvfile, disgenetFieldNames, restkey, restval, dialect );

	for row in disgenetReader:
		if kot == 0 : # magic to skip the first header row
			kot = 1
			continue
		insertgenedataQuery = "INSERT INTO gene( geneId, geneName, disgenetScore, noPubMedIDs ) VALUES ( '" + row['c2.geneId'] + "', '" + row['c2.symbol'] + "', " + row['c0.score'] + ", " + row['c0.Npmids'] +" );"
		try:
			cursor.execute( insertgenedataQuery )
		except pymysql.err.IntegrityError:
			print( colored.magenta( " ( " + str ( counter ) + " of " + str( disgenetReaderLength ) + " ) " ) + colored.red( "FAILED: " + insertgenedataQuery ) )
		else:
			out1 = colored.magenta( " ( " + str ( counter ) + " of " + str( disgenetReaderLength ) + " )\t" )
			out2 = colored.cyan( insertgenedataQuery )
			print( out1 +  out2 )
		counter += 1
	conn.commit( )
	cursor.close( )

	if __DEBUG__:
		sys.exit( 0 )

	###########################################


def uniprot( ):
	print( colored.yellow( "\n########################################### UNIPROT -- UNIPROT -- UNIPROT -- ###########################################\n") )


	# # connect to db
	host, user, password, db = connection_details( )
	conn = pymysql.connect( host, user, password )
	if conn != -1 :
		print( colored.green( 'database connection established' ) )
	else:
		print( colored.red ('Houston we have a problem' ) )
		sys.exit( 255 )

	conn.begin( )
	cursor = conn.cursor( )
	# select our database
	cursor.execute( "use " + db )
	conn.commit( )

	##uniprot
	###########################################
	uniprotProteinsDir      = './uniprot/proteins'
	uniprotFastaDir         = './uniprot/fasta'
	uniprotProteinDataFiles = os.listdir( uniprotProteinsDir )
	uniprotFastaDataFiles   = os.listdir( uniprotFastaDir )
	unitprotFieldNames = [ 'Entry', 'Entry name', 'Protein names', 'Status', 'Gene names  (primary )']
	restkey    = 'unknownkey';
	restval    = 'uknownvalue';
	dialect    = 'excel-tab';

	uniprotDataFilesLength = 0 #5500 # Get a total count of items to insert.
	for uniprotProteinDataFile in uniprotProteinDataFiles: 
		uniprotCsvFile = open( uniprotProteinsDir + '/' + uniprotProteinDataFile )
		reader = csv.DictReader( uniprotCsvFile, unitprotFieldNames, restkey, restval, dialect );
		for row in reader:
			#	next(reader, None) # skip the headers
			kot = 'FALSE'
			if row['Status'] == 'reviewed':
				kot = 'TRUE'
			if row['Entry'] == 'Entry':
				continue
			gene , extension = os.path.splitext( uniprotProteinDataFile )
			if gene != str.upper(row['Gene names  (primary )']):
				continue
			uniprotDataFilesLength += 1

	# read payload - proteins
	###########################################
	counter = 1
	for uniprotProteinDataFile in uniprotProteinDataFiles: 
		uniprotCsvFile = open( uniprotProteinsDir + '/' + uniprotProteinDataFile )
		reader = csv.DictReader( uniprotCsvFile, unitprotFieldNames, restkey, restval, dialect );
		for row in reader:
			#	next(reader, None) # skip the headers
			kot = 'FALSE'
			if row['Status'] == 'reviewed':
				kot = 'TRUE'
			if row['Entry'] == 'Entry':
				continue
			gene , extension = os.path.splitext( uniprotProteinDataFile )
			if gene != str.upper(row['Gene names  (primary )']):
				continue
			geneId = str.upper(row['Gene names  (primary )'])
			if re.search( "-\d+", geneId ):
				geneId, _  = geneId.split( '-', 1 )
			
			insertgenedata_query = "INSERT INTO protein( proteinId, proteinName, proteinConfirmed, geneName ) VALUES ( '" + row['Entry'] + "', '" + str.upper(row['Protein names']) + "', " + kot + ", '" + geneId +"' );"
			try:
				cursor.execute( insertgenedata_query )
			except pymysql.err.IntegrityError:
				print( colored.magenta( " ( " + str ( counter ) + " of " + str( uniprotDataFilesLength ) + " ) " ) + colored.red( " FAILED: " + insertgenedata_query ) )
				sys.exit( 255 )
			else:
				print( colored.magenta( " ( " + str ( counter ) + " of " + str( uniprotDataFilesLength ) + " ) " ) + colored.cyan( insertgenedata_query ) )
			counter += 1

	conn.commit( ) #moving the commit out of the loop allows for a somewhat faster execution time, at the price of doing a bulk commit at the end.
	cursor.close( )

	if __DEBUG1__:
		sys.exit( 0 )

	###########################################

	ignoredProteins = [ ]
	# read payload - fasta
	################
	unitprotFieldNames = [ 'fasta sequence', 'name' ]
	counter  = 1
	for uniprotFastaDataFile in uniprotFastaDataFiles: 

		try:
			uniprotFastaFile = SeqIO.parse(open( uniprotFastaDir + '/' + uniprotFastaDataFile ) ,'fasta')
		except:
			print ( "Could not open file " + uniprotFastaDir + '/' + uniprotFastaDataFile + " . Exiting." )
		for fasta in uniprotFastaFile:
			print( )
			print( colored.magenta( "#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + uniprotFastaDataFile + " (" + str( counter ) + " of " + str( len( uniprotFastaDataFiles ) ) + ") <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" ) )
			name, sequence = fasta.id, str( fasta.seq )
			# sp|O02828|TAU_CAPHI , sp|O02828-2|TAU_CAPHI , tr|A0A151NP48|A0A151NP48_ALLMI
			_, proteinId, isomorphId = name.split( '|', 3 )
			name = proteinId
			if re.search( "-\d+", proteinId ):
				proteinId, _  = proteinId.split( '-', 1 )
			insertgenedata_query = "INSERT INTO isomorph( isomorphName, isomorphFASTASequence, proteinId ) VALUES ( '" + name + "', '" + sequence + "', '" + proteinId + "' );"
			try:  # any FASTA seqquence that does not have a primary sequence/key in the db gets ignored
				cursor.execute( insertgenedata_query )
			except pymysql.err.IntegrityError:
				print( colored.red( "No primary protein key in db: Ignore: " + insertgenedata_query ) )
				# add protein to list of proteins that need to be looked at: why were they downloaded, if they have nothing to do with our sequences.
				ignoredProteins.append( proteinId )
				continue
			else:
				print( colored.cyan( insertgenedata_query ) )

		counter += 1 # increment files read
	conn.commit( ) #moving the commit out of the loop allows for a somewhat faster execution time, at the price of doing a bulk commit at the end.
	cursor.close( )

	if __DEBUG2__:
		sys.exit( 0 )

	# write failed fasta entries to disk
	if ignoredProteins: 
		ignoredProteinsFile = "ignoredProteins.txt"
		with open( ignoredProteinsFile, 'w' ) as file:
			#
			# pretty print the array in a nice term-lenght size array
			#
			print( colored.yellow( "##############################################################################"))
			print( "The following " + str( len( ignoredProteins ) - 1 ) + " proteins were ignored. They where written to disk for follow up: " + colored.yellow( ignoredProteins ) )
			print( colored.yellow( "##############################################################################"))
			try:
				file.write( "\n".join( ignoredProteins ) )
			except:
				print ( colored.red( "Could not write proteins to disk; Aborting.") )
				sys.exit( 255 )

	 # something funky is happening with this: if you time the script it takes 42 secs on my mac mini, for the script to get up to here.
	 # 		but should you uncomment the time.sleep() command, /usr/bin/time returns 0m37.662s as real time. 
	time.sleep( 3 )
	###########################################
	if __DEBUG__:
		sys.exit( 0 )


def hintkb2( ):

	print( colored.yellow( "\n########################################### HINTKB2 -- HINTKB2 -- HINTKB2 -- ###########################################\n") )

	## GeneOntology/hintdb
	###########################################
	#hintkbFieldNames = [ 'function_id', 'go_term', 'function_name', 'function_namespace' ]

	# # connect to db
	host, user, password, db = connection_details( )
	conn = pymysql.connect( host, user, password )
	if conn != -1 :
		print( colored.green( 'database connection established' ) )
	else:
		print( colored.red ('Houston we have a problem' ) )
		sys.exit( 255 )

	conn.begin( )
	cursor = conn.cursor( )
	# select our database
	cursor.execute( "use " + db )
	conn.commit( )

	# #read payload
	selectQuery = "select distinct protein.proteinid from protein order by proteinid;"
	cursor.execute( selectQuery )
	selectResult = cursor.fetchall( )
	# print( selectResult )
	# sys.exit( 0 )

	ignoredOntologiesQuery = [ ]
	response  = " "
	results   = { }

	# manager = multiprocessing.Manager()
	# return_dict = manager.dict()
	processes = 100

# 50 workers gets us | 100 workers gets us | 150 workers gets us
# real	5m53.480s    |   5m40.438s         | 5m42.387s
# user	0m13.203s    |   0m14.236s         | 0m17.817s
# sys	0m6.900s     |   0m7.495s          | 0m10.103s

	print( colored.yellow( "Contacting HintKB2: " + str(len( selectResult )) + " results, using " + str(processes) + " processes" ) )
	with multiprocessing.Pool( processes ) as p:
		p.map( callHintkb, selectResult )

	sys.exit( 0 )

	counter = 1; # incremented at the end of the loop
	for result in results:
		parsedJson = { }
		parsedJson = json.loads( result )
		if parsedJson:
			for item in parsedJson:
				bar = re.sub( '_', ' ', item['function_namespace'] )
				insertGoQuery = "INSERT INTO geneOntology( ontologyId, ontologyName, ontologyFunction, biological_process, proteinId ) values ( " + str(item['function_id']) + ', ' + str(item['go_term']) + ', \'' + str(item['function_name']) + '\', \'' +  str(bar) + '\', \'' + str( result.key ) + '\' );' 
				try:
					cursor.execute( insertGoQuery )
				except:
					print( colored.magenta( " ( " + str ( counter ) + " of " + str( len ( list( parsedJson ) ) ) + " ) " ) + colored.red( insertGoQuery ) )
					ignoredOntologiesQuery.append( insertGoQuery )
				else:
					print( colored.magenta( " ( " + str ( counter ) + " of " + str( len ( list( parsedJson ) ) ) + " ) " ) + colored.cyan( insertGoQuery ) )
		counter += 1

	conn.commit( ) #moving the commit out of the loop allows for a somewhat faster execution time, at the price of doing a bulk commit at the end.

	sys.exit( 0 )

	#################
	# Currently attempting to turn this code to multithreadeds
	################

	# write failed ongologies entries to disk
	if ignoredOntologiesQuery: 
		ignoredOntologiesFile = "ignoredOntologies.txt"
		print( colored.yellow( "##############################################################################"))
		print( "The following ontologies were ignored. They where written to disk (" + ignoredOntologiesFile + ") for follow up: " )
		for item in ignoredOntologiesQuery:
			print( colored.yellow( item ) )
		print( colored.yellow( "##############################################################################"))
		with open( ignoredOntologiesFile, 'w' ) as file:
			for ontology in ignoredOntologiesQuery:
				file.write( ontology )

	#cursor.close( )
	###########################################

def connection_details( ):
	host       = '192.168.1.5';
	user       = 'root';
	password   = '12345'
	defaultcharset    = 'utf8'
	defaultcollation  = 'utf8_general_ci'


	db = "pez_project2501a"

	if "PEZ_HOST" in os.environ:
		host = str(os.environ['PEZ_HOST'])
	if "PEZ_USER" in os.environ:
		user = str(os.environ['PEZ_USER'])
	if "PEZ_PASSWORD" in os.environ:
		password = str(os.environ['PEZ_PASSWORD'])
	if "PEZ_DATABASE" in os.environ:
		db = str(os.environ['PEZ_DATABASE'])

	return ( host, user, password, db )

def main():

	__DEBUG__  = 0
	__DEBUG1__ = 0
	__DEBUG2__ = 0

	try:
		opts, args = getopt.getopt( sys.argv[1:], "hvdf", [ "help", "verbose", "debug", "test-function" ] )
	except getopt.GetoptError as err:
		# print help information and exit:
		print( err ) # will print something like "option -a not recognized"
		usage( )
		sys.exit(2)

	function = None
	verbose = False
	for o, a in opts:
		if o == "-v":
		    verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-d", "--debug"):
			# see if there is an argument to debug and set debug appropriatelly
			__DEBUG__ = 1
		elif o in ("-f", "--test-function"):
			kot
			# get the argument of which function to test to send
		else:
			assert False, "unhandled option"

	##### load data from files
	###########################################
	#disgenet( )
	#uniprot( )
	hintkb2( )



if __name__ == "__main__":
	main( )

#print( colored.yellow( "\n########################################### END - END - END ###########################################\n") )

