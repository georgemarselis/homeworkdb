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



host       = '192.168.1.4';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "pez_project2501a"

if str(os.environ['PEZ_HOST']):
	host = str(os.environ['PEZ_HOST'])
if str(os.environ['PEZ_DATABASE'] ):
	db = str(os.environ['PEZ_DATABASE'])
if str(os.environ['PEZ_USER'] ):
	user = str(os.environ['PEZ_USER'])
if str(os.environ['PEZ_PASSWORD'] ):
	password = str(os.environ['PEZ_PASSWORD'])


# # connect to db
conn = pymysql.connect( host, user, password )
if conn != -1 :
	print( 'database connection established' )
else:
	print( 'Houston we have a problem' )

dropdb_query = 'drop database if exists ' + db
createdb_query = 'create database ' + db + ' default character set ' +  defaultcharset + ' default collate ' + defaultcollation

# # init db
conn.begin( )
cursor = conn.cursor( )
dropdb_query = 'drop database if exists ' + db
print( dropdb_query )
cursor.execute( dropdb_query )
createdb_query = 'create database if not exists ' + db + ' default character set ' +  defaultcharset + ' default collate ' + defaultcollation
print( createdb_query )
cursor.execute( createdb_query )
conn.commit( )

cursor.execute( "use " + db )
conn.commit( )

# # clean tables if exist
droptable_query     = "drop table if exists isomorph, geneOntology, protein, gene"
print( droptable_query )
cursor.execute( droptable_query )
conn.commit( )
# # create tables
createTableGene     = "CREATE TABLE IF NOT EXISTS gene( geneId VARCHAR(255) NOT NULL, geneName VARCHAR(255), disgenetScore FLOAT NOT NULL,noPubMedIDs INTEGER, PRIMARY KEY (geneId) )"
createTableProtein  = "CREATE TABLE IF NOT EXISTS protein( proteinId VARCHAR(255) NOT NULL, proteinName TEXT NOT NULL, proteinConfirmed BOOLEAN NOT NULL, geneId VARCHAR(255) NOT NULL, PRIMARY KEY (proteinId) )"
createTableOntology = "CREATE TABLE IF NOT EXISTS geneOntology( ontologyId BIGINT NOT NULL, ontologyName BIGINT NOT NULL, ontologyFunction VARCHAR(255) NOT NULL, biological_process VARCHAR(255) NOT NULL, proteinId VARCHAR(255) NOT NULL, PRIMARY KEY (ontologyId, proteinId) )"
createTableIsomorph = "CREATE TABLE IF NOT EXISTS isomorph ( isomorphName VARCHAR(255) NOT NULL, isomorphFASTASequence TEXT NOT NULL, proteinId VARCHAR(255) NOT NULL, PRIMARY KEY (isomorphName) );"
createViewSequence  = "create algorithm=TEMPTABLE view sequence as select * from isomorph;"
createViewFasta     = "create algorithm=TEMPTABLE view fasta as select * from isomorph;"
createViewIsoform   = "create algorithm=TEMPTABLE view isoform as select * from isomorph;"

print( createTableGene )
cursor.execute( createTableGene )
print( createTableProtein )
cursor.execute( createTableProtein )
print( createTableOntology )
cursor.execute( createTableOntology )
print( createTableIsomorph )
cursor.execute( createTableIsomorph )
print( createViewSequence )
cursor.execute( createViewSequence )
print( createViewSequence )
cursor.execute( createViewFasta )
print( createViewFasta )
cursor.execute( createViewIsoform )
conn.commit( )


# # constraints
geneOntologyRestraint = "ALTER TABLE geneOntology ADD CONSTRAINT geneOntology_fk_1 FOREIGN KEY (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE ON UPDATE CASCADE"
isomorphRestraint     = "ALTER TABLE isomorph ADD CONSTRAINT Isomorph_fk_1 FOREIGN KEY (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE ON UPDATE CASCADE"
proteinRestraint      = "ALTER TABLE protein ADD CONSTRAINT Protein2Gene_fk_1 FOREIGN KEY (geneId) REFERENCES gene (geneId) ON DELETE CASCADE ON UPDATE CASCADE"

print( geneOntologyRestraint )
cursor.execute( geneOntologyRestraint )
print( isomorphRestraint )
cursor.execute( isomorphRestraint )
print( proteinRestraint )
cursor.execute( proteinRestraint )
conn.commit( )

##### load data from files
###########################################

print( "\n########################################### DISGENET -- DISGENET -- DISGENET -- ###########################################\n")

## disgenet
###########################################
disgenetDataFile = 'disgenet/disgenet_data.tsv'
disgenetFieldNames = [ 'c1.cui', 'c1.name', 'c1.hpoName', 'c1.omimInt', 'c1.diseaseId', 'c1.STY', 'c1.MESH', 'c1.diseaseClassName', 'c1.type', 'c1.hdoName', 'c2.name', 'c2.geneId', 'c2.uniprotId', 'c2.description', 'c2.pathName', 'c2.pantherName', 'c3.PI', 'c3.PL', 'c0.score', 'c0.pmids', 'c0.snps', 'c0.sourceId', 'c4.numberOfassocDiseases' ]
restkey    = 'unknownkey';
restval    = 'uknownvalue';
dialect    = 'excel-tab';

# read payload
###########################################
disgenetCsvfile = open( disgenetDataFile )
disgenetReader = csv.DictReader( disgenetCsvfile, disgenetFieldNames, restkey, restval, dialect );
kotikot = 0 ;
koko = ""
for row in disgenetReader:
	if kotikot == 0 :
			kotikot = 1
			continue
	insertgenedataQuery = " "
	if row['c2.pathName'] == 'null':
		insertgenedataQuery = "INSERT INTO gene( geneId, geneName, disgenetScore, noPubMedIDs ) VALUES ( '" + row['c2.name'] + "', NULL, " + row['c0.score'] + ", " + row['c0.pmids'] +" )"
	else:
		insertgenedataQuery = "INSERT INTO gene( geneId, geneName, disgenetScore, noPubMedIDs ) VALUES ( '" + row['c2.name'] + "', '" + row['c2.pathName'] + "', " + row['c0.score'] + ", " + row['c0.pmids'] +" )"
	print( insertgenedataQuery )
	cursor.execute( insertgenedataQuery )

conn.commit( )
###########################################


print( "\n########################################### UNIPROT -- UNIPROT -- UNIPROT -- ###########################################\n")


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
		print( insertgenedata_query )
		cursor.execute( insertgenedata_query )

	conn.commit( )


# read payload - fasta
################
unitprotFieldNames = [ 'fasta sequence', 'name' ]
for uniprotFastaDataFile in uniprotFastaDataFiles: 

	print( )
	print( "#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + uniprotFastaDataFile + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" )
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
		print( insertgenedata_query )
		cursor.execute( insertgenedata_query )

	conn.commit( )
###########################################


print( "\n########################################### HINTKB -- HINTKB -- HINTKB -- ###########################################\n")


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
			print( insertGoQuery )
			cursor.execute( insertGoQuery )
			conn.commit( )

cursor.close( )


