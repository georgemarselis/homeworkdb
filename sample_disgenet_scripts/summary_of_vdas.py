import urllib.request, urllib.error, urllib.parse

query="""
DEFINE
	c0='/data/variant_disease_summary',
	c1='/data/diseases',
	c2='/data/variants',
	c3='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c0 (snpId, score, EI, snpId, source, diseaseId, Npmids),
	c1 (diseaseId, name, hpoName, diseaseId, name, STY, MESH, diseaseClassName, doName, type, OMIM),
	c2 (DSI, DPI, chromosome, coord, most_severe_consequence, REF_ALT, class, AF_EXAC, AF_1000G)
FROM
	c0
WHERE
	(
		c1 = 'C0030567'
	AND
		c3 = 'ALL'
	)
ORDER BY
	c0.score DESC"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)
print(res.read().decode('utf-8'))