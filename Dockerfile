FROM tiangolo/uwsgi-nginx:python3.6

LABEL maintainer="Marco Graetsch <magdev3.0@gmail.com>"

ENV OPDSPROXY_SCRAPY_LOG_FILE="/app/data/scrapy.log" \
	OPDSPROXY_DJANGO_ENV="development" \
	UWSGI_INI="/app/uwsgi.ini" \
	LISTEN_PORT=80

RUN apt-get update \
	&& apt-get install --no-install-recommends -y \
      avahi-daemon \
	&& rm -rf /var/lib/apt/lists/* \
	&& update-rc.d dbus enable \
	&& update-rc.d avahi-daemon enable

VOLUME ["/app/data"]
WORKDIR /app
COPY . .

RUN rm -f /etc/nginx/conf.d/nginx.conf \
	&& rm -f /etc/supervisor/conf.d/supervisord.conf \
	&& mv docker/nginx.conf /etc/nginx/conf.d/nginx.conf \
	&& mv docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf \
	&& mv docker/scrapyd.conf crawler/scrapyd.conf \
	&& mv docker/uwsgi.ini uwsgi.ini \
	&& mv docker/opds-proxy.service /etc/avahi/services/opds-proxy.service \
	&& mv docker/entrypoint.sh /entrypoint.sh \
	&& chmod +x /entrypoint.sh \
	&& pip install --upgrade pip \
	&& pip install -r requirements.txt

#EXPOSE 80 6800 8081
EXPOSE 80 6800
