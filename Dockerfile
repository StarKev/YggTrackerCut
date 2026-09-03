FROM python:3.12-slim

LABEL org.opencontainers.image.title="YggTrackerCut"
LABEL org.opencontainers.image.description="Removes a specific tracker from qBittorrent torrents once a download threshold is reached"

WORKDIR /app

RUN pip install --no-cache-dir requests

COPY YggTrackerCut.py .

# Variables d'environnement, surchargées depuis docker-compose.yml / .env
ENV QBIT_URL="http://localhost:8080"
ENV QBIT_USER="admin"
ENV QBIT_PASS="changeme"
ENV TRACKER_MATCH="tracker.yggreborn.org"
ENV THRESHOLD_MB="10"
ENV CHECK_INTERVAL="10"

CMD ["python3", "-u", "YggTrackerCut.py"]