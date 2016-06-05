#!/opt/local/bin/python3.4

import pymysql

fieldnames = ['geneId', 'geneName', 'description', 'diseaseId', 'diseaseName', 'score', 'NofPmids', 'NofSnps', 'sources' ];
restkey    = 'unknownkey';
restval    = 'uknownvalue';
delimiter  = '\t';
dialect    = 'excel-tab';
host       = '192.168.1.26';
user       = 'root';
password   = '12345'
db 		   = 'disgenet'
defaultcollation  = 'utf8_general_ci'
defaultcharset    = 'utf8'
tsv_file   = 'out'


# connect to db
conn = pymysql.connect( host, user, password, db )
if conn != -1 :
	print( 'database connection established' )
else:
	print( 'Houston we have a problem' )

conn.begin( )
cursor = conn.cursor( )
cursor.execute( "use " + db )

# select all the things!
selectrelevantgenes_query = ""
results = cursor.fetchall( selectrelevantgenes_query );
print( results );
cursor.commit( )

# select all the other things!
selectrelevantdiseases_query = ""
results = cursor.fetchall( selectdiseases_query );
print( results );
cursor.commit( )
cursor.close( )

# FIN
