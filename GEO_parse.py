#!/opt/local/bin/python3.4

import sys
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
import GEOparse
import pandas
import numpy



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


gds = GEOparse.get_GEO(geo="GDS2519")

gds.table.to_csv('gds2619.tsv', '\t')


file = 'gds2619.tsv'
df = pandas.read_csv(file)

columns = df.columns

query = ""
query_head = "CREATE TABLE IF NOT EXISTS gene_expression( "
query_body1 = ""
query_body2 = ""
query_tail = "' );"

magickot = 0
for col in columns:
	if magickot = 0:
		query_body1 = query_body1 + col.values + " INT NOT NULL, "
		magickot = 1
	query_body1 = query_body1 + ""

createTableGene     = "CREATE TABLE IF NOT EXISTS gene( geneId VARCHAR(10) NOT NULL, geneName VARCHAR(10) NOT NULL, disgenetScore FLOAT NOT NULL, noPubMedIDs INTEGER NOT NULL, PRIMARY KEY (geneName) );"
insertgenedata_query = "INSERT INTO protein( proteinId, proteinName, proteinConfirmed, geneName ) VALUES ( '" + row['Entry'] + "', '" + str.upper(row['Protein names']) + "', " + kot + ", '" + geneId +"' )"

query = query_head + query_body1 + query_body2 + query_tail
print( colored.cyan( query ))

sys.exit( 0 )
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
