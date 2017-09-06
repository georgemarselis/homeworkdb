#!/usr/bin/env python3.4

import urllib.request, urllib.error, urllib.parse
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
	c1 (diseaseId, name, STY, MESH, diseaseClassName, doName, type, OMIM ),
	c2 (symbol, geneId, uniprotId, description, DPI, DSI, pantherName ),
	c0 (score, EI, Npmids, Nsnps, source ),
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