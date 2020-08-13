server_ip=$(awk -F "=" '/server_IP/ {print $2}' app.conf)
server_ip=${server_ip// /}
master_ip=$(awk -F "=" '/master_IP/ {print $2}' app.conf)
master_ip=${master_ip// /}
screen_for_logos=$(awk -F "=" '/screen_for_logos/ {print $2}' app.conf)
screen_for_logos=${screen_for_logos// /}
screen_for_colorbar=$(awk -F "=" '/screen_for_colorbar/ {print $2}' app.conf)
screen_for_colorbar=${screen_for_colorbar// /}

kml_file_source='http://'$server_ip':8000/static/kml/SST_regions.kml'

kml_file_target='/var/www/html/kmls.txt'
logos_file_target='/var/www/html/kml/slave_'$screen_for_logos'.kml'
colorbar_file_target='/var/www/html/kml/slave_'$screen_for_colorbar'.kml'

ssh $master_ip "
    echo $kml_file_source > $kml_file_target
    echo '<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\">
    <Document>
        <Folder>
            <name>Logos</name>
            <ScreenOverlay>
                <name>Logo</name>
                <Icon>
                <href>http://$server_ip:8000/static/logos/Logos.png</href>
                </Icon>
                <overlayXY x=\"0\" y=\"1\" xunits=\"fraction\" yunits=\"fraction\"/>
                <screenXY x=\"0.02\" y=\"0.9\" xunits=\"fraction\" yunits=\"fraction\"/>
                <rotationXY x=\"0\" y=\"0\" xunits=\"fraction\" yunits=\"fraction\"/>
                <size x=\"0.1\" y=\"0.2\" xunits=\"fraction\" yunits=\"fraction\"/>
            </ScreenOverlay>
        </Folder>
    </Document>' > $logos_file_target
    echo '<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\">
    <Document>
        <Folder>
            <name>Colorbar</name>
            <ScreenOverlay>
                <name>Colorbar</name>
                <Icon>
                <href>http://$server_ip:8000/static/img/colorbar.png</href>
                </Icon>
                <overlayXY x=\"0\" y=\"1\" xunits=\"fraction\" yunits=\"fraction\"/>
                <screenXY x=\"0.85\" y=\"0.3\" xunits=\"fraction\" yunits=\"fraction\"/>
                <rotationXY x=\"0\" y=\"0\" xunits=\"fraction\" yunits=\"fraction\"/>
                <size x=\"0.1\" y=\"0.6\" xunits=\"fraction\" yunits=\"fraction\"/>
            </ScreenOverlay>
        </Folder>
    </Document>' > $colorbar_file_target
"