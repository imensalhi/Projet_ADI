# 🛩️ Qboard ADI - Plateforme de Management de la Performance Qualité

<div align="center">

*Plateforme web complète de monitoring et contrôle qualité en temps réel pour l'industrie aérospatiale*

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.2-orange?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensource&logoColor=white)](LICENSE)

 | [📖 Documentation](#-utilisation) | [🐛 Issues](https://github.com/imensalhi/Projet_ADI/issues)

</div>

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture & Rôles](#-architecture--rôles)
- [Technologies](#-technologies-utilisées)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [API Reference](#-api-reference)
- [Déploiement](#-déploiement)

---

## 🎯 Présentation

**Qboard ADI** est une plateforme web moderne développée avec Flask pour le monitoring et le contrôle qualité des ateliers de fabrication aérospatiale chez ADI. Elle offre une vision en temps réel des indicateurs clés de performance (KPI) avec une interface intuitive et responsive.

### Indicateurs Qualité Surveillés

- **📊 PPM** (Parts Per Million) - Défauts par million de pièces
- **♻️ Taux de Rebut** - Pourcentage de pièces rejetées
- **🔧 Taux de Retouche** - Pièces nécessitant une correction
- **💰 Coûts de Rebut** - Impact financier des défauts
- **📞 Réclamations Clients** - Retours et plaintes qualité
- **📈 CNQ** (Coût de Non-Qualité) - Analyse des coûts totaux

---

## 🚀 Fonctionnalités

### 📊 **Tableaux de Bord Interactifs**
- Visualisation en temps réel avec graphiques dynamiques (histogrammes, courbes, aires)
- Métriques YTD (Year to Date) avec comparaisons annuelles
- Actualisation automatique toutes les 5 minutes
- Filtrage par atelier, année et mois

### 📈 **Analyse Avancée**
- Analyse de conformité avec seuils personnalisables
- Comparaisons multi-ateliers et multi-années
- Calculs statistiques automatisés (moyennes, tendances, écarts)
- Alertes visuelles pour dépassements de seuils

### 📤 **Import/Export Multi-formats**
- **Excel** (.xlsx) - Import/Export des données
- **PowerPoint** (.pptx) - Génération de rapports automatiques
- **CSV** - Échange de données simplifié
- **PDF** - Rapports formatés pour impression

### 🎨 **Interface Moderne**
- Design responsive (Desktop, Tablet, Mobile)
- Animations fluides avec AOS (Animate On Scroll)
- Thème moderne avec dégradés et effets visuels
- Interface multilingue (Français)

### 🔄 **Temps Réel**
- Mises à jour automatiques des données
- Synchronisation instantanée des modifications
- Notifications en temps réel
- States de chargement et gestion d'erreurs

### **Saisie des Données**
Permet aux utilisateurs autorisés d'enregistrer les données qualité mensuelles pour un atelier spécifique.

### **Consultation des Données** 
Offre des vues détaillées des métriques qualité historiques et actuelles.

### **Analyse de Conformité** 
Affiche l'état de conformité mensuel avec seuils et taux de conformité.

### **Métriques YTD (Year to Date)** 
Résume les KPI cumulés pour l'année ou l'atelier sélectionné.


### **Gestion des Utilisateurs** 
Prend en charge l'accès basé sur les rôles avec profils utilisateur et gestion de sessions.

### **Animations et Visuels** 
Utilise AOS pour des animations fluides et un style basé sur des dégradés pour un look moderne.

### **Gestion des Erreurs** 
Gestion robuste des erreurs API avec des états de chargement et d'erreur conviviaux.

### **📋 Gestion des seuils** 
Configuration dynamique des seuils d'alerte par atelier et indicateur

---

## 👥 Architecture & Rôles

### 🔑 **ADMIN** - Contrôle Total
**Permissions complètes :**
- ✅ **Gestion utilisateurs** : Ajouter, modifier, supprimer des utilisateurs
- ✅ **Configuration seuils** : Définir les limites d'alerte par atelier/indicateur
- ✅ **Saisie CNQ** : Entrer les valeurs de Coût de Non-Qualité
- ✅ **Consultation totale** : Accès à tous les ateliers et toutes les années
- ✅ **Visualisation avancée** : Graphiques comparatifs et analyses YTD
- ✅ **Export/Import** : Gestion complète des données

### 👨‍🔧 **CHARGÉ/ANIMATEUR QUALITÉ** - Opérationnel
**Permissions ciblées :**
- ✅ **Saisie données** : Formulaire d'entrée des métriques qualité mensuelles
- ✅ **Consultation** : Vue détaillée des données historiques de son périmètre
- ✅ **Graphiques** : Visualisation des indicateurs de son atelier
- ✅ **YTD personnel** : Métriques cumulées de son périmètre
- ❌ Gestion utilisateurs (lecture seule)

### 👀 **AUTRE/CONSULTATION** - Vue Lecture
**Permissions limitées :**
- ✅ **Consultation seule** : Visualisation des données publiques
- ✅ **Graphiques basiques** : Vue des tendances générales
- ❌ Saisie de données
- ❌ Gestion utilisateurs
- ❌ Configuration système

---

## 🛠️ Technologies Utilisées

### 🐍 **Backend**
```python
Flask 3.1.2          # Framework web Python
Gunicorn 21.2.0      # Serveur WSGI production
Pandas 2.3.2         # Manipulation de données
NumPy 2.3.3          # Calcul scientifique
Python-pptx 1.0.2    # Génération PowerPoint
XlsxWriter 3.2.9     # Création Excel
Pillow 11.3.0        # Traitement d'images
```

### 🎨 **Frontend**
```javascript
HTML5/CSS3           # Structure et style modernes
JavaScript ES6       # Logique client interactive
Bootstrap 5          # Framework CSS responsive
Chart.js 4           # Visualisations graphiques
AOS                  # Animations on scroll
Jinja2 3.1.6         # Templates HTML dynamiques
```

### 🗄️ **Base de Données & API**
```json
SQLite   # Base de données relationnelle
RESTful API          # Architecture API standard
JSON                 # Format d'échange de données

# Endpoints principaux :
/api/charts_data     # Données graphiques
/api/ytd_data       # Métriques YTD
/api/user/current   # Informations utilisateur
```

---

## 📦 Installation

### 🔧 **Prérequis**
- ![Python](https://img.shields.io/badge/Python-3.12+-blue) **Python 3.12** ou supérieur
- ![pip](https://img.shields.io/badge/pip-latest-green) **pip** (gestionnaire de packages Python)
- ![Git](https://img.shields.io/badge/Git-latest-red) **Git** pour le clonage

### 🚀 **Installation Locale**

1. **📁 Cloner le repository**
   
   git clone https://github.com/imensalhi/Projet_ADI.git
   cd Projet_ADI
   

2. **🐍 Créer un environnement virtuel**
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate


3. **📦 Installer les dépendances**

   pip install --upgrade pip
   pip install -r requirements.txt
   

4. **⚙️ Configuration initiale**

   # Variables d'environnement
   cp .env.example .env
   # Éditer .env avec vos paramètres


5. **🏃‍♂️ Lancer l'application**
   
   # Mode développement
   flask run
   
   # Mode production
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   

### 🐳 **Installation Docker (Recommandée)**

``
# Télécharger l'image Docker
docker pull imensalhi275/qboard-adi-app:latest

# Lancer le conteneur
docker run -d -p 5000:5000 --name qboard-app imensalhi275/qboard-adi-app:latest

# Vérifier le statut
docker logs qboard-app

---

## 🚀 Utilisation

### 🌐 **Accès à l'application**

1. **🔗 Ouvrir l'application**
   
   Local: http://localhost:5000
   Docker: http://your-server-ip:5000
   

2. **🔐 Connexion**
   - Utilisez vos identifiants ADI

### 📊 **Fonctionnalités par Rôle**

#### 👑 **Interface Admin**
```
📈 Dashboard Principal → Vue globale tous ateliers
👥 Gestion Utilisateurs → CRUD complet utilisateurs  
⚙️  Configuration Seuils → Limites par atelier/indicateur
💰 Saisie CNQ → Coûts de Non-Qualité
📊 Analytics Avancées → Comparaisons multi-années
```

#### 🔧 **Interface Chargé Qualité**
```
📝 Saisie Données → Formulaire mensuel atelier
📊 Mes Graphiques → Indicateurs de mon périmètre
📋 Consultation → Historique de mes données
📈  YTD → Métriques cumulées 
```

#### 👀 **Interface Consultation**
```
📊 Tableaux de Bord → Vue lecture graphiques
📋 Données Publiques → Consultation limitée
📈 Tendances → Analyses générales
```

### 🔄 **Workflow Typique**

1. **🔑 Admin** configure les seuils et utilisateurs
2. **👨‍🔧 Chargé Qualité** saisit les données mensuelles
3. **📊 Système** calcule automatiquement les métriques
4. **👀 Tous** consultent les résultats en temps réel

---


## 🐳 Déploiement

Docker : Conteneurisation de l'application pour un déploiement simplifié.

Docker Hub : Image disponible à hub.docker.com/r/imensalhi275/qboard-adi-app.

GitHub Actions : Pipeline CI/CD pour construire et pousser l'image Docker.
### ☁️ **Production avec Docker**


# Build custom image
docker build -t qboard-production .

# Run avec variables d'environnement
docker run -d \
  -p 80:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://... \
  --name qboard-prod \
  qboard-production


### 🔧 **Configuration Nginx (Optionnelle)**

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


---
**🐳 Déploiement sur Docker Hub**

L’image est disponible sur Docker Hub :

hub.docker.com/r/imensalhi275/qboard-adi-app

Image : imensalhi275/qboard-adi-app:latest

Commande par défaut : Utilise gunicorn pour servir l’application en production.

## 🧪 Tests

### 🔍 **Exécution des Tests**


# Tests unitaires
python -m pytest tests/ -v

# Tests avec couverture
python -m pytest --cov=app --cov-report=html tests/

# Tests d'intégration
python -m pytest tests/integration/ -v

# Tests API
python -m pytest tests/api/ -v


<div align="center">


Made with ❤️ for ADI Quality Management

</div>
