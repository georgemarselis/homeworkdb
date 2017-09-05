#!/opt/local/bin/python3.4

import pymysql
import os

host       = '192.168.1.5';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "project2501a_pez"

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
	print( 'database connection established' )
else:
	print( 'Houston we have a problem' )

conn.begin( )
cursor = conn.cursor( )
#turn this into a stored procedure

cursor.execute( "use " + db )
conn.commit( )

selectQuery = "select gene.geneId, gene.geneName, gene.noPubMedIDs, protein.proteinId from gene inner join protein on gene.geneId = protein.geneId group by gene.geneId order by protein.proteinId;"
cursor.execute( selectQuery )

#substitute for fetchone
for row in cursor:
	print( row )

cursor.close( )
