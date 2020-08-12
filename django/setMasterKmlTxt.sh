ip=`ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
kml_file='/var/www/html/kmls.txt'
slave_file='/var/www/html/kml/slave_2.kml'

ssh $1 "
    echo 'http://$ip:81/static/kml/SST_regions.kml' > $kml_file
    echo '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2">
    <Document>
        <Folder>
            <name>Temperature regions</name>
            <ScreenOverlay>
                <name>Logo</name>
                <Icon>
                <href>http://$ip:8000/static/seasight_forecasting/logos/Logos.png</href>
                </Icon>
                <overlayXY x="0" y="1" xunits="fraction" yunits="fraction"/>
                <screenXY x="0.02" y="0.9" xunits="fraction" yunits="fraction"/>
                <rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/>
                <size x="0.1" y="0.2" xunits="fraction" yunits="fraction"/>
            </ScreenOverlay>
        </Folder>
    </Document>' > $slave_file
"