#!/usr/bin/env python3

import GEOparse

gds = GEOparse.get_GEO(geo="GDS2519")

gds.table.to_csv('gds2619.tsv', '\t')
