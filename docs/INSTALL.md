# Install Guide
## Common Steps
1. Install packages
    ```
    sudo apt install git python3-pip python3-tk
    ```

2. Upgrade pip3
    ```
    sudo pip3 install --upgrade pip
    ```

3. Install virtualenv
    ```
    pip3 install virtualenv
    ```

4. Clone this repository
   ```
   git clone https://github.com/LiquidGalaxyLAB/Seasight-Forecasting.git
   ```

5. Go inside the newly created folder
   ```
   cd Seasight-Forecasting
   ```

6. Create virtualenv with python3
   ```
   virtualenv -p python3 <"VIRTUALENV FOLDER">
   ```

## For Django Web Application
1. Activate Virtual Env
   ``` 
   source <"VIRTUALENV FOLDER">/bin/activate
   ```

2. Install requirements
   ```
   pip3 install -r django/requirements.txt
   ```

3. Apply migrations
   ```
   python manage.py migrate
   ```

## For LG master
1. Add in /var/www/html/kmls.txt the following line:
    ```
    http://<SERVER-IP>:81/Seasight-Forecasting/data/SST_regions.kml
    ```

## RUN
1. Run the application with:
    ```
    python3 django/manage.py runserver
    ```