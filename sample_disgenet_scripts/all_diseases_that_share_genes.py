#!/usr/bin/env python3.6

import urllib.request, urllib.error, urllib.parse

query="""
DEFINE
	c0='/data/disease_to_disease_map',
	c1='/data/diseases',
	c2='/data/diseases2',
	c3='/data/genes',
	c4='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c1 (diseaseId, name),
	c2 (type, diseaseClassName),
	c3 (symbol, geneId, description, pantherName),
	c0 (source)
FROM
	c0
WHERE
	(
		c1 = 'C0030567'
	AND
		c4 = 'ALL'
	)"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)
print(res.read().decode('utf-8'))