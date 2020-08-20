
import configparser
import os

config = configparser.ConfigParser()
configFilePath = r'app.conf'
config.read(configFilePath)

server_IP = config['INSTALLATION']['server_IP']
lg_IP = config['INSTALLATION']['lg_IP']
lg_pass = config['INSTALLATION']['lg_pass']
screen_for_logos = int(config['INSTALLATION']['screen_for_logos'])

kml = '<kml xmlns=\\\"http://www.opengis.net/kml/2.2\\\" xmlns:atom=\\\"http://www.w3.org/2005/Atom\\\" xmlns:gx=\\\"http://www.google.com/kml/ext/2.2\\\">'
kml += '<Document>'
kml += '<Folder>'
kml += '<name>Logos</name>'
kml += '<ScreenOverlay>'
kml += '<name>Logo</name>'
kml += '<Icon>'
kml += '<href>http://{}:8000/static/logos/Logos.png</href>'.format(server_IP)
kml += '</Icon>'
kml += '<overlayXY x=\\\"0\\\" y=\\\"1\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '<screenXY x=\\\"0.02\\\" y=\\\"0.9\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '<rotationXY x=\\\"0\\\" y=\\\"0\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '<size x=\\\"0.5\\\" y=\\\"0.5\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '</ScreenOverlay>'
kml += '</Folder>'
kml += '</Document>'
kml += '</kml>'

logos_file_target = '/var/www/html/kml/slave_{}.kml'.format(screen_for_logos)

command = "sshpass -p {} ssh {} echo \"{} > {}\"".format(lg_pass, lg_IP, kml, logos_file_target)
print(command)
os.system(command)
