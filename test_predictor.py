
import pandas as pd

from machine_learning.src.feature_builder import build_features
from machine_learning.src.predictor import predict_rtt


# Charger le dataset
df = pd.read_csv(
    "data/localnet_dynamics.csv",
    low_memory=False
)

# Sélectionner 13 observations
history = df.iloc[100:113].copy()

# Construire les 42 variables RF12
features = build_features(history)
input_data = features.iloc[0].to_dict()


# Test 1 : prédiction normale
print("\n===== TEST PREDICTOR RF12 =====")

prediction = predict_rtt(input_data)

print(f"Nombre de variables : {len(input_data)}")
print(f"RTT prédit : {prediction:.4f} ms")


# Fonction pour tester les erreurs
def test_error(label, test_data):
    print(f"\n===== {label} =====")

    try:
        predict_rtt(test_data)
        print("ERREUR : les données invalides ont été acceptées.")

    except (ValueError, TypeError) as e:
        print("Erreur détectée correctement :")
        print(e)


# Test 2 : variable manquante
input_incomplete = input_data.copy()
input_incomplete.pop("rtt_avg_ms")

test_error(
    "TEST DONNEES INCOMPLETES",
    input_incomplete
)


# Test 3 : valeur NaN
input_nan = input_data.copy()
input_nan["rtt_avg_ms"] = float("nan")

test_error(
    "TEST VALEURS MANQUANTES",
    input_nan
)


# Test 4 : valeur infinie
input_inf = input_data.copy()
input_inf["rtt_avg_ms"] = float("inf")

test_error(
    "TEST VALEURS INFINIES",
    input_inf
)
