#!/opt/local/bin/python3.4

import pymysql
import csv
import os
import sys
import xml.etree.ElementTree

delimiter  = '\t';

host       = '192.168.1.26';
user       = 'root';
password   = '12345'
db 		   = 'disgenet'
defaultcharset    = 'utf8'
defaultcollation  = 'utf8_general_ci'

##### load data from files

## disgenet
disgenetDataFile = 'disgenet/disgenet_data.tsv'
disgenetFieldNames = ['cui', 'name', 'hpoName', 'omimInt', 'diseaseId', 'STY', 'MESH', 'diseaseClassName', 'type', 'hdoName', 'name', 'geneId', 'uniprotId', 'description', 'pathName', 'pantherName', 'PI', 'PL', 'score', 'pmids', 'snps', 'sourceId', 'numberOfassocDiseases' ]
restkey    = 'unknownkey';
restval    = 'uknownvalue';
dialect    = 'excel-tab';

# read payload
# disgenetCsvfile = open( disgenetDataFile )
# disgenetReader = csv.DictReader( disgenetCsvfile, disgenetFieldNames, restkey, restval, dialect );
# next(disgenetReader, None) # skip the headers

# for row in disgenetReader:
#	print( row )
###########################################


## hintdb
# hintkbDir = './hintkb'
# hintkbDataFiles =  os.listdir( hintkbDir )
# hintkbFieldNames = [ 'uniprot_id1', 'uniprot_id2', 'go_function', 'go_component', 'go_process', 'sequence_similarity', 'coexpression1', 'coexpression2', 'coexpression3', 'coexpression4', 'coexpression5', 'coexpression6', 'coexpression7', 'coexpression8', 'coexpression9', 'coexpression10', 'coexpression11', 'coexpression12', 'coexpression13', 'coexpression14', 'coexpression15', 'localization', 'homology_yeast', 'domain_domain_interaction', 'score', 'hprd_flag' ]
# restkey    = 'unknownkey';
# restval    = 'uknownvalue';
# dialect    = 'excel-tab';

# #read payload
# for hintkbDataFile in hintkbDataFiles: 
# 	hintkbCvsFile =  open( hintkbDir + '/' + hintkbDataFile )
# 	hintkbReader = csv.DictReader( hintkbCvsFile, hintkbFieldNames, restkey, restval, dialect );
# 	next(hintkbReader, None) # skip the headers

# 	print( )
# 	print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + hintkbDataFile + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" )
# 	print( )

# 	for row in hintkbReader:
# 		print( row )
###########################################

##uniprot
uniprotDataFile = 'uniprot/O60260'
e = xml.etree.ElementTree.parse(uniprotDataFile).getroot()
# unitprotFieldNames = ['cui', 'name', 'hpoName', 'omimInt', 'diseaseId', 'STY', 'MESH', 'diseaseClassName', 'type', 'hdoName', 'name', 'geneId', 'uniprotId', 'description', 'pathName', 'pantherName', 'PI', 'PL', 'score', 'pmids', 'snps', 'sourceId', 'numberOfassocDiseases' ]
# restkey    = 'unknownkey';
# restval    = 'uknownvalue';
# dialect    = 'excel-tab';
for atype in e.findall('type'):
    print(atype.get('foobar'))
#read payload
# uniprotCsvFile = open( uniprotDataFile )
# reader = csv.DictReader( csvfile, unitprotFieldNames, restkey, restval, dialect );
# next(reader, None) # skip the headers

# for row in reader:
# 	print( row )
###########################################


exit()

