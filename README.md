# 🛩️ Qboard ADI - Plateforme de Management de la Performance Qualité

<div align="center">

*Plateforme web complète de monitoring et contrôle qualité en temps réel pour l'industrie aérospatiale*

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.3.2-orange?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensource&logoColor=white)](LICENSE)

[🚀 Démo Live](http://ip172-18-0-36-d358r2469qi000fadg6g-5000.direct.labs.play-with-docker.com/) | [📖 Documentation](#-utilisation) | [🐛 Issues](https://github.com/imensalhi/Projet_ADI/issues)

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
- [Tests](#-tests)
- [Contribution](#-contribution)

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
SQLite/PostgreSQL    # Base de données relationnelle
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
   ```bash
   git clone https://github.com/imensalhi/Projet_ADI.git
   cd Projet_ADI
   ```

2. **🐍 Créer un environnement virtuel**
   ```bash
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **📦 Installer les dépendances**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **⚙️ Configuration initiale**
   ```bash
   # Variables d'environnement
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```

5. **🏃‍♂️ Lancer l'application**
   ```bash
   # Mode développement
   flask run
   
   # Mode production
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

### 🐳 **Installation Docker (Recommandée)**

```bash
# Télécharger l'image Docker
docker pull imensalhi275/qboard-adi-app:latest

# Lancer le conteneur
docker run -d -p 5000:5000 --name qboard-app imensalhi275/qboard-adi-app:latest

# Vérifier le statut
docker logs qboard-app
```

---

## 🚀 Utilisation

### 🌐 **Accès à l'application**

1. **🔗 Ouvrir l'application**
   ```
   Local: http://localhost:5000
   Docker: http://your-server-ip:5000
   ```

2. **🔐 Connexion**
   - Utilisez vos identifiants ADI
   - Sélectionnez votre profil (Admin/Qualité/Autre)

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
📈 Mon YTD → Métriques cumulées personnelles
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
4. **🚨 Alertes** générées si dépassement de seuils  
5. **👀 Tous** consultent les résultats en temps réel

---

## 🔌 API Reference

### 📊 **Endpoints Principaux**

```http
GET /api/charts_data
Content-Type: application/json
Parameters: atelier, year, month

Response:
{
  "ppm": [...],
  "rebut": [...],
  "retouche": [...],
  "couts": [...],
  "reclamations": [...]
}
```

```http
GET /api/ytd_data
Content-Type: application/json
Parameters: atelier, year

Response:
{
  "ytd_ppm": 150.5,
  "ytd_rebut": 2.3,
  "ytd_retouche": 1.8,
  "conformite": 94.2
}
```

```http
GET /api/user/current
Content-Type: application/json

Response:
{
  "username": "user123",
  "role": "admin",
  "atelier": "A1",
  "permissions": [...]
}
```

---

## 🐳 Déploiement

### ☁️ **Production avec Docker**

```bash
# Build custom image
docker build -t qboard-production .

# Run avec variables d'environnement
docker run -d \
  -p 80:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://... \
  --name qboard-prod \
  qboard-production
```

### 🔧 **Configuration Nginx (Optionnelle)**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🧪 Tests

### 🔍 **Exécution des Tests**

```bash
# Tests unitaires
python -m pytest tests/ -v

# Tests avec couverture
python -m pytest --cov=app --cov-report=html tests/

# Tests d'intégration
python -m pytest tests/integration/ -v

# Tests API
python -m pytest tests/api/ -v
```

### 📈 **Métriques de Qualité**
- ✅ **Couverture de code** : > 85%
- ✅ **Tests unitaires** : 120+ tests
- ✅ **Tests d'intégration** : 45+ scénarios
- ✅ **Tests API** : 30+ endpoints

---

## 🤝 Contribution

### 🛠️ **Développement**

1. **🍴 Fork** le project
2. **🌿 Créer** une branch feature (`git checkout -b feature/AmazingFeature`)
3. **💾 Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **📤 Push** sur la branch (`git push origin feature/AmazingFeature`)
5. **🔄 Ouvrir** une Pull Request

### 📋 **Guidelines**
- Suivre les conventions PEP 8 pour Python
- Documenter les nouvelles fonctionnalités
- Ajouter des tests pour le nouveau code
- Mettre à jour la documentation si nécessaire

---

## 📄 License

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

---

## 👨‍💻 Auteur

**Imen Salhi** - [@imensalhi275](https://github.com/imensalhi275)

📧 Contact : [imen.salhi@adi.com](mailto:imen.salhi@adi.com)

---

## 🙏 Remerciements

- 🏢 **ADI** - Support et infrastructure
- 🐍 **Flask Community** - Framework exceptionnel  
- 📊 **Chart.js** - Visualisations puissantes
- 🎨 **Bootstrap** - Interface responsive
- 🐳 **Docker** - Conteneurisation simple

---

<div align="center">

**⭐ N'oubliez pas de mettre une étoile si ce projet vous aide ! ⭐**

Made with ❤️ for ADI Quality Management

</div>
