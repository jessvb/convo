# Extend the official Rasa SDK image
FROM rasa/rasa:1.8.1

USER root

# Add a custom python library (e.g. jupyter)
RUN pip install --no-cache-dir rasa[transformers]
