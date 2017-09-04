import urllib.request, urllib.error, urllib.parse

query="""
DEFINE
	c0='/data/variant_disease',
	c1='/data/variants',
	c2='/data/diseases',
	c3='/data/variant_disease_summary',
	c4='/data/publication',
	c5='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c1 (coord, symbol, geneId, AF_1000G, class, snpId, AF_EXAC, most_severe_consequence),
	c2 (hpoName, diseaseId, name, STY, MESH, diseaseClassName, doName, type, OMIM, diseaseId, name),
	c3 (score),
	c0 (originalSource, sentence, pmid),
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
print(res.read().decode('utf-8'))