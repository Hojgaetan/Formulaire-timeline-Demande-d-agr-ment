# Backend pour Formulaire de Demande d'Agrément

Ce backend implémente une API REST avec Python et SQLite3 pour gérer les demandes d'agrément.

## Structure du Projet

```
backend/
├── app.py                # Application Flask principale
├── database.py           # Opérations de base de données
├── schema.sql            # Schéma de la base de données
├── requirements.txt      # Dépendances Python
├── templates/            # Templates HTML
│   └── formulaire.html   # Formulaire de demande d'agrément
└── static/               # Fichiers statiques (CSS, JS, images)
```

## Installation

1. Cloner le dépôt :
```bash
git clone <url-du-repo>
cd Formulaire-timeline-Demande-d-agr-ment
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances :
```bash
pip install -r backend/requirements.txt
```

4. Exécuter le script de configuration pour initialiser la base de données et copier les fichiers statiques :
```bash
cd backend
python setup.py
```

## Exécution

Pour lancer l'application :

```bash
cd backend
python app.py
```

L'application sera accessible à l'adresse http://localhost:5000

## Tests

Pour tester l'API, vous pouvez utiliser le script de test fourni :

```bash
# Assurez-vous que l'application est en cours d'exécution dans un autre terminal
python test_api.py
```

Ce script teste les fonctionnalités principales de l'API :
- Soumission d'un formulaire complet
- Récupération des données d'un cabinet
- Ajout d'un dirigeant
- Ajout d'une logistique

## API Endpoints

### Soumission du formulaire complet
- **URL** : `/api/submit`
- **Méthode** : `POST`
- **Description** : Soumet toutes les données du formulaire en une seule requête

### Récupération des données d'un cabinet
- **URL** : `/api/cabinet/<cabinet_id>`
- **Méthode** : `GET`
- **Description** : Récupère toutes les données associées à un cabinet

### Ajout d'un dirigeant
- **URL** : `/api/cabinet/<cabinet_id>/dirigeant`
- **Méthode** : `POST`
- **Description** : Ajoute un dirigeant à un cabinet

### Ajout d'une logistique
- **URL** : `/api/cabinet/<cabinet_id>/logistique`
- **Méthode** : `POST`
- **Description** : Ajoute une logistique à un cabinet

### Ajout d'un personnel
- **URL** : `/api/cabinet/<cabinet_id>/personnel`
- **Méthode** : `POST`
- **Description** : Ajoute un personnel à un cabinet

### Ajout d'une supervision
- **URL** : `/api/cabinet/<cabinet_id>/supervision`
- **Méthode** : `POST`
- **Description** : Ajoute une supervision à un cabinet

### Mise à jour d'une expertise
- **URL** : `/api/cabinet/<cabinet_id>/expertise`
- **Méthode** : `POST`
- **Description** : Met à jour une expertise pour un cabinet

### Ajout d'une référence
- **URL** : `/api/cabinet/<cabinet_id>/reference`
- **Méthode** : `POST`
- **Description** : Ajoute une référence à un cabinet

### Ajout d'une autre mission
- **URL** : `/api/cabinet/<cabinet_id>/autre-mission`
- **Méthode** : `POST`
- **Description** : Ajoute une autre mission à un cabinet

### Ajout d'une autre expérience
- **URL** : `/api/cabinet/<cabinet_id>/autre-experience`
- **Méthode** : `POST`
- **Description** : Ajoute une autre expérience à un cabinet

### Ajout d'honoraires
- **URL** : `/api/cabinet/<cabinet_id>/honoraires`
- **Méthode** : `POST`
- **Description** : Ajoute des honoraires à un cabinet

## Structure de la Base de Données

La base de données SQLite3 contient les tables suivantes :

- **cabinet** : Informations principales sur le cabinet
- **dirigeants** : Dirigeants du cabinet
- **logistiques** : Équipements et logistiques du cabinet
- **personnel** : Personnel professionnel permanent
- **supervision** : Personnel de supervision et coordination
- **expertises** : Domaines d'expertise du cabinet
- **references** : Références du cabinet
- **autres_missions** : Autres missions réalisées
- **autres_experiences** : Autres expériences
- **honoraires** : Informations sur les honoraires

## Développement

Pour contribuer au développement :

1. Créer une branche pour votre fonctionnalité
2. Développer et tester votre fonctionnalité
3. Soumettre une pull request

## Licence

Ce projet est sous licence [MIT](LICENSE).
