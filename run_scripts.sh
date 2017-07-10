#!/bin/bash

./getGenesPublications.py 
./getProteinsIsoformsCount.py
./getProteinExperimentalVerified.py
./getGeneByScore.py -s .4
./getProteinFunctions.py
./getProteinsByFunction.py -F E
./getProteinIsoformCountByPubsCount.py -p 2
./getGeneByIsoformSequence.py -S E
./getProteinsFunctionByNamespace.py -N E
./getGenesIsoformsCountBySequence.py -s E