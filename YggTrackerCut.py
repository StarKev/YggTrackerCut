#!/usr/bin/env python3

import os
import time
import requests

# ----------------- CONFIGURATION (via variables d'environnement) -----------------
QBIT_URL = os.environ.get("QBIT_URL", "http://localhost:8080")
QBIT_USER = os.environ.get("QBIT_USER", "admin")
QBIT_PASS = os.environ.get("QBIT_PASS", "changeme")

# Sous-chaîne identifiant le tracker à supprimer (pas besoin de l'URL exacte)
TRACKER_MATCH = os.environ.get("TRACKER_MATCH", "tracker.yggreborn.org")

# Seuil de déclenchement, en Mo (mets simplement 1 ou 10 par exemple)
THRESHOLD_MB = float(os.environ.get("THRESHOLD_MB", 10))
THRESHOLD_BYTES = int(THRESHOLD_MB * 1024 * 1024)

# Intervalle entre deux vérifications, en secondes
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", 10))

# Se reconnecter à la session toutes les X secondes (les sessions qBittorrent expirent)
RELOGIN_INTERVAL = int(os.environ.get("RELOGIN_INTERVAL", 1800))
# -----------------------------------------------------------------------------------


# Se connecte au WebUI qBittorrent et ouvre une session
def login(session):
    r = session.post(
        f"{QBIT_URL}/api/v2/auth/login",
        data={"username": QBIT_USER, "password": QBIT_PASS},
    )
    r.raise_for_status()
    if r.text.strip() != "Ok.":
        raise RuntimeError("Échec de connexion à qBittorrent WebUI")


# Récupère la liste des torrents actuellement en téléchargement
def get_torrents(session):
    r = session.get(
        f"{QBIT_URL}/api/v2/torrents/info",
        params={"filter": "downloading"},
    )
    r.raise_for_status()
    return r.json()


# Récupère la liste des trackers d'un torrent donné
def get_trackers(session, torrent_hash):
    r = session.get(
        f"{QBIT_URL}/api/v2/torrents/trackers",
        params={"hash": torrent_hash},
    )
    r.raise_for_status()
    return r.json()


# Supprime un tracker précis d'un torrent donné
def remove_tracker(session, torrent_hash, tracker_url):
    r = session.post(
        f"{QBIT_URL}/api/v2/torrents/removeTrackers",
        data={"hash": torrent_hash, "urls": tracker_url},
    )
    # 200 = ok, 409 = tracker déjà absent -> on ignore
    if r.status_code not in (200, 409):
        r.raise_for_status()


# Vérifie une fois tous les torrents en téléchargement et supprime le tracker si le seuil est atteint
def check_once(session):
    torrents = get_torrents(session)

    for t in torrents:
        downloaded = t.get("downloaded", 0)
        if downloaded < THRESHOLD_BYTES:
            continue

        torrent_hash = t["hash"]
        trackers = get_trackers(session, torrent_hash)

        for tr in trackers:
            url = tr.get("url", "")
            if TRACKER_MATCH in url:
                print(f"[{t['name']}] seuil atteint ({downloaded} o) -> suppression de {url}", flush=True)
                remove_tracker(session, torrent_hash, url)


# Boucle principale : se connecte puis vérifie les torrents en continu
def main():
    session = requests.Session()
    login(session)
    print("Surveillance démarrée, en attente des torrents...", flush=True)

    last_login = time.time()

    while True:
        try:
            if time.time() - last_login > RELOGIN_INTERVAL:
                login(session)
                last_login = time.time()

            check_once(session)

        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau/API, nouvelle tentative dans {CHECK_INTERVAL}s : {e}", flush=True)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()