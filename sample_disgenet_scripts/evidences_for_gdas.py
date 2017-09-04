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
	c0 (source, geneId, source, geneId, source, geneId, associationType, originalSource, originalSource, originalSource, sentence, pmid),
	c1 (pantherName, symbol, geneId, description, symbol, geneId),
	c2 (diseaseId, name, hpoName, diseaseId, name, STY, MESH, diseaseClassName, doName, type, OMIM, type),
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
print(res.read().decode('utf-8'))