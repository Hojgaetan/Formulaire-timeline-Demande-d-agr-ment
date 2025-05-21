#!/usr/bin/env python3
"""
Test script for the backend API
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_submit_form():
    """Test submitting a complete form"""
    print("Testing form submission...")
    
    # Sample data for testing
    data = {
        "renouvellement": True,
        "manuel_procedures": True,
        "attestation_non_interdiction": True,
        "annee_creation": "2020",
        "domaine": "Conseil",
        "ca_n1": "1000000",
        "sous_traite_n1": "20%",
        "masse_salariale_n1": "500000",
        "ca_n2": "1200000",
        "sous_traite_n2": "25%",
        "masse_salariale_n2": "600000",
        "dirigeants": [
            {"prenom": "John", "nom": "Doe"},
            {"prenom": "Jane", "nom": "Smith"}
        ],
        "logistiques": [
            {"libelle": "Ordinateurs portables"},
            {"libelle": "Imprimantes"}
        ],
        "personnel": [
            {
                "nom": "Johnson",
                "prenom": "Robert",
                "grade": "Senior",
                "fonction": "Développeur",
                "domaine_competence": "Informatique",
                "annees_experience": "10"
            }
        ],
        "supervision": [
            {
                "nom": "Williams",
                "prenom": "Mary",
                "grade": "Manager",
                "fonction": "Chef de projet",
                "domaine_competence": "Gestion de projet",
                "annees_experience": "15"
            }
        ],
        "expertises": {
            "AA": True,
            "AB": False,
            "B": True,
            "D": True
        },
        "references": [
            {
                "domaine": "Conseil",
                "entreprise_bailleur": "Acme Inc",
                "annee": "2019",
                "pays": "Sénégal",
                "description": "Conseil en stratégie",
                "prenom_source": "Alice",
                "nom_source": "Brown",
                "telephone_source": "+221 77 123 45 67"
            }
        ],
        "autres_missions": [
            {"libelle": "Formation en management"}
        ],
        "autres_experiences": [
            {"libelle": "Conseil en transformation digitale"}
        ],
        "honoraires": {
            "type_consultant": "Consultant sénior",
            "taux_journalier": "300.000 - 400.000",
            "signature_certification": True
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/submit", json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            print(f"Form submitted successfully! Cabinet ID: {result.get('cabinet_id')}")
            return result.get('cabinet_id')
        else:
            print(f"Error: {result.get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_get_cabinet(cabinet_id):
    """Test retrieving cabinet data"""
    print(f"\nTesting get cabinet data for ID {cabinet_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/cabinet/{cabinet_id}")
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            print("Cabinet data retrieved successfully!")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {result.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def test_add_dirigeant(cabinet_id):
    """Test adding a dirigeant"""
    print(f"\nTesting add dirigeant for cabinet ID {cabinet_id}...")
    
    data = {
        "prenom": "Michael",
        "nom": "Jordan"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/cabinet/{cabinet_id}/dirigeant", json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            print(f"Dirigeant added successfully! ID: {result.get('dirigeant_id')}")
        else:
            print(f"Error: {result.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def test_add_logistique(cabinet_id):
    """Test adding a logistique"""
    print(f"\nTesting add logistique for cabinet ID {cabinet_id}...")
    
    data = {
        "libelle": "Serveurs cloud"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/cabinet/{cabinet_id}/logistique", json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get('success'):
            print(f"Logistique added successfully! ID: {result.get('logistique_id')}")
        else:
            print(f"Error: {result.get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    """Main function to run tests"""
    print("Starting API tests...\n")
    
    # Test form submission
    cabinet_id = test_submit_form()
    
    if cabinet_id:
        # Test getting cabinet data
        test_get_cabinet(cabinet_id)
        
        # Test adding a dirigeant
        test_add_dirigeant(cabinet_id)
        
        # Test adding a logistique
        test_add_logistique(cabinet_id)
        
        # Test getting updated cabinet data
        test_get_cabinet(cabinet_id)
    
    print("\nTests completed.")

if __name__ == "__main__":
    main()