import pandas as pd


CURRENT_FEATURES = [
    "rtt_avg_ms",
    "rtt_stddev_ms",
    "jitter_ms",
    "packet_loss_pct",
    "gateway_rtt_avg_ms",
    "gateway_jitter_ms",
]

HISTORICAL_VARIABLES = [
    "rtt_avg_ms",
    "jitter_ms",
    "packet_loss_pct",
]

N_LAGS = 12


def build_features(history):
    """
    Construit les 42 variables nécessaires au modèle RF12.

    history : DataFrame de 13 observations,
              ordonnées de la plus ancienne à la plus récente.

    Retour : DataFrame contenant une seule ligne et 42 variables.
    """

    if len(history) != N_LAGS + 1:
        raise ValueError(
            "Il faut exactement 13 observations pour construire RF12."
        )

    required_columns = CURRENT_FEATURES + ["gap_before_s"]

    missing_columns = [
        col for col in required_columns
        if col not in history.columns
    ]

    for variable in HISTORICAL_VARIABLES:
        if variable not in history.columns:
            missing_columns.append(variable)

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes : {missing_columns}"
        )

    history = history.reset_index(drop=True)

    if history[HISTORICAL_VARIABLES].isnull().any().any():
        raise ValueError(
            "Les historiques contiennent des valeurs manquantes."
        )

    if history.iloc[-1][CURRENT_FEATURES].isnull().any():
        raise ValueError(
            "Les variables de l'observation actuelle sont incomplètes."
        )

    intervals = history["gap_before_s"].iloc[1:]

    if intervals.isnull().any() or not intervals.between(25, 45).all():
        raise ValueError(
            "Les 12 intervalles historiques doivent être compris entre 25 et 45 secondes."
        )

    current = history.iloc[-1]

    features = {}

    for feature in CURRENT_FEATURES:
        features[feature] = current[feature]

    for variable in HISTORICAL_VARIABLES:
        for lag in range(1, N_LAGS + 1):
            features[f"{variable}_lag{lag}"] = (
                history.iloc[-1 - lag][variable]
            )

    return pd.DataFrame([features])