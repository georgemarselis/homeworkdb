#!/opt/local/bin/python3.4

import pymysql
import csv 


fieldnames = ['geneId', 'geneName', 'description', 'diseaseId', 'diseaseName', 'score', 'NofPmids', 'NofSnps', 'sources' ];
restkey    = 'unknownkey';
restval    = 'uknownvalue';
delimiter  = '\t';
dialect    = 'excel-tab';

def file_len(fname):
	i = 0;
	with open(fname) as f:
		i = sum(1 for _ in f);
	return i + 1; 

def connectdb( ):
	host      = '192.168.1.26';
	user      = 'root';
	password  = '12345'
	database  = 'project2501a_nosokomio'
	collation = 'utf8_general_ci'
	return pymysql.connect( host, user, password, database ) #, collation )

def getTest( conn ):
	conn.begin( )
	cursor = conn.cursor( )
	select_query = 'select * from test'
	cursor.execute( select_query )
	results = cursor.fetchall( )
	if len(results) > 0:
		print( results );
		print( "Connection established." )
	cursor.close( )

def setTest( conn ):
	conn.begin( )
	cursor = conn.cursor( )
	insert_query = "insert into test values( null, 'Hello3')"
	cursor.execute( insert_query )
	conn.commit( )
	cursor.close( )

if __name__ == '__main__':
	conn = connectdb( )
	if conn == -1 :
		print( "db connection established")
		getTest(conn)
		setTest(conn)
		conn.close
	else:
		print( "Houston we have a problem")

with open( 'all_gene_disease_associations.tsv' ) as csvfile:
	reader = csv.DictReader( csvfile, fieldnames, restkey, restval, dialect );
	next(reader, None) # skip the headers
	size         = file_len('./all_gene_disease_associations.tsv')
	payload      = [ [0 for x in range(5)] for y in range(size) ];
	genes        = [ [0 for x in range(5)] for y in range(size) ];
	diseases     = [ [0 for x in range(5)] for y in range(size) ];
	gene2disease = [ [0 for x in range(5)] for y in range(size) ];

	counter = 0;
	for row in reader:
		payload[ counter ]       = [ row['geneId'], row['geneName'], row['diseaseId'], row['diseaseName'], row['score'] ];
		genes[ counter ]         = [ row['geneId'], row['geneName'] ];
		diseases[ counter ]      = [ row['diseaseId'], row['diseaseName'] ];
		gene2disease[ counter ]  = [ row['geneId'], row['diseaseId'], row['score'] ];
		#print( counter, array [ counter] );
		counter += 1;
	print( len( payload ) );

# connect to db
# init db
# init tables
# insert payload


