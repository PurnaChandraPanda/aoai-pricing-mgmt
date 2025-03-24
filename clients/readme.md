## Pre-requisite packages
```
pip install openai
pip install python-dotenv
```

## Load run the client app
- Set .env with with aoai endpoint and model deployment details
- Run the app with load testing
```
python clientapp.py
```
- This run will generate a log file named `aoai_requests.csv`

## Calculate the tokens usage price for endpoint
```
python tokens_price.py
```