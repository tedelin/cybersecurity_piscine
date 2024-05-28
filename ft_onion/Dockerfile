FROM debian:bookworm

RUN apt-get update && apt-get install -y openssh-server nginx tor 

RUN mkdir -p /var/www/html/ft_onion
RUN mkdir -p /var/lib/tor/ft_onion
COPY torrc /etc/tor/torrc
COPY index.html /var/www/html/ft_onion
COPY sshd_config /etc/ssh/sshd_config
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80 4242

CMD su debian-tor -s /bin/bash -c "tor" & nginx -g 'daemon off;'