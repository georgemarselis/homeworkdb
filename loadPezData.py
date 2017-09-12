#!/opt/local/bin/python3.4

import pymysql
import csv
import os
import sys
import xml.etree.ElementTree
import re
import os.path
import glob
import time
import urllib.request
import json
import random
import getopt
import pickle
from multiprocessing import Pool, Value
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


def disgenet( ):
	print( colored.yellow( "\n########################################### DISGENET -- DISGENET -- DISGENET -- ###########################################\n" ) )

	__DEBUG__ = 0
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

	disgenetCsvfile     = open( disgenetDataFile )
	disgenetReader      = csv.DictReader( disgenetCsvfile, disgenetFieldNames, restkey, restval, dialect );
	insertgenedataQuery = [ ]

	for row in disgenetReader:
		if kot == 0 : # magic to skip the first header row
			kot = 1
			continue
		insertgenedataQuery.append( "INSERT INTO gene( geneId, geneName, disgenetScore, noPubMedIDs ) VALUES ( '" + row['c2.geneId'] + "', '" + row['c2.symbol'] + "', " + row['c0.score'] + ", " + row['c0.Npmids'] +" );" )

	for query in insertgenedataQuery:
		try:
			cursor.execute( query )
		except pymysql.err.IntegrityError:
			print( colored.magenta( " ( " + str ( counter ) + " of " + str( disgenetReaderLength ) + " ) " ) + colored.red( "FAILED: " + query ) )
		else:
			print( colored.magenta( " ( " + str ( counter ) + " of " + str( disgenetReaderLength ) + " )\t" ) + colored.cyan( query ) )
		counter += 1
	conn.commit( )
	cursor.close( )

	if __DEBUG__:
		sys.exit( 0 )

	###########################################

def uniprot( ):
	print( colored.yellow( "\n########################################### UNIPROT -- UNIPROT -- UNIPROT -- ###########################################\n") )

	global __DEBUG__
	global __DEBUG1__
	global __DEBUG2__

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
	insertgenedata_query = [ ]
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
			
			insertgenedata_query.append( "INSERT INTO protein( proteinId, proteinName, proteinConfirmed, geneName ) VALUES ( '" + row['Entry'] + "', '" + str.upper(row['Protein names']) + "', " + kot + ", '" + geneId +"' );" )

	counter  = 1
	for query in insertgenedata_query:
		try:
			cursor.execute( query )
		except pymysql.err.IntegrityError:
			print( colored.magenta( " ( " + str ( counter ) + " of " + str( uniprotDataFilesLength ) + " ) " ) + colored.red( " FAILED: " + query ) )
			sys.exit( 255 )
		else:
			print( colored.magenta( " ( " + str ( counter ) + " of " + str( uniprotDataFilesLength ) + " ) " ) + colored.cyan( query ) )
		counter += 1

	conn.commit( ) #moving the commit out of the loop allows for a somewhat faster execution time, at the price of doing a bulk commit at the end.
	# cursor.close( )

	# if __DEBUG1__:
	# 	sys.exit( 0 )

	###########################################

	# read payload - fasta
	################
	unitprotFieldNames = [ 'fasta sequence', 'name' ]
	insertgenedata_query = [ ]
	for uniprotFastaDataFile in uniprotFastaDataFiles: 

		try:
			uniprotFastaFile = SeqIO.parse(open( uniprotFastaDir + '/' + uniprotFastaDataFile ) ,'fasta')
		except:
			print ( "Could not open file " + uniprotFastaDir + '/' + uniprotFastaDataFile + " . Exiting." )
		for fasta in uniprotFastaFile:
			name, sequence = fasta.id, str( fasta.seq )
			# sp|O02828|TAU_CAPHI , sp|O02828-2|TAU_CAPHI , tr|A0A151NP48|A0A151NP48_ALLMI
			_, proteinId, isomorphId = name.split( '|', 3 )
			name = proteinId
			if re.search( "-\d+", proteinId ):
				proteinId, _  = proteinId.split( '-', 1 )
			# insertgenedata_query.append( "INSERT INTO isomorph( isomorphName, isomorphFASTASequence, proteinId ) VALUES ( '" + name + "', '" + sequence + "', '" + proteinId + "' );" )
			insertgenedata_query.append( ( name, sequence, proteinId ) )

	#
	# this can now be parallelised 
	###########################################
	# global counter
	# global totalCount
	counter  = 1 #renit
	ignoredProteins = [ ]
	for data in insertgenedata_query:
		try:  # any FASTA seqquence that does not have a primary sequence/key in the db gets ignored
			insertstatement =  "INSERT INTO isomorph( isomorphName, isomorphFASTASequence, proteinId ) VALUES ( '" + data[0] + "', '" + data[1] + "', '" + data[2] + "' );" 
			cursor.execute( insertstatement )
		except pymysql.err.IntegrityError:
			print( colored.red( "No primary protein key in db: Ignore: " + insertstatement ) )
			# add protein to list of proteins that need to be looked at: why were they downloaded, if they have nothing to do with our sequences.
			# ignoredProteins.append( proteinId )
			ignoredProteins.append( data[2] )
			continue
		else:
			print( )
			print( colored.magenta( "#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + uniprotFastaDataFile + " (" + str( counter ) + " of " + str( len( uniprotFastaDataFiles ) ) + ") <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" ) )
			print( colored.cyan( insertstatement ) )
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


def insertintoGeneOntology( results ):


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

	ignoredOntologiesQuery = [ ]
	totalCounter = 1; # incremented at the end of the loop
	for protein in results:
		parsedJson = { }
		parsedJson = json.loads( results[protein] )
		counter = 1
		for item in parsedJson:
			bar = re.sub( '_', ' ', item['function_namespace'] )
			insertGoQuery = "INSERT INTO geneOntology( ontologyId, ontologyName, ontologyFunction, biological_process, proteinId ) values ( " + str(item['function_id']) + ', ' + str(item['go_term']) + ', \'' + str(item['function_name']) + '\', \'' +  str(bar) + '\', \'' + str( protein ) + '\' );' 
			try:
				cursor.execute( insertGoQuery )
			except:
				print( colored.magenta( " ( " + str ( counter ) + " of " + str( len( parsedJson ) ) + " ) " ) + colored.red( insertGoQuery ) )
				ignoredOntologiesQuery.append( insertGoQuery )
			else:
				print( colored.magenta( " ( " + str ( counter ) + " of " + str( len( parsedJson ) ) + " )" + "/" + str( totalCounter ) ) + " " + colored.cyan( insertGoQuery ) )
			counter += 1
			totalCounter += 1

	conn.commit( ) #moving the commit out of the loop allows for a somewhat faster execution time, at the price of doing a bulk commit at the end.
	cursor.close( )

	# write failed ongologies entries to disk
	if ignoredOntologiesQuery: 
		ignoredOntologiesFile = "ignoredOntologies.txt"
		print( colored.yellow( "##############################################################################"))
		print( "The following ontologies were ignored. They where written to disk ('" + ignoredOntologiesFile + "'') for follow up: " )
		for item in ignoredOntologiesQuery:
			print( colored.yellow( item ) )
		print( colored.yellow( "##############################################################################"))
		with open( ignoredOntologiesFile, 'w' ) as file:
			for ontology in ignoredOntologiesQuery:
				file.write( ontology )

	###########################################

def callHintkb( result ):
#def callHintkb( result, output, counter, totalCount ):
#def callHintkb( result ):
	hintkbURL = "http://hintkb.ceid.upatras.gr/api/functions/byprotein/"
	URL = hintkbURL + result[0]  # protein is a list of lists, actually
	global counter
	global totalCount

	try:
		response = urllib.request.urlopen( URL )
	except urllib.error.URLError as e:
		print( colored.red(  "Failed: " + URL ) + colored.magenta( "\t( " + str( counter.value ) + " / " + str( totalCount.value ) + " )" ) )
		with counter.get_lock():
			counter.value += 1
	except urllib.error.HTTPError as e: # ignore for now
		variable = ""
	else:
		print( colored.green(  "\t" + URL ) + colored.magenta( "\t( " + str( counter.value ) + " / " + str( totalCount.value ) + " )" ) )
		# {"function_id":17269,"go_term":"0033603","function_name":"positive regulation of dopamine secretion","function_namespace":"biological_process"}
		#output.put( result1 )
		with counter.get_lock():
			counter.value += 1
		return ( result, response.read( ).decode( 'UTF-8' ) )

counter = None
totalCount = None

def init( counterValue, totalValue ):
	''' store the counter for later use '''
	global counter
	global totalCount
	counter = counterValue
	totalCount = totalValue

def hintkb2( ):

	__SINGLETHREADED__ = 0 #turn this into an Debug member variable
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
	# print( str( len ( list ( selectResult ) ) ) )
	# sys.exit( 0 )

#
# The following time is just for data to be retrieved from HintKB2
#
#       20 workers gets us | 50 workers gets us | 100 workers gets us | 150 workers gets us | 200 workers gets us | No workers gets us
# real	      4m44.325s    |       5m53.480s    |        5m40.438s    |        5m42.387s    |        4m29.458s*   |       64m47.450s
# user	      0m10.795s    |       0m13.203s    |        0m14.236s    |        0m17.817s    |        0m19.321s    |        0m10.543s
# sys	      0m5.367s     |       0m6.900s     |        0m7.495s     |        0m10.103s    |        0m11.621s    |        0m4.755s
#
# 																								* dropped HTTP requests
# At 400 processes, there were a lot of failed http requests, possibly more than the successfurl ones
# 		multiprocessing.pool.RemoteTraceback:
#			TimeoutError: [Errno 60] Operation timed out
#		server timed out
#
# At 500 processes, the mac mini gives up the spirit:
#		`BlockingIOError: [Errno 35] Resource temporarily unavailable
#
# maxtasksperchild = 10, real	4m47.476s | maxtasksperchild = 40, 4m40.327s
# prosses = 100, maxtasksperchild = 1 
# prosses = 100, maxtasksperchild = 100


	results   = { }
	dumpfile = 'hintkb.pyc'
	if not os.path.isfile( dumpfile ):
		print( colored.green( "Reading from the internets" ) )
		response  = ""
		if __SINGLETHREADED__:
			print( colored.yellow( "Contacting HintKB2: " + str(len( selectResult )) + " results, using 1 process" ) )
			for result in selectResult:
				callHintkb( result )
		else:
			results = [ ]
			print( colored.yellow( "Contacting HintKB2: " + str(len( selectResult )) + " queries, using multiprocessing.Pool( )" ) )
			counter = Value('i', 1 )
			totalCount = Value( 'i', len( selectResult )  )

			with Pool( processes = 100, initializer = init, initargs = (counter, totalCount ), maxtasksperchild = 1 ) as p: 
				results.append( p.map( callHintkb, selectResult ) )

			# serialize the output
			with open( dumpfile, 'wb' ) as f:
				pickle.dump( obj = results, file = f, protocol = pickle.DEFAULT_PROTOCOL, fix_imports = True )
	else:
		print( colored.green( "Reading results from file '" + dumpfile + "'" )  )
		with open( dumpfile, 'rb' ) as f:
			results = pickle.load( f )

	myhash = {}
	for m in range( len( results ) ):
		for n in range( len( results[m] )):
			if results[m][n]:
				if '[]' not in results[m][n][1]:
					myhash[ results[m][n][0][0] ] = results[m][n][1]

#	for key in myhash:
#		print( "key: " + key + " | value: " + myhash[key] )
# 	for stuff in results:
# 		for value in stuff:
#			for kot in stuff:
# 			key1, key3, key2 = value;
# 			print( colored.cyan( key1 + " -> " + key2 ) )

#	sys.exit( 0 )
	# https://stackoverflow.com/questions/2080660/python-multiprocessing-and-a-shared-counter
	insertintoGeneOntology( myhash )


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

__DEBUG__  = 0
__DEBUG1__ = 0
__DEBUG2__ = 0

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
	disgenet( )
	uniprot( )
	hintkb2( )



if __name__ == "__main__":
	main( )

print( colored.magenta( "\n########################################### END - END - END ###########################################\n") )

