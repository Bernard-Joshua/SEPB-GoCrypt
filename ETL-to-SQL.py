#!/usr/bin/env python
# coding: utf-8

# In[123]:


#importing essential libraries for pyspark and sql
import findspark
findspark.init()


# In[124]:


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import Row
import mysql.connector
import pandas as pd

#create spark session
spark = SparkSession.builder.config("spark.jars", "/home/hduser/mysql-connector-java-5.1.47/mysql-connector-java-5.1.47.jar")     .master("local").appName("ETL to SQL").getOrCreate()
spark


# In[125]:


#connecting to localhost sql database
 
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database ='etl'
)
 
# Creating an instance of 'cursor' class
# which is used to execute the 'SQL'
# statements in 'Python'
cursor = mydb.cursor()
 
# Show database tables
cursor.execute("SHOW TABLES")
 
for x in cursor:
  print(x)

#cursor.execute("INSERT INTO crypto (Name,Symbol,Date,High,Low,Open,Close,Volume,Marketcap) values('test',0,0,0,0,0,0,0,0)")
#mydb.commit()


# In[126]:


#define function for etl processing of dataframe
def etl_data(df):
    df=df.drop("SNo")
    df_date = df.withColumn('Date',to_date(df.Date))
    df=df_date
    df=df.withColumn("High",round("High",3))
    df=df.withColumn("Low",round("Low",3))
    df=df.withColumn("Open",round("Open",3))
    df=df.withColumn("Close",round("Close",3))
    return(df)
    #df.select('Name','Symbol','Date','High','Low','Open','Close','Volume','Marketcap').write.format("jdbc").option("url", "jdbc:mysql://127.0.0.1:3306/dezyre_db&useUnicode=true&characterEncoding=UTF-8&useSSL=false") \
	#.option("driver", "com.mysql.jdbc.Driver").option("dbtable", "students") \
	#.option("user", "root").option("password", "root").save(
    #print("Successfully cleaned and added data to sql table")
    
#define function for upload to sql table    
def sql_upload(df):
    pd_dataframe=df.toPandas()
    for index, row in pd_dataframe.iterrows():
        cursor.execute("INSERT INTO crypto (Name,Symbol,Date,High,Low,Open,Close,Volume,Marketcap) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(row['Name'],row['Symbol'],row['Date'],row['High'],row['Low'],row['Open'],row['Close'],row['Volume'],row['Marketcap']))
        mydb.commit()
    print("Successfully uploaded to sql table")


# In[129]:


#check if etl worked
doge_df = spark.read.csv('csv\\coin_Dogecoin.csv', header=True, sep=",").cache()
etl_doge=etl_data(doge_df)
etl_doge.show()


# In[133]:


sql_upload(etl_doge)


# In[84]:


btc_df = spark.read.csv('csv\\coin_Bitcoin.csv', header=True, sep=",").cache()
etl_btc=etl_data(btc_df)
sql_upload(etl_btc)

aave_df = spark.read.csv('csv\\coin_Aave.csv', header=True, sep=",").cache()
etl_aave=etl_data(aave_df)
sql_upload(etl_aave)

binance_df = spark.read.csv('csv\\coin_BinanceCoin.csv', header=True, sep=",").cache()
etl_binance=etl_data(binance_df)
sql_upload(etl_binance)

cardano_df = spark.read.csv('csv\\coin_Cardano.csv', header=True, sep=",").cache()
etl_cardano=etl_data(cardano_df)
sql_upload(etl_cardano)

usdt_df = spark.read.csv('csv\\coin_Tether.csv', header=True, sep=",").cache()
etl_usdt=etl_data(usdt_df)
sql_upload(etl_usdt)

ethereum_df = spark.read.csv('csv\\coin_Ethereum.csv', header=True, sep=",").cache()
etl_ethereum=etl_data(ethereum_df)
sql_upload(etl_ethereum)

solana_df = spark.read.csv('csv\\coin_Solana.csv', header=True, sep=",").cache()
etl_solana=etl_data(solana_df)
sql_upload(etl_solana)

lite_df = spark.read.csv('csv\\coin_Litecoin.csv', header=True, sep=",").cache()
etl_lite=etl_data(lite_df)
sql_upload(etl_lite)

stellar_df = spark.read.csv('csv\\coin_Stellar.csv', header=True, sep=",").cache()
etl_stellar=etl_data(stellar_df)
sql_upload(etl_stellar)

usd_df = spark.read.csv('csv\\coin_USDCoin.csv', header=True, sep=",").cache()
etl_usd=etl_data(usd_df)
sql_upload(etl_usd)


# In[ ]:




