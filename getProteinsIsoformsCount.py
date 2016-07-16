#!/opt/local/bin/python3.4

import pymysql


host       = '192.168.1.4';
user       = 'root';
password   = '12345'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'


db = "pez2015_project2501a"

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

selectQuery = "select isomorph.proteinid, count( isomorph.isomorphFASTASequence ) from isomorph group by proteinId;"
cursor.execute( selectQuery )

#substitute for fetchone
for row in cursor:
	print( row )

cursor.close( )