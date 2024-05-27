FROM debian:bookworm

RUN apt-get update && apt-get install -y openssh-server nginx tor 

RUN mkdir -p /var/www/html/ft_onion
COPY torrc /etc/tor/torrc
COPY index.html /var/www/html/ft_onion
COPY nginx.conf /etc/nginx/sites-available/
COPY sshd_config /etc/ssh/sshd_config
RUN mv /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-available/site.conf && \
    ln -s /etc/nginx/sites-available/site.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]