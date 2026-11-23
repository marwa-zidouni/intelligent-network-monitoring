# Système intelligent de supervision réseau : prédiction des performances par machine learning

Projet de groupe : mesure de la latence réseau par ping, prédiction du prochain RTT avec un modèle Random Forest (RF12) et dashboard Streamlit de supervision en temps réel.

## Architecture
Collecte par ping (live_collector.py) --> data/live_data.csv --> modèle RF12 (machine_learning/) --> dashboard (app.py)

## Prérequis
- Git et Git LFS
- Docker Desktop
- Python 3 (pour la collecte, sur le PC)
- Le modèle machine_learning/models/rf12_localnet_dynamics.pkl (téléchargé avec : git lfs pull)

## Lancer le projet
1. Récupérer le modèle : git lfs pull
2. Régler la passerelle : trouver la "Passerelle par défaut" avec la commande ipconfig, puis la recopier dans la variable PASSERELLE de live_collector.py
3. Lancer la collecte sur le PC (hors Docker, pour garder les vraies valeurs de ping), dans un premier terminal à laisser ouvert :

        pip install -r requirements-collect.txt
        python live_collector.py

4. Lancer le dashboard dans un deuxième terminal :

        docker compose up --build

5. Ouvrir http://localhost:8501

Le modèle a besoin de 13 mesures consécutives : la première prédiction apparaît après environ 5 à 6 minutes de collecte.

## Données
- Les mesures affichées par le dashboard sont collectées par le groupe avec live_collector.py (fichier data/live_data.csv, non versionné).
- Le modèle RF12 a été entraîné sur le dataset public LocalNet-Dynamics (auteur : Alexander Ezharjan, licence MIT, voir THIRD_PARTY_NOTICES.md), présent dans data/localnet_dynamics.csv. Il n'a pas été validé sur les mesures du groupe (voir README_ML.md).

## Documentation du module machine learning
Voir README_ML.md

## CI/CD
À chaque push et pull request, GitHub Actions vérifie la syntaxe Python, construit l'image Docker et teste le démarrage du dashboard. Elle ne teste pas la prédiction : le modèle (environ 255 Mo, stocké avec Git LFS) n'est volontairement pas téléchargé en CI.

## Le travail de groupe
- Collecte des mesures réseau par ping vers 8.8.8.8 et vers la passerelle, sur le PC Windows, hors Docker (live_collector.py)
- Entraînement du modèle de machine learning (jeu de données public LocalNet-Dynamics)
- Création du dashboard : il tourne dans Docker, relit le fichier toutes les 30 secondes et affiche les mesures, les alertes et la prédiction
- Intégration et déploiement du projet avec Docker
