#!/bin/bash
yum install httpd -y
echo "<html><body><h1>Hello World!</h1></body></html>" >> /var/www/html/index.html
service httpd start
chkconfig httpd on
