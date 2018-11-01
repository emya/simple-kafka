FROM python:3.6

ENV KAFKA_HOST=kafka:9092 \
    LIBRDKAFKA_VERSION=0.11.3 \
    LIBRDKAFKA_SHA=2b96d7ed71470b0d0027bd9f0b6eb8fb68ed979f8092611c148771eb01abb72c

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN set -ex; \
    pip install --upgrade pip; \
    pip install -U setuptools;

# Install librdkafka for use in Kafka
RUN set -ex; \
    if ! wget "https://github.com/edenhill/librdkafka/archive/v${LIBRDKAFKA_VERSION}.tar.gz"; then \
        echo >&2 "error: failed to download 'librdkafka-v${LIBRDKAFKA_VERSION}'"; \
        exit 1; \
    fi; \
    echo "${LIBRDKAFKA_SHA} v0.11.3.tar.gz" | sha256sum -c -; \
    tar -C /opt -xzf "v${LIBRDKAFKA_VERSION}.tar.gz"; \
    cd "/opt/librdkafka-${LIBRDKAFKA_VERSION}"; \
    ./configure; \
    make -j; \
    make install; \
    ldconfig; \
    rm "/usr/src/app/v${LIBRDKAFKA_VERSION}.tar.gz";


ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app

CMD ["python", "-u", "/usr/src/app/consumer.py"]
