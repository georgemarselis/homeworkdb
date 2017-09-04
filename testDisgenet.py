#!/opt/local/bin/python3.6

import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError

# orig 
#    c1 (diseaseId, name, hpoName, diseaseId, name, STY, MESH, diseaseClassName, doName, type, OMIM, type, diseaseClassName, STY, diseaseId, name),
#    c0 (score, score, EI, diseaseId, geneId, Npmids, diseaseId, geneId, Npmids, diseaseId, Npmids, geneId, Npmids, Nsnps, source, diseaseId, geneId, Nsnps, source, diseaseId, geneId),
#    c2 (symbol, geneId, symbol, geneId, uniprotId, description, DPI, DSI, pantherName, symbol, geneId),


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
    c1 (sdiseaseId, name, hpoName, STY, MESH, diseaseClassName, doName, type, OMIM ),
    c2 (symbol, geneId, uniprotId, description, DPI, DSI, pantherName ),
    c0 (score, EI, diseaseId, geneId, Npmids, Nsnps, source ),
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

query    = query.encode("utf-8")
request  = urllib.request.Request("http://www.disgenet.org/oql")
response = urllib.request.urlopen( request, query )
print(response.read().decode('utf-8'))
