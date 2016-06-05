#!/opt/local/bin/python3.4

import pymysql
import csv 


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
	#getTest(conn)
	#setTest(conn)
	#conn.close
else:
	print( 'Houston we have a problem' )

# init db
conn.begin( )
cursor = conn.cursor( )
dropdb_query = 'drop database if exists ' + db
createdb_query = 'create database ' + db + ' default character set ' +  defaultcharset + ' default collate ' + defaultcollation
cursor.execute( dropdb_query )
cursor.execute( createdb_query )
conn.commit( )
# init tables
droptable_query                = 'drop table if exists gene2disease, gene, disease'
createtable_gene_query         = 'create table if not exists gene( geneId varchar(20) not null, geneName varchar(50) not null, primary key (geneId) )'
createtable_disease_query      = 'create table if not exists disease( diseaseId varchar(20) not null, diseaseName varchar(50) not null, primary key (diseaseId) )'
createtable_gene2disease_query = 'create table if not exists gene2disease ( geneId varchar(20) not null, diseaseId varchar(20) not null, foreign key (geneId) references gene(geneId) on update cascade on delete restrict, foreign key (diseaseId) references disease(diseaseId) on update cascade on delete restrict )'
cursor.execute( "use " + db )
print( droptable_query )
cursor.execute( droptable_query )
print( createtable_gene_query )
cursor.execute( createtable_gene_query )
print( createtable_gene_query )
cursor.execute( createtable_disease_query )
print( createtable_gene2disease_query )
cursor.execute( createtable_gene2disease_query )
conn.commit( )

# insert payload
with open( tsv_file ) as csvfile:
	reader = csv.DictReader( csvfile, fieldnames, restkey, restval, dialect );
	next(reader, None) # skip the headers
	gene_keys    = [ ]
	disease_keys = [ ]

	for row in reader:
		if row['geneId'] not in gene_keys:
			gene_keys.append( row['geneId'] )
			previous_gene_key = row['geneId']
			insertgenedata_query = "insert into gene( geneId, geneName ) value ( '" + row['geneId'] + "', '" + row['geneName'] + "' )"
			print( insertgenedata_query )
			cursor.execute( insertgenedata_query )

		if row['diseaseId'] not in disease_keys: 
			disease_keys.append( row['diseaseId'] )
			insertdiseasedata_query = "insert into disease( diseaseId, diseaseName ) value ( '" + row['diseaseId'] + "', '" + row['geneName'] + "' )"
			print( insertdiseasedata_query )
			cursor.execute( insertdiseasedata_query )
		cursor.execute( "insert into gene2disease( geneId, diseaseId ) value ( '" + row['geneId'] + "', '" + row['diseaseId'] + "' )" )

	conn.commit( )
	cursor.close( )
	exit( )


# select gene and diseases
conn.begin( )
cursor = conn.cursor( )
selectgene_query = ""
selectdiseasedata_query = ""
cursor.execute( selectgene_query )
cursor.execute( selectdiseasedata_query )
conn.commit( )
cursor.close( )



# def connectdb( ):
# #	database  = 'disgenet'
# 	return pymysql.connect( host, user, password, database )

# def getTest( conn ):
# 	conn.begin( )
# 	cursor = conn.cursor( )
# 	select_query = 'select * from test'
# 	cursor.execute( select_query )
# 	results = cursor.fetchall( )
# 	if len(results) > 0:
# 		print( results );
# 		print( 'Connection established.' )
# 	cursor.close( )

# def setTest( conn ):
# 	conn.begin( )
# 	cursor = conn.cursor( )
# 	insert_query = 'insert into test values( null, \'Hello3\')'
# 	cursor.execute( insert_query )
# 	conn.commit( )
# 	cursor.close( )

# def file_len(fname):
# 	i = 0;
# 	with open(fname) as f:
# 		i = sum(1 for _ in f);
# 	return i + 1; 
