server_ip=$(awk -F "=" '/server_IP/ {print $2}' app.conf)
server_ip=${server_ip// /}
master_ip=$(awk -F "=" '/master_IP/ {print $2}' app.conf)
master_ip=${master_ip// /}
screen_for_logos=$(awk -F "=" '/screen_for_logos/ {print $2}' app.conf)
screen_for_logos=${screen_for_logos// /}
screen_for_colorbar=$(awk -F "=" '/screen_for_colorbar/ {print $2}' app.conf)
screen_for_colorbar=${screen_for_colorbar// /}

kml_file_source='http://'$server_ip':8000/static/kml/SST_regions.kml'
logos_file_source='http://'$server_ip':8000/static/kml/slave_'$screen_for_logos'.kml'
colorbar_file_source='http://'$server_ip':8000/static/kml/slave_'$screen_for_colorbar'.kml'

kml_file_target='/var/www/html/kmls.txt'
logos_file_target='/var/www/html/kml/slave_'$screen_for_logos'.kml'
colorbar_file_target='/var/www/html/kml/slave_'$screen_for_colorbar'.kml'

echo ssh master_ip "
    echo $kml_file_source > $kml_file_target
    echo $logos_file_source > $logos_file_target
    echo $colorbar_file_source > $colorbar_file_target
"