server_ip=$(awk -F "=" '/server_IP/ {print $2}' app.conf)
server_ip=${server_ip// /}
lg_ip=$(awk -F "=" '/lg_IP/ {print $2}' app.conf)
lg_ip=${lg_ip// /}
screen_for_logos=$(awk -F "=" '/screen_for_logos/ {print $2}' app.conf)
screen_for_logos=${screen_for_logos// /}

kml_filename=$(awk -F "=" '/kml_destination_file/ {print $2}' app.conf)
kml_filename=${kml_filename// /}

kml_file_source='http://'$lg_ip':81/SF/'$kml_filename

kml_file_target='/var/www/html/kmls.txt'
logos_file_target='/var/www/html/kml/slave_'$screen_for_logos'.kml'

ssh $lg_ip "
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
                <size x=\"0.5\" y=\"0.5\" xunits=\"fraction\" yunits=\"fraction\"/>
            </ScreenOverlay>
        </Folder>
    </Document>
</kml>' > $logos_file_target
"