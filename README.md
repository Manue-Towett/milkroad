## Requires python 3.10+
- make sure to click on "Add to PATH" when installing.

## Also requires zyte-smartproxy-ca.crt certificate
- To download the certificate, go to https://docs.zyte.com/_static/zyte-proxy-ca.crt

- Follow the instructions here to install: https://docs.zyte.com/smart-proxy-manager/next-steps/fetching-https-pages-with-smart-proxy.html#fetching-https-pages-with-smart-proxy

- After installing, get the path to the certificate on your local machine
and go to the utils directory in this directory and set the VERIFY field to be equal to the path to your file. Currently, it is as follows:

```VERIFY = '/usr/local/share/ca-certificates/zyte-smartproxy-ca.crt'```

- '/usr/local/share/ca-certificates/zyte-smartproxy-ca.crt' is the path to the certificate in my linux machine

## Usage

- Open the command prompt / terminal

- cd into the milkroad folder

- If running for the first time, type the following command and press enter to install all the dependencies

    ```pip install -r requirements.txt```

- To run the scraper, type the following command and press enter:

    - For Linux/Mac:
        ```python3 main.py```
    
    -For windows:
        ```python main.py```

- Formatted templates will be downloaded to "milkroad" subfolder and images will be downloaded to the images folder.