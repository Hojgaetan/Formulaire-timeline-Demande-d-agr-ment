from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import database
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Initialize database
@app.before_first_request
def initialize_database():
    database.init_db()

# Home route - redirect to the form
@app.route('/')
def index():
    return redirect(url_for('form'))

# Form route - serve the HTML form
@app.route('/form')
def form():
    return render_template('formulaire.html')

# API endpoint to submit the entire form
@app.route('/api/submit', methods=['POST'])
def submit_form():
    try:
        data = request.json
        
        # Create cabinet entry
        cabinet_data = {
            'renouvellement': data.get('renouvellement', False),
            'manuel_procedures': data.get('manuel_procedures', False),
            'attestation_non_interdiction': data.get('attestation_non_interdiction', False),
            'annee_creation': data.get('annee_creation'),
            'domaine': data.get('domaine'),
            'ca_n1': data.get('ca_n1'),
            'sous_traite_n1': data.get('sous_traite_n1'),
            'masse_salariale_n1': data.get('masse_salariale_n1'),
            'ca_n2': data.get('ca_n2'),
            'sous_traite_n2': data.get('sous_traite_n2'),
            'masse_salariale_n2': data.get('masse_salariale_n2')
        }
        
        cabinet_id = database.create_cabinet(cabinet_data)
        
        if not cabinet_id:
            return jsonify({'success': False, 'message': 'Failed to create cabinet entry'}), 500
        
        # Add dirigeants
        dirigeants = data.get('dirigeants', [])
        for dirigeant in dirigeants:
            database.add_dirigeant(cabinet_id, dirigeant.get('prenom'), dirigeant.get('nom'))
        
        # Add logistiques
        logistiques = data.get('logistiques', [])
        for logistique in logistiques:
            database.add_logistique(cabinet_id, logistique.get('libelle'))
        
        # Add personnel
        personnel_list = data.get('personnel', [])
        for personnel in personnel_list:
            database.add_personnel(cabinet_id, personnel)
        
        # Add supervision
        supervision_list = data.get('supervision', [])
        for supervision in supervision_list:
            database.add_supervision(cabinet_id, supervision)
        
        # Update expertises
        expertises = data.get('expertises', {})
        for code, selected in expertises.items():
            database.update_expertise(cabinet_id, code, selected)
        
        # Add references
        references = data.get('references', [])
        for reference in references:
            database.add_reference(cabinet_id, reference)
        
        # Add autres missions
        autres_missions = data.get('autres_missions', [])
        for mission in autres_missions:
            database.add_autre_mission(cabinet_id, mission.get('libelle'))
        
        # Add autres experiences
        autres_experiences = data.get('autres_experiences', [])
        for experience in autres_experiences:
            database.add_autre_experience(cabinet_id, experience.get('libelle'))
        
        # Add honoraires
        honoraires = data.get('honoraires', {})
        if honoraires:
            database.add_honoraires(cabinet_id, honoraires)
        
        return jsonify({'success': True, 'cabinet_id': cabinet_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to get cabinet data
@app.route('/api/cabinet/<int:cabinet_id>', methods=['GET'])
def get_cabinet_data(cabinet_id):
    try:
        cabinet = database.get_cabinet(cabinet_id)
        
        if not cabinet:
            return jsonify({'success': False, 'message': 'Cabinet not found'}), 404
        
        # Get related data
        dirigeants = database.get_dirigeants(cabinet_id)
        logistiques = database.get_logistiques(cabinet_id)
        personnel = database.get_personnel(cabinet_id)
        expertises = database.get_expertises(cabinet_id)
        
        # Construct response
        response = {
            'success': True,
            'cabinet': cabinet,
            'dirigeants': dirigeants,
            'logistiques': logistiques,
            'personnel': personnel,
            'expertises': expertises
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add a dirigeant
@app.route('/api/cabinet/<int:cabinet_id>/dirigeant', methods=['POST'])
def add_dirigeant(cabinet_id):
    try:
        data = request.json
        prenom = data.get('prenom')
        nom = data.get('nom')
        
        if not prenom or not nom:
            return jsonify({'success': False, 'message': 'Prenom and nom are required'}), 400
        
        dirigeant_id = database.add_dirigeant(cabinet_id, prenom, nom)
        
        if not dirigeant_id:
            return jsonify({'success': False, 'message': 'Failed to add dirigeant'}), 500
        
        return jsonify({'success': True, 'dirigeant_id': dirigeant_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add a logistique
@app.route('/api/cabinet/<int:cabinet_id>/logistique', methods=['POST'])
def add_logistique(cabinet_id):
    try:
        data = request.json
        libelle = data.get('libelle')
        
        if not libelle:
            return jsonify({'success': False, 'message': 'Libelle is required'}), 400
        
        logistique_id = database.add_logistique(cabinet_id, libelle)
        
        if not logistique_id:
            return jsonify({'success': False, 'message': 'Failed to add logistique'}), 500
        
        return jsonify({'success': True, 'logistique_id': logistique_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add personnel
@app.route('/api/cabinet/<int:cabinet_id>/personnel', methods=['POST'])
def add_personnel(cabinet_id):
    try:
        data = request.json
        
        required_fields = ['nom', 'prenom', 'grade', 'fonction', 'domaine_competence', 'annees_experience']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        personnel_id = database.add_personnel(cabinet_id, data)
        
        if not personnel_id:
            return jsonify({'success': False, 'message': 'Failed to add personnel'}), 500
        
        return jsonify({'success': True, 'personnel_id': personnel_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add supervision
@app.route('/api/cabinet/<int:cabinet_id>/supervision', methods=['POST'])
def add_supervision(cabinet_id):
    try:
        data = request.json
        
        required_fields = ['nom', 'prenom', 'grade', 'fonction', 'domaine_competence', 'annees_experience']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        supervision_id = database.add_supervision(cabinet_id, data)
        
        if not supervision_id:
            return jsonify({'success': False, 'message': 'Failed to add supervision'}), 500
        
        return jsonify({'success': True, 'supervision_id': supervision_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to update expertise
@app.route('/api/cabinet/<int:cabinet_id>/expertise', methods=['POST'])
def update_expertise(cabinet_id):
    try:
        data = request.json
        code = data.get('code')
        selected = data.get('selected', False)
        
        if not code:
            return jsonify({'success': False, 'message': 'Code is required'}), 400
        
        success = database.update_expertise(cabinet_id, code, selected)
        
        if not success:
            return jsonify({'success': False, 'message': 'Failed to update expertise'}), 500
        
        return jsonify({'success': True}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add reference
@app.route('/api/cabinet/<int:cabinet_id>/reference', methods=['POST'])
def add_reference(cabinet_id):
    try:
        data = request.json
        
        required_fields = ['domaine', 'entreprise_bailleur', 'annee', 'pays', 
                          'description', 'prenom_source', 'nom_source', 'telephone_source']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        reference_id = database.add_reference(cabinet_id, data)
        
        if not reference_id:
            return jsonify({'success': False, 'message': 'Failed to add reference'}), 500
        
        return jsonify({'success': True, 'reference_id': reference_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add autre mission
@app.route('/api/cabinet/<int:cabinet_id>/autre-mission', methods=['POST'])
def add_autre_mission(cabinet_id):
    try:
        data = request.json
        libelle = data.get('libelle')
        
        if not libelle:
            return jsonify({'success': False, 'message': 'Libelle is required'}), 400
        
        mission_id = database.add_autre_mission(cabinet_id, libelle)
        
        if not mission_id:
            return jsonify({'success': False, 'message': 'Failed to add autre mission'}), 500
        
        return jsonify({'success': True, 'mission_id': mission_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add autre experience
@app.route('/api/cabinet/<int:cabinet_id>/autre-experience', methods=['POST'])
def add_autre_experience(cabinet_id):
    try:
        data = request.json
        libelle = data.get('libelle')
        
        if not libelle:
            return jsonify({'success': False, 'message': 'Libelle is required'}), 400
        
        experience_id = database.add_autre_experience(cabinet_id, libelle)
        
        if not experience_id:
            return jsonify({'success': False, 'message': 'Failed to add autre experience'}), 500
        
        return jsonify({'success': True, 'experience_id': experience_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to add honoraires
@app.route('/api/cabinet/<int:cabinet_id>/honoraires', methods=['POST'])
def add_honoraires(cabinet_id):
    try:
        data = request.json
        
        required_fields = ['type_consultant', 'taux_journalier', 'signature_certification']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        honoraires_id = database.add_honoraires(cabinet_id, data)
        
        if not honoraires_id:
            return jsonify({'success': False, 'message': 'Failed to add honoraires'}), 500
        
        return jsonify({'success': True, 'honoraires_id': honoraires_id}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)