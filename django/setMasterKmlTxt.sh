ip=`ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
file='/var/www/html/kmls.txt'

ssh $1 "echo 'http://$ip:81/static/kml/SST_regions.kml' > $file"