FROM debian:stable-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data

ENTRYPOINT ["pdftoppm"]
