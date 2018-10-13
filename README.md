# Flask-app
A flask app that calls an API to fetch 6 months of stock price

Libraries#
flask       microframework used to build this website
urllib      urllib.request for opening and reading URLs
json        load the data coming from API Call
sqlite3     database used to store 6 months of data fetched during the API call
os          Operating System command to delete older images
pandas      Data is being processed using dataframe
matplotlib  Create a plot to display on the website
datetime    use date to define filename 
time        use date to define filename

API used# https://api.iextrading.com/1.0/stock/voo/chart/6m This API will fetch 6 months of stock data for Vanguard S&P 500

File createDB.py creates database file dbAPI.db

Website can be accessed using url: http://127.0.0.1:5000/

Output will include a 6 month stock chart and summarized information for that stock
Highest Stock price value :$XXX
Lowest Stock price value :$XXX
Maximum Intraday gain :$XXX
Maximum Intraday loss :$XXX
