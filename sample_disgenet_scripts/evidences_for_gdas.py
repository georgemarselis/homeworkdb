#!/usr/bin/env python3.6

import urllib.request, urllib.error, urllib.parse

query="""
DEFINE
	c0='/data/gene_disease',
	c1='/data/genes',
	c2='/data/diseases',
	c3='/data/gene_disease_summary',
	c4='/data/publication',
	c5='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c0 (source, geneId, associationType, originalSource, sentence, pmid),
	c1 (pantherName, symbol, description ),
	c2 (diseaseId, name, hpoName, STY, MESH, diseaseClassName, doName, type, OMIM ),
	c3 (score),
	c4 (year)
FROM
	c0
WHERE
	(
		c2 = 'C0030567'
	AND
		c5 = 'ALL'
	)
ORDER BY
	c3.score DESC"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)
print(res.read().decode( encoding = 'UTF-8', errors = 'ignore' ) ) #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb5 in position 1120: invalid start byte