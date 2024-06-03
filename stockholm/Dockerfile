FROM debian:bookworm

RUN useradd -ms /bin/bash tedelin

USER tedelin
WORKDIR /home/tedelin

RUN mkdir -p infection

COPY --chown=tedelin sample infection/sample
COPY dist/stockholm ./stockholm

ENTRYPOINT ["tail", "-f", "/dev/null"]