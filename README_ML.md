
# Module Machine Learning — LocalNet-Dynamics

## 1. Présentation

Ce module permet de prédire le prochain RTT valide (latence réseau) à partir de mesures réseau historiques.

Le modèle retenu est Random Forest RF12, entraîné sur le dataset public LocalNet-Dynamics.

La prédiction est exprimée en millisecondes (ms).

## 2. Modèle utilisé

- Algorithme : Random Forest Regressor
- Nom : RF12
- Nombre de variables : 42
- Nombre d'arbres : 300
- `min_samples_leaf` : 3
- `max_features` : 0.8
- `random_state` : 42

## 3. Structure des fichiers

```text
machine_learning/
├── models/
│   ├── rf12_localnet_dynamics.pkl
│   └── features_rf12.pkl
└── src/
    ├── __init__.py
    ├── feature_builder.py
    └── predictor.py

requirements.txt
test_predictor.py
README_ML.md
```

## 4. Installation des dépendances

Depuis la racine du projet :

```powershell
python -m pip install -r requirements.txt
```

## 5. Utilisation du module

Le module expose deux fonctions :

- `build_features(history)` : construit les 42 variables à partir de 13 observations historiques.
- `predict_rtt(input_data)` : effectue la prédiction avec le modèle RF12.

Exemple :

```python
from machine_learning.src.feature_builder import build_features
from machine_learning.src.predictor import predict_rtt

# history doit contenir 13 observations chronologiques
features = build_features(history)

# Conversion de la ligne construite en dictionnaire
input_data = features.iloc[0].to_dict()

# Prédiction du prochain RTT valide
rtt_predit = predict_rtt(input_data)

print(f"RTT prédit : {rtt_predit:.4f} ms")
```

La fonction `predict_rtt()` retourne une valeur numérique exprimée en millisecondes.

## 6. Organisation des variables

Les 42 variables sont réparties en deux groupes.

### Mesures actuelles (6)

- `rtt_avg_ms`
- `rtt_stddev_ms`
- `jitter_ms`
- `packet_loss_pct`
- `gateway_rtt_avg_ms`
- `gateway_jitter_ms`

### Variables historiques (36)

- 12 valeurs historiques de `rtt_avg_ms`
- 12 valeurs historiques de `jitter_ms`
- 12 valeurs historiques de `packet_loss_pct`

Les variables historiques utilisent les suffixes `_lag1` à `_lag12`.

`lag1` correspond à l'observation précédente la plus récente.

## 7. Conditions d'utilisation

- Les 13 observations doivent être ordonnées de la plus ancienne à la plus récente.
- Les 12 intervalles historiques doivent être compris entre 25 et 45 secondes.
- Les mesures nécessaires doivent être présentes et numériques.
- Les variables doivent respecter les noms, unités et définitions utilisés pendant l'entraînement.
- Les périodes d'indisponibilité ne doivent pas être artificiellement interpolées.
- Les observations incomplètes ou les intervalles non conformes sont rejetés par le constructeur de variables.

## 8. Test du module

Depuis la racine du projet :

```powershell
python test_predictor.py
```

Ce script vérifie le chargement du modèle, réalise une prédiction et teste le rejet de données invalides.

Il utilise le dataset local `data/localnet_dynamics.csv`.

## 9. Limites

- Le modèle a été entraîné sur LocalNet-Dynamics.
- Il prédit le prochain RTT valide, et non une latence à un horizon fixe de 60 secondes.
- Il n'est pas encore validé sur les mesures du futur système de collecte de l'équipe.
- Il ne constitue pas à lui seul un système de détection d'anomalies ou de génération d'alertes.
- Les performances observées sur le dataset de test ne garantissent pas les mêmes performances sur un autre réseau.
- Le modèle et le fichier des variables (`.pkl`) sont nécessaires à l'exécution et doivent être fournis séparément, car ils sont exclus de Git.
