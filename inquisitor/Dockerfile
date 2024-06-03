FROM debian:bookworm

RUN useradd -ms /bin/bash tedelin

USER tedelin
WORKDIR /home/tedelin

COPY dist/inquisitor ./inquisitor

ENTRYPOINT ["tail", "-f", "/dev/null"]