-- Schema for the Demande d'Agrément database

-- Cabinet table to store company information
CREATE TABLE IF NOT EXISTS cabinet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    renouvellement BOOLEAN NOT NULL,
    manuel_procedures BOOLEAN NOT NULL,
    attestation_non_interdiction BOOLEAN NOT NULL,
    annee_creation INTEGER NOT NULL,
    domaine TEXT NOT NULL,
    ca_n1 REAL,
    sous_traite_n1 REAL,
    masse_salariale_n1 REAL,
    ca_n2 REAL,
    sous_traite_n2 REAL,
    masse_salariale_n2 REAL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dirigeants table to store company leaders
CREATE TABLE IF NOT EXISTS dirigeants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    prenom TEXT NOT NULL,
    nom TEXT NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- Logistiques table to store equipment
CREATE TABLE IF NOT EXISTS logistiques (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    libelle TEXT NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- Personnel table to store professional staff
CREATE TABLE IF NOT EXISTS personnel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    grade TEXT NOT NULL,
    fonction TEXT NOT NULL,
    domaine_competence TEXT NOT NULL,
    annees_experience INTEGER NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- Supervision table to store supervision staff
CREATE TABLE IF NOT EXISTS supervision (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    grade TEXT NOT NULL,
    fonction TEXT NOT NULL,
    domaine_competence TEXT NOT NULL,
    annees_experience INTEGER NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- Expertises table to store areas of expertise
CREATE TABLE IF NOT EXISTS expertises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    libelle TEXT NOT NULL,
    selected BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- References table to store references
CREATE TABLE IF NOT EXISTS references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    domaine TEXT NOT NULL,
    entreprise_bailleur TEXT NOT NULL,
    annee INTEGER NOT NULL,
    pays TEXT NOT NULL,
    description TEXT NOT NULL,
    prenom_source TEXT NOT NULL,
    nom_source TEXT NOT NULL,
    telephone_source TEXT NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- AutresMissions table to store other missions
CREATE TABLE IF NOT EXISTS autres_missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    libelle TEXT NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- AutresExperiences table to store other experiences
CREATE TABLE IF NOT EXISTS autres_experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    libelle TEXT NOT NULL,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- Honoraires table to store fees
CREATE TABLE IF NOT EXISTS honoraires (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cabinet_id INTEGER NOT NULL,
    type_consultant TEXT NOT NULL,
    taux_journalier TEXT NOT NULL,
    signature_certification BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (cabinet_id) REFERENCES cabinet(id) ON DELETE CASCADE
);

-- Insert default expertise categories
INSERT INTO expertises (cabinet_id, code, libelle, selected) VALUES
(0, 'AA', 'Politique Générale et Développement Organisationnel', 0),
(0, 'AB', 'Système d''information et informatique', 0),
(0, 'AC', 'Gestion de la qualité', 0),
(0, 'AD', 'Information et veille', 0),
(0, 'AE', 'Maintenance', 0),
(0, 'AF', 'Gestion Financière, Gestion comptable et Administrative', 0),
(0, 'AG', 'Gestion des opérations et de la production, Ingénierie de la production', 0),
(0, 'AH', 'Marketing distribution et communication', 0),
(0, 'AI', 'Ressources humaines', 0),
(0, 'B', 'Assistance juridique et fiscale', 0),
(0, 'CA', 'Formation en gestion', 0),
(0, 'CB', 'Formation en informatique', 0),
(0, 'CC', 'Formation technique et industrielle', 0),
(0, 'D', 'Etudes Economiques', 0),
(0, 'EA', 'Plans d''affaires et recherche de partenaires financiers', 0),
(0, 'EB', 'Intermédiaire Financière', 0),
(0, 'EC', 'Suivi post financement', 0);