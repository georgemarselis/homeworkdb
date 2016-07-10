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
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'
tsv_file   = 'out'


##### load data from files

## disgenet
disgenetDataFile = 'disgenet/disgenet_data.tsv'
## hintdb

##uniprot





# connect to db
conn = pymysql.connect( host, user, password, db )
if conn != -1 :
	print( 'database connection established' )
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
createtable_gene_query         = 'create table if not exists gene( geneId varchar(50) not null, geneName varchar(100) not null, primary key (geneId) )'
createtable_disease_query      = 'create table if not exists disease( diseaseId varchar(50) not null, diseaseName varchar(100) not null, description varchar(100) not null, primary key (diseaseId) )'
createtable_gene2disease_query = 'create table if not exists gene2disease ( geneId varchar(50) not null, diseaseId varchar(50) not null, foreign key (geneId) references gene(geneId) on update cascade on delete restrict, foreign key (diseaseId) references disease(diseaseId) on update cascade on delete restrict )'
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
			insertdiseasedata_query = "insert into disease( diseaseId, diseaseName, description ) value ( '" + row['diseaseId'] + "', " + conn.escape(row['diseaseName']) + ", " + conn.escape(row['description']) + " )"
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
