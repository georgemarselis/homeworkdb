#!/usr/bin/env python3.6

import urllib.request, urllib.error, urllib.parse

query="""
DEFINE
	c0='/data/disease_to_diseasegenenumber',
	c1='/data/diseases',
	c2='/data/diseases2',
	c3='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c1 (diseaseId, name),
	c2 (type, diseaseClassName),
	c0 (Ngenes, diseaseId2, source)
FROM
	c0
WHERE
	(
		c1 = 'C0030567'
	AND
		c3 = 'ALL'
	)
ORDER BY
	c0.Ngenes DESC"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)
print(res.read().decode('utf-8'))