# Install Guide
## Common Steps
1. Install packages
    ```
    sudo apt install git python3-pip python3-tk libspatialindex-dev libhdf5-serial-dev netcdf-bin libnetcdf-dev
    ```

2. Upgrade pip3
    ```
    pip3 install --upgrade --user pip
    ```

3. Install virtualenv
    ```
    pip3 install virtualenv
    ```

4. Clone this repository
   ```
   git clone https://github.com/LiquidGalaxyLAB/Seasight-Forecasting.git
   ```

5. Move the API credentials file to HOME
   ```
   mv Seasight-Forecasting/.cdsapirc $HOME
   ```

6. Go inside the newly created folder
   ```
   cd Seasight-Forecasting
   ```

7. Create virtualenv with python3
   ```
   virtualenv -p python3 <"VIRTUALENV FOLDER">
   ```

## For Django Web Application
1. Activate Virtual Env
   ```
   source <"VIRTUALENV FOLDER">/bin/activate
   ```

2. Change to Django folder
   ```
   cd django
   ```

3. Install requirements
   ```
   pip3 install -r requirements.txt
   ```

4. Add server as allowed host adding Server's IP inside `ALLOWED_HOSTS` in `Seasight-Forecasting/djang/mysite/settings.py` as the following:
   ```
   ALLOWED_HOSTS = ['XXX.XXX.XXX.XXX']
   ```

5. Apply migrations
   ```
   python manage.py migrate
   ```

## RUN
1. Modify `app.conf` file adding the Server's IP and the Master's IP

2. Ensure you are inside `Seasight-Forecasting/django`

3. Run the application
    ```
    ./startDjango.sh
    ```

4. Run the script
   ```
   ./setMasterKmlTxt.sh
   ```