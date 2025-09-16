# Projet ADI✈️ - Plateforme d'Analyse de Données Industrielles

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.2-orange)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
Une plateforme web complète pour l'analyse et la visualisation des données industrielles, développée avec Flask.

## Présentation
Le Tableau de Bord Qualité ADI est une plateforme web conçue pour gérer et visualiser les métriques de qualité des ateliers de fabrication chez ADI. Elle offre des insights en temps réel sur les indicateurs clés de performance (KPI) tels que le PPM (Parts Per Million), les taux de rebut, les taux de retouche, les coûts de rebut et les réclamations clients. La plateforme prend en charge deux rôles principaux : Chargé Qualité/Animateur Qualité (saisie et consultation des données) , Admin et Utilisateurs en Visualisation (analyse des données via des graphiques et tableaux interactifs). 
Construite avec une interface moderne et responsive, elle utilise Bootstrap, Chart.js et AOS pour une expérience utilisateur fluide.
## 🚀 Fonctionnalités

- **📊 Tableaux de bord interactifs** - Visualisation en temps réel des métriques qualité avec des graphiques dynamiques (histogrammes, courbes, aires) pour plusieurs ateliers et années.
- **Saisie des Données**: Permet aux utilisateurs autorisés d'enregistrer les données qualité mensuelles pour un atelier spécifique.
- **📈 Analyse de données** - Traitement et analyse des données industrielles avec Pandas et NumPy
- **Consultation des Données** - Offre des vues détaillées des métriques qualité historiques et actuelles.
- **Analyse de Conformité** - Affiche l'état de conformité mensuel avec seuils et taux de conformité.
- **Métriques YTD (Year to Date)** -  Résume les KPI cumulés pour l'année ou l'atelier sélectionné.
- **Design Responsive** - Optimisé pour ordinateurs, tablettes et mobiles.
- **Gestion des Utilisateurs** - Prend en charge l'accès basé sur les rôles avec profils utilisateur et gestion de sessions.
- **Mises à Jour en Temps Réel** - Actualisation automatique des données toutes les 5 minutes pour des informations à jour.
- **Animations et Visuels** - Utilise AOS pour des animations fluides et un style basé sur des dégradés pour un look moderne.
-  **Gestion des Erreurs** - Gestion robuste des erreurs API avec des états de chargement et d'erreur conviviaux.
- **📋 Gestion des seuils** - Configuration dynamique des seuils d'alerte par atelier et indicateur
- **📤 Import/Export** - Support multiple formats (Excel, PPTX, CSV)
- **👨‍�Interface d'administration** - Gestion complète des utilisateurs et paramètres

## 🛠️ Technologies Utilisées

### Backend
- **Flask 3.1.2** - Framework web Python
- **Pandas 2.3.2** - Manipulation et analyse de données
- **NumPy 2.3.3** - Calcul scientifique
- **Python-pptx 1.0.2** - Génération de présentations PowerPoint
- **XlsxWriter 3.2.9** - Création de fichiers Excel
- * API RESTful pour la récupération des données (/api/charts_data, /api/ytd_data, /api/user/current)

### Frontend
- **HTML5/CSS3** - Structure et style
- **JavaScript** - Interactivité
- **Bootstrap** - Framework CSS responsive
- **Chart.js** - Visualisations graphiques
- **Jinja2 3.1.6** - Templating HTML

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)
- Virtualenv (recommandé)

### Installation pas à pas

1. **Cloner le dépôt**
   git clone https://github.com/imensalhi/Projet_ADI.git
   cd Projet_ADI
2. **Créer un environnement virtuel**
    python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
3.**Installer les dépendances**
pip install -r requirement.txt

## 🚀 Utilisation

1.**Accès à l'application**
Lancez le serveur : flask run

Ouvrez votre navigateur : http://localhost:5000

Connectez-vous avec vos identifiants

2.**Fonctionnalités principales**
Tableau de bord : Visualisation des indicateurs clés

Gestion des données : Import/export des données industrielles

Configuration des seuils : Définition des limites d'alerte

Consultation des données 

Administration : Gestion des utilisateurs et paramètres système

3.**🧪 Tests**

# Exécuter les tests unitaires
python -m pytest tests/

# Exécuter avec couverture de code
python -m pytest --cov=app tests/
