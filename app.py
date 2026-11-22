import streamlit as st
import pandas as pd
from machine_learning.src.feature_builder import build_features
from machine_learning.src.predictor import predict_rtt

st.title("Supervision réseau")


@st.cache_data
def charger():
    df = pd.read_csv("data/localnet_dynamics.csv")
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
    return df


@st.cache_data
def predire(history):
    features = build_features(history)
    return predict_rtt(features.iloc[0].to_dict())


df = charger()

# Menu de gauche
run = st.sidebar.selectbox("Session de mesure", df["run_id"].unique())
nb = st.sidebar.slider("Points affichés", 50, 1000, 200)
seuil_lat = st.sidebar.slider("Seuil latence (ms)", 10, 500, 100)
seuil_perte = st.sidebar.slider("Seuil perte (%)", 0, 50, 5)

d = df[df["run_id"] == run].sort_values("sample_index")

# Indicateurs
c1, c2, c3 = st.columns(3)
c1.metric("Latence moyenne", f"{d['rtt_avg_ms'].mean():.1f} ms")
c2.metric("Jitter moyen", f"{d['jitter_ms'].mean():.1f} ms")
c3.metric("Perte de paquets", f"{d['packet_loss_pct'].mean():.1f} %")

# Alertes sur la dernière mesure
derniere = d.iloc[-1]
if derniere["packet_loss_pct"] > seuil_perte:
    st.error(f"⚠️ Perte de paquets élevée : {derniere['packet_loss_pct']:.0f} %")
elif derniere["rtt_avg_ms"] > seuil_lat:
    st.warning(f"⚠️ Latence élevée : {derniere['rtt_avg_ms']:.0f} ms")
else:
    st.success("✅ Réseau OK")

st.dataframe(d.tail(10))

# Graphiques
g = d.tail(nb).set_index("timestamp_utc")
st.subheader("Latence dans le temps")
st.line_chart(g[["rtt_avg_ms"]])
st.subheader("Jitter")
st.line_chart(g["jitter_ms"])
st.subheader("Perte de paquets")
st.bar_chart(g["packet_loss_pct"])

# Prédiction du modèle de P2
st.subheader("Prédiction du modèle (RF12)")
try:
    rtt_predit = predire(d.tail(13))
    st.metric("Prochain RTT prédit", f"{rtt_predit:.1f} ms")
    if rtt_predit > seuil_lat:
        st.warning("⚠️ Latence élevée prévue")
    else:
        st.success("✅ Latence prévue normale")
except Exception as e:
    st.error(f"Prédiction impossible : {e}")