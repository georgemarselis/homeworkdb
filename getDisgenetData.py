#!/usr/bin/env python3.4

import sys
import urllib.request, urllib.error, urllib.parse
import pandas
import numpy
import csv
from clint.textui import colored

# 	c1 (diseaseId, name, hpoName, STY, MESH, diseaseClassName, doName, type, OMIM ),

query="""
DEFINE
	c0='/data/gene_disease_summary',
	c1='/data/diseases',
	c2='/data/genes',
	c3='/data/gene_to_associated_diseases',
	c4='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c1 (diseaseId, OMIM ),
	c2 (symbol, geneId, uniprotId, description, pantherName ),
	c0 (score, Npmids, Nsnps ),
	c3 (Ndiseases)
FROM
	c0
WHERE
	(
		c1 = 'C0030567'
	AND
		c4 = 'ALL'
	AND
		c0.score > '0.25'
	)
ORDER BY
	c0.score DESC"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)

csvresults = res.read().decode( 'utf-8' )

print( colored.green( csvresults ) )

disgenetDataFile = 'disgenet/disgenet_data.tsv'
with open( disgenetDataFile, 'w' ) as file:
		for row in csvresults:
			file.write( row )

## disgenet
###########################################
disgenetDataFile = 'disgenet/disgenet_data.tsv'
disgenetFieldNames = [ 'c1.diseaseId', 'c1.OMIM', 'c2.symbol', 'c2.geneId', 'c2.uniprotId', 'c2.description', 'c2.pantherName', 'c0.score', 'c0.Npmids', 'c0.Nsnps', 'c3.Ndiseases' ]
restkey    = 'unknownkey';
restval    = 'uknownvalue';
dialect    = 'excel-tab';

# read payload
###########################################
disgenetCsvfile = open( disgenetDataFile )
disgenetReader = csv.DictReader( disgenetCsvfile, disgenetFieldNames, restkey, restval, dialect );

array = []
kot = 0 # magic to skip the first header row
for row in disgenetReader:
	if kot == 0 :
		kot = 1
		continue
	if row['c2.symbol'] not in array:
		array.append( row['c2.symbol'] )

print( "Array of genes to be writen to disk: " + colored.yellow( array ) )

listOfGenes = 'listOfGenes.tsv'
with open( listOfGenes, 'w' ) as file:
	file.write( '\n'.join( array ) )
