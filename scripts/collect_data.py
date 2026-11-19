import csv, time, os
from datetime import datetime
from icmplib import ping

CIBLES = ["8.8.8.8", "1.1.1.1", "google.com"]
FICHIER = "data.csv"
INTERVALLE = 5  # secondes

def mesurer(host):
    r = ping(host, count=4, interval=0.2, timeout=2, privileged=False)
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "host": host,
        "latence_moy_ms": round(r.avg_rtt, 2),
        "latence_max_ms": round(r.max_rtt, 2),
        "jitter_ms": round(r.jitter, 2),
        "perte_pct": r.packet_loss * 100,
        "disponible": int(r.is_alive),
    }

nouveau = not os.path.exists(FICHIER)
with open(FICHIER, "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=mesurer(CIBLES[0]).keys())
    if nouveau:
        w.writeheader()
    try:
        while True:
            for h in CIBLES:
                w.writerow(mesurer(h))
            f.flush()
            time.sleep(INTERVALLE)
    except KeyboardInterrupt:
        print("Collecte arrêtée.")