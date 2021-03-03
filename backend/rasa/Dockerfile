# Extend the official Rasa SDK image
FROM rasa/rasa:latest-full

USER root

# Add a custom python library (e.g. jupyter)
RUN pip install --no-cache-dir rasa[transformers]

COPY requirements.txt ./

RUN pip install -r requirements.txt
