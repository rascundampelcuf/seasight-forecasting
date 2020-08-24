
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
kml += '\n ' + '<Document>'
kml += '\n  ' + '<Folder>'
kml += '\n   ' + '<name>Logos</name>'
kml += '\n   ' + '<ScreenOverlay>'
kml += '\n    ' + '<name>Logo</name>'
kml += '\n    ' + '<Icon>'
kml += '\n     ' + '<href>http://{}:8000/static/logos/Logos.png</href>'.format(server_IP)
kml += '\n    ' + '</Icon>'
kml += '\n    ' + '<overlayXY x=\\\"0\\\" y=\\\"1\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '\n    ' + '<screenXY x=\\\"0.02\\\" y=\\\"0.98\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '\n    ' + '<rotationXY x=\\\"0\\\" y=\\\"0\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '\n    ' + '<size x=\\\"0.95\\\" y=\\\"0.3\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
kml += '\n   ' + '</ScreenOverlay>'
kml += '\n  ' + '</Folder>'
kml += '\n ' + '</Document>'
kml += '\n' + '</kml>'

logos_file_target = '/var/www/html/kml/slave_{}.kml'.format(screen_for_logos)

command = "sshpass -p {} ssh {} echo \"'{}' > {}\"".format(lg_pass, lg_IP, kml, logos_file_target)
print(command)
os.system(command)
