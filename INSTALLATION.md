# Create Virtual Environment

If this is the first time running the App, make sure your virtual environment is set-up : 
```
MacOS / UNIX > python3 -m venv env
WINDOWS > py -m venv env
```
After creating the environment, activate it by running :
```
MacOS / UNIX > source env/bin/activate
WINDOWS > .\env\Scripts\activate
```
Install the dependencies 

```bash
 pip install -r requirements.txt
```

You can now run the App

```bash
 flask  --debug run
```

## Documentation
* Flask documentation: https://flask.palletsprojects.com/

* Web scraping with BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/