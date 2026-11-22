# Système intelligent de supervision réseau : prédiction des performances par machine learning

Projet de groupe : prédiction de la latence réseau (RTT) avec un modèle Random Forest (RF12) et un dashboard Streamlit de supervision.

## Architecture
Les données (data/) --> le modèle RF12 (machine_learning/) --> le dashboard (app.py)

## Prérequis
- Git et Git LFS
- Docker Desktop
- Le modèle machine_learning/models/rf12_localnet_dynamics.pkl (téléchargé avec : git lfs pull)

## Lancer le dashboard
    git lfs pull
    docker compose up --build

Puis ouvrir http://localhost:8501

## Documentation du module machine learning
Voir README_ML.md

## CI/CD
À chaque push et pull request, GitHub Actions vérifie la syntaxe Python, construit l'image Docker et teste le démarrage du dashboard.

## Le travail de groupe
- Utiliser un jeu de données existant, trouvé et réutilisé (non collecté par le groupe)
- Entraîner le modèle de machine learning
- Créer le dashboard
- Intégrer et déployer le projet avec Docker
