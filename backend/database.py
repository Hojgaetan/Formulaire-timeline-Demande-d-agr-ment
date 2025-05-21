import sqlite3
import os
from sqlite3 import Error

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'demande_agrement.db')

def get_db_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    
    return conn

def init_db():
    """Initialize the database with schema"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            # Read schema file
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql'), 'r') as f:
                schema = f.read()
            
            # Execute schema
            conn.executescript(schema)
            conn.commit()
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")

# Cabinet operations
def create_cabinet(cabinet_data):
    """Create a new cabinet entry"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO cabinet(
                renouvellement, manuel_procedures, attestation_non_interdiction,
                annee_creation, domaine, ca_n1, sous_traite_n1, masse_salariale_n1,
                ca_n2, sous_traite_n2, masse_salariale_n2
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (
                cabinet_data['renouvellement'],
                cabinet_data['manuel_procedures'],
                cabinet_data['attestation_non_interdiction'],
                cabinet_data['annee_creation'],
                cabinet_data['domaine'],
                cabinet_data.get('ca_n1'),
                cabinet_data.get('sous_traite_n1'),
                cabinet_data.get('masse_salariale_n1'),
                cabinet_data.get('ca_n2'),
                cabinet_data.get('sous_traite_n2'),
                cabinet_data.get('masse_salariale_n2')
            ))
            conn.commit()
            cabinet_id = cur.lastrowid
            return cabinet_id
        except Error as e:
            print(f"Error creating cabinet: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

def get_cabinet(cabinet_id):
    """Get a cabinet by ID"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM cabinet WHERE id = ?", (cabinet_id,))
            cabinet = cur.fetchone()
            return dict(cabinet) if cabinet else None
        except Error as e:
            print(f"Error getting cabinet: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

# Dirigeants operations
def add_dirigeant(cabinet_id, prenom, nom):
    """Add a dirigeant to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO dirigeants(cabinet_id, prenom, nom)
            VALUES(?, ?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (cabinet_id, prenom, nom))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding dirigeant: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

def get_dirigeants(cabinet_id):
    """Get all dirigeants for a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM dirigeants WHERE cabinet_id = ?", (cabinet_id,))
            dirigeants = cur.fetchall()
            return [dict(dirigeant) for dirigeant in dirigeants]
        except Error as e:
            print(f"Error getting dirigeants: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return []

# Logistiques operations
def add_logistique(cabinet_id, libelle):
    """Add a logistique to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO logistiques(cabinet_id, libelle)
            VALUES(?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (cabinet_id, libelle))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding logistique: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

def get_logistiques(cabinet_id):
    """Get all logistiques for a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM logistiques WHERE cabinet_id = ?", (cabinet_id,))
            logistiques = cur.fetchall()
            return [dict(logistique) for logistique in logistiques]
        except Error as e:
            print(f"Error getting logistiques: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return []

# Personnel operations
def add_personnel(cabinet_id, personnel_data):
    """Add a personnel to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO personnel(
                cabinet_id, nom, prenom, grade, fonction, 
                domaine_competence, annees_experience
            ) VALUES(?, ?, ?, ?, ?, ?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (
                cabinet_id,
                personnel_data['nom'],
                personnel_data['prenom'],
                personnel_data['grade'],
                personnel_data['fonction'],
                personnel_data['domaine_competence'],
                personnel_data['annees_experience']
            ))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding personnel: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

def get_personnel(cabinet_id):
    """Get all personnel for a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM personnel WHERE cabinet_id = ?", (cabinet_id,))
            personnel_list = cur.fetchall()
            return [dict(personnel) for personnel in personnel_list]
        except Error as e:
            print(f"Error getting personnel: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return []

# Similar functions for supervision, expertises, references, autres_missions, autres_experiences, and honoraires
# would follow the same pattern

# Supervision operations
def add_supervision(cabinet_id, supervision_data):
    """Add a supervision to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO supervision(
                cabinet_id, nom, prenom, grade, fonction, 
                domaine_competence, annees_experience
            ) VALUES(?, ?, ?, ?, ?, ?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (
                cabinet_id,
                supervision_data['nom'],
                supervision_data['prenom'],
                supervision_data['grade'],
                supervision_data['fonction'],
                supervision_data['domaine_competence'],
                supervision_data['annees_experience']
            ))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding supervision: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

# Expertises operations
def update_expertise(cabinet_id, code, selected):
    """Update an expertise selection for a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            # Check if the expertise already exists for this cabinet
            cur = conn.cursor()
            cur.execute("SELECT * FROM expertises WHERE cabinet_id = ? AND code = ?", (cabinet_id, code))
            expertise = cur.fetchone()
            
            if expertise:
                # Update existing record
                cur.execute("UPDATE expertises SET selected = ? WHERE id = ?", (selected, expertise['id']))
            else:
                # Get the libelle from the default expertises
                cur.execute("SELECT libelle FROM expertises WHERE cabinet_id = 0 AND code = ?", (code,))
                default_expertise = cur.fetchone()
                if default_expertise:
                    # Insert new record
                    cur.execute(
                        "INSERT INTO expertises(cabinet_id, code, libelle, selected) VALUES(?, ?, ?, ?)",
                        (cabinet_id, code, default_expertise['libelle'], selected)
                    )
            
            conn.commit()
            return True
        except Error as e:
            print(f"Error updating expertise: {e}")
            return False
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return False

def get_expertises(cabinet_id):
    """Get all expertises for a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            cur = conn.cursor()
            # Get default expertises if no cabinet-specific ones exist
            cur.execute("""
                SELECT e.code, e.libelle, COALESCE(ce.selected, 0) as selected
                FROM expertises e
                LEFT JOIN (SELECT * FROM expertises WHERE cabinet_id = ?) ce
                ON e.code = ce.code
                WHERE e.cabinet_id = 0
            """, (cabinet_id,))
            expertises = cur.fetchall()
            return [dict(expertise) for expertise in expertises]
        except Error as e:
            print(f"Error getting expertises: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return []

# References operations
def add_reference(cabinet_id, reference_data):
    """Add a reference to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO references(
                cabinet_id, domaine, entreprise_bailleur, annee, pays,
                description, prenom_source, nom_source, telephone_source
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (
                cabinet_id,
                reference_data['domaine'],
                reference_data['entreprise_bailleur'],
                reference_data['annee'],
                reference_data['pays'],
                reference_data['description'],
                reference_data['prenom_source'],
                reference_data['nom_source'],
                reference_data['telephone_source']
            ))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding reference: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

# Autres Missions operations
def add_autre_mission(cabinet_id, libelle):
    """Add an autre mission to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO autres_missions(cabinet_id, libelle)
            VALUES(?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (cabinet_id, libelle))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding autre mission: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

# Autres Experiences operations
def add_autre_experience(cabinet_id, libelle):
    """Add an autre experience to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO autres_experiences(cabinet_id, libelle)
            VALUES(?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (cabinet_id, libelle))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding autre experience: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

# Honoraires operations
def add_honoraires(cabinet_id, honoraires_data):
    """Add honoraires to a cabinet"""
    conn = get_db_connection()
    
    if conn is not None:
        try:
            sql = '''
            INSERT INTO honoraires(
                cabinet_id, type_consultant, taux_journalier, signature_certification
            ) VALUES(?, ?, ?, ?)
            '''
            cur = conn.cursor()
            cur.execute(sql, (
                cabinet_id,
                honoraires_data['type_consultant'],
                honoraires_data['taux_journalier'],
                honoraires_data['signature_certification']
            ))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Error adding honoraires: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")
        return None

# Initialize the database if this file is run directly
if __name__ == "__main__":
    init_db()