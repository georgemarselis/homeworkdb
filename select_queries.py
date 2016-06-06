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
selectrelevantgenes_query = 'SELECT geneId, description FROM gene2disease g2d INNER JOIN ( SELECT d.diseaseId, d.diseaseName, d.description FROM disease AS d WHERE d.diseaseName LIKE \'%heimer%\' ) dd ON g2d.diseaseId = dd.diseaseId'
cursor.execute( selectrelevantgenes_query )
row = cursor.fetchone( )
while row is not None:
	print( row )
	row = cursor.fetchone()

# select all the other things!
selectrelevantdiseases_query = "SELECT di.diseaseName FROM disease AS di INNER JOIN ( SELECT g2d.diseaseId FROM gene2disease g2d INNER JOIN ( SELECT g.geneId, g.geneName FROM gene AS g WHERE g.geneName = 'PTEN' ) gg ON g2d.geneId = gg.geneId ) dd ON di.diseaseId = dd.diseaseId "
cursor.execute( selectrelevantdiseases_query )
row = cursor.fetchone( )
while row is not None:
	print( row )
	row = cursor.fetchone()

# FIN
