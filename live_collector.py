import csv, os, time, statistics
from datetime import datetime, timezone
from icmplib import ping

CIBLE = "8.8.8.8"
PASSERELLE = "100.94.224.1"   
FICHIER = "data/live_data.csv"
INTERVALLE = 25  # secondes (le modèle veut entre 25 et 45)
RUN_ID = "live_" + datetime.now().strftime("%Y%m%d_%H%M%S")

COLONNES = ["run_id", "sample_index", "timestamp_utc", "epoch_s",
            "rtt_avg_ms", "rtt_stddev_ms", "jitter_ms", "packet_loss_pct",
            "gateway_rtt_avg_ms", "gateway_jitter_ms"]


def mesurer(host):
    r = ping(host, count=10, interval=0.2, timeout=2, privileged=False)
    std = statistics.pstdev(r.rtts) if len(r.rtts) > 1 else 0.0
    return r, std


os.makedirs("data", exist_ok=True)
nouveau = not os.path.exists(FICHIER)
i = 0

with open(FICHIER, "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLONNES)
    if nouveau:
        w.writeheader()
    try:
        while True:
            debut = time.time()
            r, std = mesurer(CIBLE)
            g, _ = mesurer(PASSERELLE)
            vivant = r.packets_received > 0
            w.writerow({
                "run_id": RUN_ID,
                "sample_index": i,
                "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "epoch_s": round(debut, 1),
                "rtt_avg_ms": round(r.avg_rtt, 3) if vivant else "",
                "rtt_stddev_ms": round(std, 3) if vivant else "",
                "jitter_ms": round(r.jitter, 3) if vivant else "",
                "packet_loss_pct": r.packet_loss * 100,
                "gateway_rtt_avg_ms": round(g.avg_rtt, 3) if g.packets_received else "",
                "gateway_jitter_ms": round(g.jitter, 3) if g.packets_received else "",
            })
            f.flush()
            i += 1
            time.sleep(max(0, INTERVALLE - (time.time() - debut)))
    except KeyboardInterrupt:
        print("Collecte arrêtée.")