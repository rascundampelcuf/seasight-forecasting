server_ip=$(awk -F "=" '/server_IP/ {print $2}' app.conf)
server_ip=${server_ip// /}

python manage.py runserver $server_ip:8000