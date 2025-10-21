FROM python:3.9-slim

RUN pip install --no-cache-dir scapy

WORKDIR /app

COPY . /app

ENTRYPOINT ["python", "arp_spoofer.py"]
