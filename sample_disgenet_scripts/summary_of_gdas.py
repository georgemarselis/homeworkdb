import urllib.request, urllib.error, urllib.parse

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
	c1 (diseaseId, name, hpoName, diseaseId, name, STY, MESH, diseaseClassName, doName, type, OMIM, type, diseaseClassName, STY, diseaseId, name),
	c2 (symbol, geneId, symbol, geneId, uniprotId, description, DPI, DSI, pantherName, symbol, geneId),
	c0 (score, score, EI, diseaseId, geneId, Npmids, diseaseId, geneId, Npmids, diseaseId, Npmids, geneId, Npmids, Nsnps, source, diseaseId, geneId, Nsnps, source, diseaseId, geneId),
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