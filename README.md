<div align="center">

<img src="assets/YggTrackerCut.png" alt="YggTrackerCut logo" width="400">

# YggTrackerCut

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/starkev/YggTrackerCut/releases)
[![Platform](https://img.shields.io/badge/platform-Docker-lightgrey.svg)](https://hub.docker.com/r/starkev/yggtrackercut)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[English](#english) | [Français](#français)

</div>

---

# English

## Description

**YggTrackerCut** connects to qBittorrent's Web UI and automatically removes a specific tracker (originally built for Yggreborn) from a torrent as soon as it starts downloading, once a configurable data threshold is reached. This avoids affecting the tracker's ratio tracking once the download is underway.

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Targeted removal | Removes only the configured tracker, leaves all others untouched |
| 2 | Threshold-based | Triggers once a torrent has downloaded a set amount (in MB) |
| 3 | Continuous monitoring | Runs as a background loop, checks active downloads periodically |
| 4 | Auto-reconnect | Re-authenticates automatically if the WebUI session expires |
| 5 | Docker-ready | Ships as a container, configurable entirely via environment variables |

## Requirements

- qBittorrent with **Web UI** enabled
- Docker (or Python 3.12+ if run standalone)

# Installation & Usage

### Option 1 — Docker (recommended)

```bash
docker run -d \
  --name yggtrackercut \
  --network host \
  -e QBIT_URL="http://localhost:8080" \
  -e QBIT_USER="admin" \
  -e QBIT_PASS="yourpassword" \
  -e TRACKER_MATCH="tracker.yggreborn.org" \
  -e THRESHOLD_MB="10" \
  -e CHECK_INTERVAL="10" \
  TON_PSEUDO/yggtrackercut:latest
```

### Option 2 — Docker Compose

```bash
docker compose up -d
```

### Option 3 — Python script

```bash
pip install requests
python3 YggTrackerCut.py
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `QBIT_URL` | qBittorrent Web UI address | `http://localhost:8080` |
| `QBIT_USER` | Web UI username | `admin` |
| `QBIT_PASS` | Web UI password | `changeme` |
| `TRACKER_MATCH` | Substring identifying the tracker to remove | `tracker.yggreborn.org` |
| `THRESHOLD_MB` | Download threshold in MB before removal | `10` |
| `CHECK_INTERVAL` | Seconds between each check | `10` |

## Notes

- Only torrents with status **"downloading"** are checked, to limit unnecessary API calls.
- The container uses `network_mode: host` to reach qBittorrent on `localhost`.

## Disclaimer

Removing a tracker changes how a torrent reports activity to that tracker. You are solely responsible for how you use this tool and for complying with the rules of any tracker or site you use it with.

---

# Français

## Description

**YggTrackerCut** se connecte au WebUI de qBittorrent et supprime automatiquement un tracker précis (conçu à l'origine pour Yggreborn) d'un torrent dès qu'il commence à télécharger, une fois un seuil de données configurable atteint. Cela évite d'impacter le suivi de ratio du tracker une fois le téléchargement lancé.

## Fonctionnalités

| # | Fonctionnalité | Description |
|---|---|---|
| 1 | Suppression ciblée | Ne retire que le tracker configuré, laisse tous les autres intacts |
| 2 | Basé sur un seuil | Se déclenche une fois un volume défini (en Mo) téléchargé |
| 3 | Surveillance continue | Tourne en boucle en arrière-plan, vérifie les téléchargements actifs |
| 4 | Reconnexion auto | Se ré-authentifie automatiquement si la session WebUI expire |
| 5 | Prêt pour Docker | Fourni en container, entièrement configurable via variables d'environnement |

## Prérequis

- qBittorrent avec le **WebUI** activé
- Docker (ou Python 3.12+ en usage autonome)

## Installation & Utilisation

### Option 1 — Docker (recommandé)

```bash
docker run -d \
  --name yggtrackercut \
  --network host \
  -e QBIT_URL="http://localhost:8080" \
  -e QBIT_USER="admin" \
  -e QBIT_PASS="tonmotdepasse" \
  -e TRACKER_MATCH="tracker.yggreborn.org" \
  -e THRESHOLD_MB="10" \
  -e CHECK_INTERVAL="10" \
  TON_PSEUDO/yggtrackercut:latest
```

### Option 2 — Docker Compose

```bash
docker compose up -d
```

### Option 3 — Script Python

```bash
pip install requests
python3 YggTrackerCut.py
```

## Variables d'environnement

| Variable | Description | Valeur par défaut |
|---|---|---|
| `QBIT_URL` | Adresse du WebUI qBittorrent | `http://localhost:8080` |
| `QBIT_USER` | Identifiant WebUI | `admin` |
| `QBIT_PASS` | Mot de passe WebUI | `changeme` |
| `TRACKER_MATCH` | Sous-chaîne identifiant le tracker à supprimer | `tracker.yggreborn.org` |
| `THRESHOLD_MB` | Seuil de déclenchement en Mo | `10` |
| `CHECK_INTERVAL` | Intervalle entre deux vérifications, en secondes | `10` |

## Notes

- Seuls les torrents au statut **"en téléchargement"** sont vérifiés, pour limiter les appels API inutiles.
- Le container utilise `network_mode: host` pour joindre qBittorrent sur `localhost`.

## Avertissement

Supprimer un tracker modifie la façon dont un torrent remonte son activité à ce tracker. Tu es seul responsable de l'usage de cet outil et du respect des règles du tracker ou du site avec lequel tu l'utilises.
