ip=`ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
kml_file='/var/www/html/kmls.txt'
slave2_file='/var/www/html/kml/slave_2.kml'
slave3_file='/var/www/html/kml/slave_3.kml'

ssh $1 "
    echo 'http://$ip:8000/static/kml/SST_regions.kml' > $kml_file
    echo 'http://$ip:8000/static/kml/slave_2.kml' > $slave2_file
    echo 'http://$ip:8000/static/kml/slave_3.kml' > $slave3_file
"