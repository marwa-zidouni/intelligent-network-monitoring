from pathlib import Path
from functools import lru_cache

import joblib
import numpy as np
import pandas as pd


# Chemins des fichiers du modèle
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "rf12_localnet_dynamics.pkl"
FEATURES_PATH = MODEL_DIR / "features_rf12.pkl"


@lru_cache(maxsize=1)
def load_model():
    """Charge une seule fois le modèle RF12 et ses variables."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {MODEL_PATH}"
        )

    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Fichier des variables introuvable : {FEATURES_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)

    if len(features) != model.n_features_in_:
        raise ValueError(
            "Le nombre de variables ne correspond pas au modèle."
        )

    return model, features


def predict_rtt(input_data):
    """
    Prédit le prochain RTT valide avec RF12.

    input_data : dictionnaire contenant les 42 variables.
    Retour : RTT prédit en millisecondes.
    """

    if not isinstance(input_data, dict):
        raise TypeError(
            "Les données doivent être fournies sous forme de dictionnaire."
        )

    model, features = load_model()

    # Vérifier les variables manquantes
    missing_features = [
        feature for feature in features
        if feature not in input_data
    ]

    if missing_features:
        raise ValueError(
            f"Variables manquantes : {missing_features}"
        )

    # Construire les données dans le bon ordre
    X = pd.DataFrame(
        [[input_data[feature] for feature in features]],
        columns=features
    )

    # Vérifier les valeurs numériques
    try:
        X = X.apply(pd.to_numeric, errors="raise")
    except (ValueError, TypeError):
        raise ValueError(
            "Toutes les variables doivent être numériques."
        )

    # Vérifier les valeurs manquantes
    if X.isnull().any().any():
        raise ValueError(
            "Les données contiennent des valeurs manquantes."
        )

    # Vérifier les valeurs infinies
    if not np.isfinite(X.to_numpy(dtype=float)).all():
        raise ValueError(
            "Les données contiennent des valeurs infinies."
        )

    # Effectuer la prédiction
    prediction = model.predict(X)

    return float(prediction[0])