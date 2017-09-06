#!/opt/local/bin/python3.4

import pymysql
import csv
import os
import sys
import xml.etree.ElementTree
import re
import time
import urllib.request
import json
from io  import StringIO
from Bio import SeqIO
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from clint.textui import colored


host       = '192.168.1.5';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "pez_project2501a"

if "PEZ_HOST" in os.environ:
	host = str(os.environ['PEZ_HOST'])
if "PEZ_DATABASE" in os.environ:
	db = str(os.environ['PEZ_DATABASE'])
if "PEZ_USER" in os.environ:
	user = str(os.environ['PEZ_USER'])
if "PEZ_PASSWORD" in os.environ:
	password = str(os.environ['PEZ_PASSWORD'])


# # connect to db
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

##### load data from files
###########################################

print( colored.yellow( "\n########################################### DISGENET -- DISGENET -- DISGENET -- ###########################################\n" ) )

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

kot = 0 # magic to skip the first header row
for row in disgenetReader:
	if kot == 0 :
		kot = 1
		continue
	insertgenedataQuery = " "
	insertgenedataQuery = "INSERT INTO gene( geneId, geneName, disgenetScore, noPubMedIDs ) VALUES ( '" + row['c2.geneId'] + "', '" + row['c2.symbol'] + "', " + row['c0.score'] + ", " + row['c0.Npmids'] +" )"
	print( colored.cyan( insertgenedataQuery ) )
	cursor.execute( insertgenedataQuery )

conn.commit( )
###########################################

sys.exit( 0 )

print( colored.cyan( "\n########################################### UNIPROT -- UNIPROT -- UNIPROT -- ###########################################\n") )


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

# read payload - proteins
###########################################
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
		
		insertgenedata_query = "INSERT INTO protein( proteinId, proteinName, proteinConfirmed, geneId ) VALUES ( '" + row['Entry'] + "', '" + str.upper(row['Protein names']) + "', " + kot + ", '" + geneId +"' )"
		print( colored.white( insertgenedata_query ) )
		cursor.execute( insertgenedata_query )

	conn.commit( )


# read payload - fasta
################
unitprotFieldNames = [ 'fasta sequence', 'name' ]
for uniprotFastaDataFile in uniprotFastaDataFiles: 

	print( )
	print( colored.magenta( "#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + uniprotFastaDataFile + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" ) )
	print( )

	uniprotFastaFile = SeqIO.parse(open( uniprotFastaDir + '/' + uniprotFastaDataFile ) ,'fasta')
	for fasta in uniprotFastaFile:
		name, sequence = fasta.id, fasta.seq.tostring( )
		# sp|O02828|TAU_CAPHI , sp|O02828-2|TAU_CAPHI , tr|A0A151NP48|A0A151NP48_ALLMI
		_, proteinId, isomorphId = name.split( '|', 3 )
		name = proteinId
		if re.search( "-\d+", proteinId ):
			proteinId, _  = proteinId.split( '-', 1 )
		insertgenedata_query = "INSERT INTO isomorph( isomorphName, isomorphFASTASequence, proteinId ) VALUES ( '" + name + "', '" + sequence + "', '" + proteinId + "' );"
		print( colored.white( insertgenedata_query ) )
		cursor.execute( insertgenedata_query )

	conn.commit( )

###########################################

# sys.exit( 0 )

print( colored.cyan( "\n########################################### HINTKB -- HINTKB -- HINTKB -- ###########################################\n") )


## GeneOntology/hintdb
###########################################
#hintkbFieldNames = [ 'function_id', 'go_term', 'function_name', 'function_namespace' ]

# #read payload
selectQuery = "select distinct protein.proteinid from protein order by proteinid"
cursor.execute( selectQuery )
selectResult = cursor.fetchall( )
# print( selectResult )

response = [ ]
hintkbUrl = "http://hintkb.ceid.upatras.gr/api/functions/byprotein/"
for uniprotId in selectResult:
	response = urllib.request.urlopen( hintkbUrl + uniprotId[0] )
	restResult = response.read( ) 
	# {"function_id":17269,"go_term":"0033603","function_name":"positive regulation of dopamine secretion","function_namespace":"biological_process"}
	result =  restResult.decode( 'UTF-8' )
	parsedJson = { }
	parsedJson = json.loads( result )
	if parsedJson:
		for item in parsedJson:
			bar = re.sub( '_', ' ', item['function_namespace'] )
			insertGoQuery = "INSERT INTO geneOntology( ontologyId, ontologyName, ontologyFunction, biological_process, proteinId ) values ( " + str(item['function_id']) + ', ' + str(item['go_term']) + ', \'' + str(item['function_name']) + '\', \'' +  str(bar) + '\', \'' + str(uniprotId[0]) + '\' )' 
			print( colored.white( insertGoQuery ) )
			cursor.execute( insertGoQuery )
			conn.commit( )

cursor.close( )


