/* SQLEditor (MySQL (2))*/

CREATE TABLE IF NOT EXISTS gene
(
geneId VARCHAR(10) NOT NULL,
geneName VARCHAR(10) NOT NULL,
disgenetScore FLOAT NOT NULL,
noPubMedIDs INTEGER NOT NULL,
PRIMARY KEY (geneName)
);

CREATE TABLE IF NOT EXISTS geneOntology
(
ontologyId BIGINT NOT NULL,
ontologyName BIGINT NOT NULL,
ontologyFunction VARCHAR(255) NOT NULL,
proteinId VARCHAR(8) NOT NULL,
biological_process VARCHAR(255) NOT NULL,
PRIMARY KEY (ontologyId)
);

CREATE TABLE IF NOT EXISTS protein
(
proteinId VARCHAR(14) NOT NULL,
proteinName TEXT NOT NULL,
proteinConfirmed BOOLEAN NOT NULL,
geneName VARCHAR(10) NOT NULL,
PRIMARY KEY (proteinId)
);

CREATE TABLE IF NOT EXISTS isomorph
(
isomorphName VARCHAR(12) NOT NULL,
isomorphFASTASequence TEXT NOT NULL,
proteinId VARCHAR(8) NOT NULL,
PRIMARY KEY (isomorphName)
);

CREATE TABLE IF NOT EXISTS ProteinGeneOntology
(
proteinId VARCHAR(14) NOT NULL,
ontologyId BIGINT NOT NULL,
PRIMARY KEY (proteinId,ontologyId)
);

ALTER TABLE protein ADD CONSTRAINT Protein2Gene_fk_1 FOREIGN KEY Protein2Gene_fk_1 (geneName) REFERENCES gene (geneName) ON DELETE CASCADE  ON UPDATE CASCADE;

ALTER TABLE isomorph ADD CONSTRAINT isomorph_fk_1 FOREIGN KEY isomorph_fk_1 (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE  ON UPDATE CASCADE;

ALTER TABLE ProteinGeneOntology ADD CONSTRAINT ProteinGeneOntology_fk_2 FOREIGN KEY ProteinGeneOntology_fk_2 (ontologyId) REFERENCES geneOntology (ontologyId) ON DELETE CASCADE  ON UPDATE CASCADE;

ALTER TABLE ProteinGeneOntology ADD CONSTRAINT ProteinGeneOntology_fk_1 FOREIGN KEY ProteinGeneOntology_fk_1 (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE  ON UPDATE CASCADE;
