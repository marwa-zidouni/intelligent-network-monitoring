import streamlit as st
import pandas as pd
from machine_learning.src.feature_builder import build_features
from machine_learning.src.predictor import predict_rtt

st.title("Supervision réseau (live)")

nb = st.sidebar.slider("Points affichés", 20, 500, 100)
seuil_lat = st.sidebar.slider("Seuil latence (ms)", 10, 500, 100)
seuil_perte = st.sidebar.slider("Seuil perte (%)", 0, 50, 5)


@st.cache_data(ttl=10)
def charger():
    df = pd.read_csv("data/live_data.csv")
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])
    df["gap_before_s"] = df["epoch_s"].diff()
    df = df[df["run_id"] == df["run_id"].iloc[-1]]
    return df


@st.fragment(run_every=30)
def dashboard(nb, seuil_lat, seuil_perte):
    try:
        d = charger()
    except FileNotFoundError:
        st.warning("Lance d'abord live_collector.py")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Latence moyenne", f"{d['rtt_avg_ms'].mean():.1f} ms")
    c2.metric("Jitter moyen", f"{d['jitter_ms'].mean():.1f} ms")
    c3.metric("Perte de paquets", f"{d['packet_loss_pct'].mean():.1f} %")

    derniere = d.iloc[-1]
    if derniere["packet_loss_pct"] > seuil_perte:
        st.error(f"Perte de paquets élevée : {derniere['packet_loss_pct']:.0f} %")
    elif derniere["rtt_avg_ms"] > seuil_lat:
        st.warning(f"Latence élevée : {derniere['rtt_avg_ms']:.0f} ms")
    else:
        st.success("Réseau OK")

    st.dataframe(d.tail(10))

    g = d.tail(nb).set_index("timestamp_utc")
    st.subheader("Latence dans le temps")
    st.line_chart(g["rtt_avg_ms"])
    st.subheader("Jitter")
    st.line_chart(g["jitter_ms"])
    st.subheader("Perte de paquets")
    st.bar_chart(g["packet_loss_pct"])

    st.subheader("Prédiction du modèle (RF12)")
    if len(d) < 13:
        st.info(f"En attente de mesures : {len(d)}/13")
        return
    try:
        features = build_features(d.tail(13))
        rtt = predict_rtt(features.iloc[0].to_dict())
        st.metric("Prochain RTT prédit", f"{rtt:.1f} ms")
        if rtt > seuil_lat:
            st.warning("Latence élevée prévue")
        else:
            st.success("Latence prévue normale")

        if len(d) >= 14:
             f_prec = build_features(d.iloc[-14:-1])
             rtt_prec = predict_rtt(f_prec.iloc[0].to_dict())
             reel = d.iloc[-1]["rtt_avg_ms"]
             a, b, c = st.columns(3)
             a.metric("Prédit (avant la dernière mesure)", f"{rtt_prec:.1f} ms")
             b.metric("Réel mesuré", f"{reel:.1f} ms")
             c.metric("Écart", f"{abs(reel - rtt_prec):.1f} ms")
    except Exception as e:
        st.error(f"Prédiction impossible : {e}")


dashboard(nb, seuil_lat, seuil_perte)