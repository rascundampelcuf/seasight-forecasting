$ip = ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'

ssh $1 << EOF
    vi /var/www/html/kmls.txt
    i
    http://$ip:81/static/kml/SST_regions.kml
    ^[
    ZZ
    x23LimitStringx23
EOF