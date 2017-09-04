#!/opt/local/bin/python3.z6

import urllib.request, urllib.error, urllib.parse

query="""
DEFINE
	c0='/data/gene_disease_summary',
	c1='/data/diseases',
	c2='/data/genes',
	c3='/data/gene_roles',
	c4='/data/gene_to_associated_diseases',
	c5='/data/sources'
ON
	'http://www.disgenet.org/web/DisGeNET'
SELECT
	c1 (cui, name, hpoName, omimInt, diseaseId, STY, MESH, diseaseClassName, type, hdoName ),
	c2 (name, geneId, uniprotId, description, pathName, pantherName ),
	c3 (PI, PL),
	c0 (score, pmids, snps, sourceId ),
	c4 (numberOfassocDiseases)
FROM
	c0
WHERE
	(
		c1 = 'diseaseid:C0030567'
	AND
		c5 = 'ALL'
	AND
		c0.score >= '0.25'
	)
ORDER BY
	c0.score DESC"""

binary_data = query.encode("utf-8")
req = urllib.request.Request("http://www.disgenet.org/oql")
res = urllib.request.urlopen(req, binary_data)
print(res.read().decode('utf-8'))
