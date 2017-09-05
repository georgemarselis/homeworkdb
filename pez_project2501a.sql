/* SQLEditor (MySQL (2))*/

drop database if exists pez_project2501a;

create database pez_project2501a default character set utf8 default collate utf8_general_ci;

CREATE TABLE IF NOT EXISTS gene
(
geneId VARCHAR(11) NOT NULL,
geneName VARCHAR(255) NOT NULL,
disgenetScore FLOAT NOT NULL,
noPubMedIDs INTEGER NOT NULL,
PRIMARY KEY (geneId)
);

CREATE TABLE IF NOT EXISTS geneOntology
(
ontologyId BIGINT NOT NULL,
ontologyName BIGINT NOT NULL,
ontologyFunction VARCHAR(255) NOT NULL,
proteinId VARCHAR(8) NOT NULL,
biological_process VARCHAR(255) NOT NULL,
PRIMARY KEY (ontologyId,proteinId)
);

CREATE TABLE IF NOT EXISTS protein
(
proteinId VARCHAR(8) NOT NULL,
proteinName TEXT NOT NULL,
proteinConfirmed BOOLEAN NOT NULL,
geneId VARCHAR(11) NOT NULL,
PRIMARY KEY (proteinId)
);

CREATE TABLE IF NOT EXISTS ProteinGeneontology
(
proteinId VARCHAR(8),
ontologyId BIGINT
);

CREATE TABLE IF NOT EXISTS isomorph
(
isomorphName VARCHAR(12) NOT NULL,
isomorphFASTASequence TEXT NOT NULL,
proteinId VARCHAR(8) NOT NULL,
PRIMARY KEY (isomorphName)
);

/*Foreign Key geneOntology geneOntology_fk_1 not exportable, No Target Table*/
ALTER TABLE protein ADD CONSTRAINT Protein2Gene_fk_1 FOREIGN KEY Protein2Gene_fk_1 (geneId) REFERENCES gene (geneId) ON DELETE CASCADE  ON UPDATE CASCADE;

ALTER TABLE ProteinGeneontology ADD CONSTRAINT ProteinGeneontology_fk_1 FOREIGN KEY ProteinGeneontology_fk_1 (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE  ON UPDATE CASCADE;

ALTER TABLE ProteinGeneontology ADD CONSTRAINT ProteinGeneontology_fk_2 FOREIGN KEY ProteinGeneontology_fk_2 (ontologyId) REFERENCES geneOntology (ontologyId) ON DELETE CASCADE  ON UPDATE CASCADE;

ALTER TABLE isomorph ADD CONSTRAINT isomorph_fk_1 FOREIGN KEY isomorph_fk_1 (proteinId) REFERENCES protein (proteinId) ON DELETE CASCADE  ON UPDATE CASCADE;
