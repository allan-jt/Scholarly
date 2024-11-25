FROM spark:3.5.3-scala2.12-java17-ubuntu

USER root

RUN set -ex; \
    apt-get update; \
    apt-get install -y python3 python3-pip && \
    pip3 install pipenv && \
    apt -y autoremove && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*

COPY init.sh .

CMD ["bash", "init.sh"]