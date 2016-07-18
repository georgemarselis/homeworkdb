#!/opt/local/bin/python3.4

import pymysql
import os

host       = '192.168.1.4';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "project2501a_pez2015"

if str(os.environ['PEZ_HOST']):
	host = str(os.environ['PEZ_HOST'])

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