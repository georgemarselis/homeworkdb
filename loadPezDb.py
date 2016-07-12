#!/opt/local/bin/python3.4

import pymysql
import csv
import os
import sys
import xml.etree.ElementTree
from Bio import SeqIO


delimiter  = '\t';

host       = '192.168.1.26';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "pez2015_project2501a"

# # connect to db
conn = pymysql.connect( host, user, password, db )
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
createdb_query = 'create database ' + db + ' default character set ' +  defaultcharset + ' default collate ' + defaultcollation
cursor.execute( dropdb_query )
cursor.execute( createdb_query )
conn.commit( )

cursor.execute( "use " + db )

# # clean tables if exist
droptable_query     = "drop table if exists isomorph, geneOntology, protein, gene"
print( droptable_query )
cursor.execute( droptable_query )
conn.commit( )

# # create tables
createTableGene     = "CREATE TABLE IF NOT EXISTS gene( geneId VARCHAR(255) NOT NULL, geneName VARCHAR(255) NOT NULL, disgenetScore FLOAT NOT NULL,noPubMedIDs INTEGER, PRIMARY KEY (geneId) )"
createTableOntology = "CREATE TABLE IF NOT EXISTS geneOntology( ontologyId VARCHAR(255) NOT NULL, ontologyName VARCHAR(255) NOT NULL, ontologyFunction VARCHAR(255) NOT NULL, proteinId VARCHAR(255) NOT NULL, PRIMARY KEY (ontologyId) )"
createTableIsomorph = "CREATE TABLE IF NOT EXISTS isomorph(isomorphId VARCHAR(255) NOT NULL, isomorphName VARCHAR(255) NOT NULL, isomorphFASTASequence TEXT NOT NULL, proteinId VARCHAR(255) NOT NULL, PRIMARY KEY (isomorphId) )"
createTableProtein  = "CREATE TABLE IF NOT EXISTS protein( proteinId VARCHAR(255) NOT NULL, proteinName VARCHAR(255) NOT NULL, proteinConfirmed BOOLEAN NOT NULL, geneId VARCHAR(255) NOT NULL, PRIMARY KEY (proteinId) )"

print( createTableGene )
cursor.execute( createTableGene )
print( createTableOntology )
cursor.execute( createTableOntology )
print( createTableIsomorph )
cursor.execute( createTableIsomorph )
print( createTableProtein )
cursor.execute( createTableProtein )
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


## disgenet
###########################################
disgenetDataFile = 'disgenet/disgenet_data.tsv'
disgenetFieldNames = ['cui', 'name', 'hpoName', 'omimInt', 'diseaseId', 'STY', 'MESH', 'diseaseClassName', 'type', 'hdoName', 'name', 'geneId', 'uniprotId', 'description', 'pathName', 'pantherName', 'PI', 'PL', 'score', 'pmids', 'snps', 'sourceId', 'numberOfassocDiseases' ]
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
	insertgenedata_query = "insert into gene( geneId, geneName, disgenetScore, noPubMedIDs ) value ( '" + row['geneId'] + "', '" + row['pathName'] + "', '" + row['score'] + "', '" + row['pmids'] +"' )"
	print( insertgenedata_query )
	cursor.execute( insertgenedata_query )

conn.commit( )
###########################################


## hintdb
###########################################
hintkbDir = './hintkb'
hintkbDataFiles =  os.listdir( hintkbDir )
hintkbFieldNames = [ 'uniprot_id1', 'uniprot_id2', 'go_function', 'go_component', 'go_process', 'sequence_similarity', 'coexpression1', 'coexpression2', 'coexpression3', 'coexpression4', 'coexpression5', 'coexpression6', 'coexpression7', 'coexpression8', 'coexpression9', 'coexpression10', 'coexpression11', 'coexpression12', 'coexpression13', 'coexpression14', 'coexpression15', 'localization', 'homology_yeast', 'domain_domain_interaction', 'score', 'hprd_flag' ]
restkey    = 'unknownkey';
restval    = 'uknownvalue';
dialect    = 'excel-tab';

#read payload
for hintkbDataFile in hintkbDataFiles: 
	hintkbCvsFile =  open( hintkbDir + '/' + hintkbDataFile )
	hintkbReaderFiles = csv.DictReader( hintkbCvsFile, hintkbFieldNames, restkey, restval, dialect );
	for hintkbReaderFile in hintkbReaderFiles:
		next(hintkbReader, None) # skip the headers

	# print( )
	# print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + hintkbDataFile + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" )
	# print( )

	# for row in hintkbReader:
	# 	print( row )
###########################################


##uniprot
uniprotProteinsDir      = './uniprot/proteins'
uniprotFastaDir         = './uniprot/fasta'
uniprotProteinDataFiles = os.listdir( uniprotProteinsDir )
uniprotFastaDataFiles   = os.listdir( uniprotFastaDir )
unitprotFieldNames = [ 'Entry', 'Entry name', 'Protein names', 'Status', 'Gene names  (primary )']
restkey    = 'unknownkey';
restval    = 'uknownvalue';
dialect    = 'excel-tab';

# # read payload
# for uniprotProteinDataFile in uniprotProteinDataFiles: 
# 	uniprotCsvFile = open( uniprotProteinsDir + '/' + uniprotProteinDataFile )
# 	reader = csv.DictReader( uniprotCsvFile, unitprotFieldNames, restkey, restval, dialect );
# 	for row in reader:
# 		next(reader, None) # skip the headers
# 		kot = "FALSE"
# 		if row['Status'] == "reviewed":
# 			kot = "TRUE"
# 		insertgenedata_query = "insert into protein( proteinId, proteinName, proteinConfirmed, geneId ) value ( '" + row['Entry'] + "', '" + row['Protein names'] + "', '" + kot + "', '" + str.upper(row['Gene names  (primary )']) +"' )"
# 		print( insertgenedata_query )
# 		cursor.execute( insertgenedata_query )

# conn.commit( )

exit( )

# unitprotFieldNames = [ 'fasta sequence', 'name' ]
# for uniprotFastaDataFile in uniprotFastaDataFiles: 
# 	uniprotFastaFile = SeqIO.parse(open( uniprotFastaDir + '/' + uniprotFastaDataFile ) ,'fasta')
# 	for fasta in uniprotFastaFile:
# 		name, sequence = fasta.id, fasta.seq # .tostring() implied
# 	# 	print( "Name: " + name )
	# 	print( "Sequence: " + sequence)


	# print( )
	# print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + uniprotFastaDataFile + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" )
	# print( )

	# for row in reader:
	# 	print( row )

###########################################


cursor.close( )

exit()

