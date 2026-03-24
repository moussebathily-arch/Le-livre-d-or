# Base image Python
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED 1

# Dossier de travail
WORKDIR /app

# Copier requirements et installer
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY app/ .

# Créer dossier logs
RUN mkdir -p logs

# Exposer le port (si Flask ou API)
EXPOSE 5000

# Commande de lancement
CMD ["python", "app.py"]
