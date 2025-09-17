# Image de base légère (Linux Debian-based, Python 3.12)
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements et installer dépendances (optimisé pour cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Vérifie les packages installés
RUN pip freeze
# Vérifie que gunicorn est dans le PATH
RUN which gunicorn
# Copier le code de l'app
COPY . .

# Exposer le port 5000 (port Flask par défaut)
EXPOSE 5000

# Utiliser Gunicorn pour production (multi-threadé)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
