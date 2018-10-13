from flask import Flask
from flask import render_template
import urllib.request
import json
import sqlite3
import os
import pandas as pd                                                         #pip install pandas
import matplotlib.pyplot as plt                                             #pip install matplotlib
import datetime
import time
app = Flask(__name__)

FOLDERNAME= os.path.dirname(app.instance_path)
DATABASE=FOLDERNAME+'\\database\\dbAPI.db'

def main(file_name):                                                                                    
    stock="voo" #Run this program for this stock                        
    l_stock_data = fetch_api(stock)                                         #use API to fetch data
    load_table(l_stock_data)                                                #save data to table
    generateImage(file_name)                                                #create a png plot for HTML page
    dict_data=read_table()                                                  #create dictionary data for HTML page              
    return(dict_data)

#1  API-1 to get company's stock performance
def fetch_api(stock):                                                      
    company_name=api_company_name(stock)                                    
    url='https://api.iextrading.com/1.0/stock/'+stock+'/chart/6m'       
    f = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    f1 = urllib.request.urlopen(f, timeout=5)
    apidata=f1.read()
    input_json = json.loads(apidata.decode("utf-8"))
    list_loader=[]
    for elements in input_json:
        list_loader.append((company_name,elements["date"],elements["open"],elements["high"],elements["low"],elements["close"],))
    return(list_loader)

#2  API-2 to get company's profile
def api_company_name(stock):
    url="https://api.iextrading.com/1.0/stock/"+stock+"/company"      
    f = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    f1 = urllib.request.urlopen(f, timeout=5)
    apidata=f1.read()
    input_json = json.loads(apidata.decode("utf-8"))
    name=input_json["companyName"]
    return(name)

#3 save data to a table
def load_table(input_list):
    con = sqlite3.connect(DATABASE)
    c = con.cursor()
    c.execute('DELETE FROM storeAPIData')                               #EMPTY older data 
    c.executemany('INSERT INTO storeAPIData VALUES (?,?,?,?,?,?)', input_list)    
    con.commit()
    con.close() 

#4 Generate a plot using pandas and matplotlib, save this plot to a png file
def generateImage(file_name):           
    temp_list=read_date_openprice()                                     # read data from table to create plot
    df=pd.DataFrame(temp_list)
    df[0]=pd.to_datetime(df[0])
    plt.plot(df[0],df[1])
    path=FOLDERNAME + "\\static\\"
    filelist = [ f for f in os.listdir(path) if f.endswith(".png") ]
    for f in filelist:                                                  # remove older png files
        os.remove(os.path.join(path, f))
    file=path+file_name
    plt.savefig(file)

#5 read data from table to generate the plot
def read_date_openprice():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT DateTime,OpenValue FROM storeAPIData")                               
    rows = cur.fetchall()
    con.close() 
    return(rows)

#6 read data from table and create a dictionary for HTML page
def read_table():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM storeAPIData")                           
    rows = cur.fetchall()
    con.close() 
    df=pd.DataFrame(rows)
    data={}
    data["company"]=list(df[0][:1])[0]
    data["Max_price"]=round(df[3].max(),2)
    data["Min_price"]=round(df[4].min(),2)
    data["Max_intraday"]=round(max(df[5]-df[2]),2)
    data["Min_intraday"]=round(min(df[5]-df[2]),2)
    return(data)



    
#=========================================================================================

@app.route("/")
@app.route("/home")
def hello():

    CurrTime=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    image_name="image_"+CurrTime+".png"
    dict_data_html=main(image_name)
    return render_template('home.html',posts=dict_data_html,image_name=image_name)

if __name__ == "__main__":
	app.run()
