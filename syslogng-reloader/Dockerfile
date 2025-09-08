FROM balabit/syslog-ng:latest

RUN (apt-get update && apt-get install -y --no-install-recommends inotify-tools ca-certificates && rm -rf /var/lib/apt/lists/*) \
 || (apk add --no-cache inotify-tools ca-certificates)

RUN mkdir -p /run

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
