/* SQLEditor (MySQL (2))*/

CREATE TABLE IF NOT EXISTS gene
(
geneId VARCHAR(10) NOT NULL,
geneName VARCHAR(10) NOT NULL,
disgenetScore FLOAT NOT NULL,
noPubMedIDs INTEGER NOT NULL,
PRIMARY KEY (geneName)
);

CREATE TABLE IF NOT EXISTS gene_expression
(
id INTEGER NOT NULL AUTO_INCREMENT,
ID_REF VARCHAR(24) NOT NULL,
GSM153405 FLOAT NOT NULL, 
GSM153406 FLOAT NOT NULL, 
GSM153419 FLOAT NOT NULL, 
GSM153423 FLOAT NOT NULL, 
GSM153425 FLOAT NOT NULL, 
GSM153427 FLOAT NOT NULL, 
GSM153428 FLOAT NOT NULL, 
GSM153429 FLOAT NOT NULL, 
GSM153433 FLOAT NOT NULL, 
GSM153444 FLOAT NOT NULL, 
GSM153448 FLOAT NOT NULL, 
GSM153451 FLOAT NOT NULL, 
GSM153452 FLOAT NOT NULL, 
GSM153477 FLOAT NOT NULL, 
GSM153479 FLOAT NOT NULL, 
GSM153484 FLOAT NOT NULL, 
GSM153488 FLOAT NOT NULL, 
GSM153496 FLOAT NOT NULL, 
GSM153497 FLOAT NOT NULL, 
GSM153500 FLOAT NOT NULL, 
GSM153503 FLOAT NOT NULL, 
GSM153508 FLOAT NOT NULL, 
GSM153409 FLOAT NOT NULL, 
GSM153426 FLOAT NOT NULL, 
GSM153431 FLOAT NOT NULL, 
GSM153438 FLOAT NOT NULL, 
GSM153440 FLOAT NOT NULL, 
GSM153447 FLOAT NOT NULL, 
GSM153450 FLOAT NOT NULL, 
GSM153456 FLOAT NOT NULL, 
GSM153457 FLOAT NOT NULL, 
GSM153458 FLOAT NOT NULL, 
GSM153459 FLOAT NOT NULL, 
GSM153460 FLOAT NOT NULL, 
GSM153461 FLOAT NOT NULL, 
GSM153463 FLOAT NOT NULL, 
GSM153464 FLOAT NOT NULL, 
GSM153466 FLOAT NOT NULL, 
GSM153467 FLOAT NOT NULL, 
GSM153468 FLOAT NOT NULL, 
GSM153469 FLOAT NOT NULL, 
GSM153470 FLOAT NOT NULL, 
GSM153471 FLOAT NOT NULL, 
GSM153472 FLOAT NOT NULL, 
GSM153473 FLOAT NOT NULL, 
GSM153474 FLOAT NOT NULL, 
GSM153475 FLOAT NOT NULL, 
GSM153476 FLOAT NOT NULL, 
GSM153478 FLOAT NOT NULL, 
GSM153480 FLOAT NOT NULL, 
GSM153486 FLOAT NOT NULL, 
GSM153487 FLOAT NOT NULL, 
GSM153499 FLOAT NOT NULL, 
GSM153504 FLOAT NOT NULL, 
GSM153507 FLOAT NOT NULL, 
GSM153404 FLOAT NOT NULL, 
GSM153407 FLOAT NOT NULL, 
GSM153408 FLOAT NOT NULL, 
GSM153410 FLOAT NOT NULL, 
GSM153411 FLOAT NOT NULL, 
GSM153412 FLOAT NOT NULL, 
GSM153413 FLOAT NOT NULL, 
GSM153414 FLOAT NOT NULL, 
GSM153415 FLOAT NOT NULL, 
GSM153416 FLOAT NOT NULL, 
GSM153417 FLOAT NOT NULL, 
GSM153418 FLOAT NOT NULL, 
GSM153420 FLOAT NOT NULL, 
GSM153421 FLOAT NOT NULL, 
GSM153422 FLOAT NOT NULL, 
GSM153424 FLOAT NOT NULL, 
GSM153430 FLOAT NOT NULL, 
GSM153432 FLOAT NOT NULL, 
GSM153434 FLOAT NOT NULL, 
GSM153435 FLOAT NOT NULL, 
GSM153436 FLOAT NOT NULL, 
GSM153437 FLOAT NOT NULL, 
GSM153439 FLOAT NOT NULL, 
GSM153441 FLOAT NOT NULL, 
GSM153442 FLOAT NOT NULL, 
GSM153443 FLOAT NOT NULL, 
GSM153445 FLOAT NOT NULL, 
GSM153446 FLOAT NOT NULL, 
GSM153449 FLOAT NOT NULL, 
GSM153453 FLOAT NOT NULL, 
GSM153454 FLOAT NOT NULL, 
GSM153455 FLOAT NOT NULL, 
GSM153462 FLOAT NOT NULL, 
GSM153465 FLOAT NOT NULL, 
GSM153481 FLOAT NOT NULL, 
GSM153482 FLOAT NOT NULL, 
GSM153483 FLOAT NOT NULL, 
GSM153485 FLOAT NOT NULL, 
GSM153489 FLOAT NOT NULL, 
GSM153490 FLOAT NOT NULL, 
GSM153491 FLOAT NOT NULL, 
GSM153492 FLOAT NOT NULL, 
GSM153493 FLOAT NOT NULL, 
GSM153494 FLOAT NOT NULL, 
GSM153495 FLOAT NOT NULL, 
GSM153498 FLOAT NOT NULL, 
GSM153501 FLOAT NOT NULL, 
GSM153502 FLOAT NOT NULL, 
GSM153505 FLOAT NOT NULL, 
GSM153506 FLOAT NOT NULL,
PRIMARY KEY (id)
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
