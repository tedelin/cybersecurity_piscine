sudo systemctl restart tor
sudo export onion_site=$(cat /var/lib/tor/ft_onion/hostname)
sed -i "3i $onion_site" /etc/nginx/sites-available/nginx.conf
sudo systemctl restart nginx