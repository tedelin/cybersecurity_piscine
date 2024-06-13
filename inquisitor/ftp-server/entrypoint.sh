#!/bin/bash

mkdir -p /var/run/vsftpd/empty
chown root:root /var/run/vsftpd/empty

useradd -m -s /bin/bash "$FTP_USER"
echo "$FTP_USER:$FTP_PASSWORD" | chpasswd

usr/sbin/vsftpd /etc/vsftpd.conf