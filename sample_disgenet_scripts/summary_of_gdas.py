#!/usr/bin/env python3.6

import urllib.request, urllib.error, urllib.parse
import csv

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
	c1 (diseaseId, name, hpoName, STY, MESH, diseaseClassName, doName, type, OMIM ),
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
	)
ORDER BY
	c0.score DESC"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)
print(res.read().decode('utf-8'))

# trying to directly manipulate the data into an array or CVS reader format
#cr = csv.reader(res)
#stuff = res.read().decode('utf-8')  #)
#for row in cr:
#    print( row )
#print( type (stuff ) )