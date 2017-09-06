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


#################################################
##
## config variables
##

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

#################################################
##
## running program
##


# # connect to db
conn = pymysql.connect( host, user, password )
if conn != -1 :
	print( colored.green( 'database connection established' ) )
else:
	print( colored.red( 'Houston we have a problem' ) )

dropdb_query = 'drop database if exists ' + db
createdb_query = 'create database ' + db + ' default character set ' +  defaultcharset + ' default collate ' + defaultcollation

print ( colored.yellow( "Creating database schema..." ) )
# # init db
conn.begin( )
cursor = conn.cursor( )
dropdb_query = 'drop database if exists ' + db
print( colored.cyan( dropdb_query ) )
cursor.execute( dropdb_query )
createdb_query = 'create database if not exists ' + db + ' default character set ' +  defaultcharset + ' default collate ' + defaultcollation
print( colored.cyan( createdb_query ) )
cursor.execute( createdb_query )
conn.commit( )

cursor.execute( "use " + db )
conn.commit( )

print( colored.green( "Creating tables..." ) )
# # create tables
createTableGene     = "CREATE TABLE IF NOT EXISTS gene( geneId VARCHAR(11) NOT NULL, geneName VARCHAR(255), disgenetScore FLOAT NOT NULL,noPubMedIDs INTEGER, PRIMARY KEY ( geneId ) )"
createTableProtein  = "CREATE TABLE IF NOT EXISTS protein( proteinId VARCHAR(8) NOT NULL, proteinName TEXT NOT NULL, proteinConfirmed BOOLEAN NOT NULL, geneId VARCHAR(11) NOT NULL, PRIMARY KEY (proteinId) )"
createTableOntology = "CREATE TABLE IF NOT EXISTS geneOntology( ontologyId BIGINT NOT NULL, ontologyName BIGINT NOT NULL, ontologyFunction VARCHAR(255) NOT NULL, biological_process VARCHAR(255) NOT NULL, proteinId VARCHAR(8) NOT NULL, PRIMARY KEY (ontologyId, proteinId) )"
createTableIsomorph = "CREATE TABLE IF NOT EXISTS isomorph ( isomorphName VARCHAR(255) NOT NULL, isomorphFASTASequence TEXT NOT NULL, proteinId VARCHAR(8) NOT NULL, PRIMARY KEY (isomorphName) );"
createTableBullshit = "CREATE TABLE IF NOT EXISTS ProteinGeneOntology( proteinId VARCHAR(8) NOT NULL, ontologyId BIGINT NOT NULL, PRIMARY KEY (proteinId,ontologyId) );"
createViewSequence  = "create algorithm=TEMPTABLE view sequence as select * from isomorph;"
createViewFasta     = "create algorithm=TEMPTABLE view fasta as select * from isomorph;"
createViewIsoform   = "create algorithm=TEMPTABLE view isoform as select * from isomorph;"

print( colored.cyan( createTableGene ) )
cursor.execute( createTableGene )
print( colored.cyan( createTableProtein ) )
cursor.execute( createTableProtein )
print( colored.cyan( createTableOntology ) )
cursor.execute( createTableOntology )
print( colored.cyan( createTableIsomorph ) )
cursor.execute( createTableIsomorph )
print( colored.cyan( createTableBullshit ) )
cursor.execute( createTableBullshit )
print( colored.cyan( createViewSequence ) )
cursor.execute( createViewSequence )
print( colored.cyan( createViewSequence ) )
cursor.execute( createViewFasta )
print( colored.cyan( createViewFasta ) )
cursor.execute( createViewIsoform )
conn.commit( )

print( colored.green(  "Database tables created" ) )


print( colored.green(  "Creating database constraints..." ) )
# # constraints

proteinRestraint              = "ALTER TABLE protein ADD CONSTRAINT Protein2Gene_fk_1 FOREIGN KEY Protein2Gene_fk_1 (geneId) REFERENCES gene (geneId) ON DELETE CASCADE  ON UPDATE CASCADE;"
proteinGeneOntologyRestraint1 = "ALTER TABLE ProteinGeneOntology ADD CONSTRAINT ProteinGeneontology_fk_1 FOREIGN KEY ProteinGeneontology_fk_1 (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE  ON UPDATE CASCADE;"
ProteinGeneOntologyRestraint2 = "ALTER TABLE ProteinGeneOntology ADD CONSTRAINT ProteinGeneontology_fk_2 FOREIGN KEY ProteinGeneontology_fk_2 (ontologyId) REFERENCES geneOntology (ontologyId) ON DELETE CASCADE  ON UPDATE CASCADE;"
isomorphRestraint             = "ALTER TABLE isomorph ADD CONSTRAINT isomorph_fk_1 FOREIGN KEY isomorph_fk_1 (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE  ON UPDATE CASCADE;"

print( colored.cyan( proteinRestraint ) )
cursor.execute( proteinRestraint )                          #1
print( colored.cyan( proteinGeneOntologyRestraint1 ) )
cursor.execute( proteinGeneOntologyRestraint1 )             #2
print( colored.cyan( ProteinGeneOntologyRestraint2 ) )
cursor.execute( ProteinGeneOntologyRestraint2 )             #3
print( colored.cyan( isomorphRestraint ) )
cursor.execute( isomorphRestraint )                         #4
conn.commit( )
cursor.close( )
print( colored.green( "Database constraints created" ) )

print ( colored.green( 'Database schema created' ) )

