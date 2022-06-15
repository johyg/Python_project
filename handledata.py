import sqlite3
import pandas as pd
pd.options.mode.chained_assignment = None  #Option to avoid redundant warning messages
import numpy as np

#Create class and methods

class HandleData:

    
    def __init__(self,path:str):
        self.data = pd.read_csv(path)
        #self.cur
        #self.remove_nan_df = None
        #self.db 

    def create_database(self):
        """Public method that creates a database
            
        Args: none
                
        Returns: returns a a database object and a cursor object
                
        """
        self.db = sqlite3.connect('vaccin_covid.db')
        self.cur = self.db.cursor()
        #print(self.cur.fetchall())       

    def seed_database(self):
        """Public method that fills database with csv data
        Args: None

        Returns: df(dataframe) a dataframe reading from sql
        """
        
        vaccination = self.data
        vaccination.to_sql("vaccination", self.db)       
        df = pd.read_sql("SELECT * FROM vaccination", self.db)       
        
        
        

    def normalize_data(self):
        """Public method that normalizes the data to fulfill the requirements of First normal form.
           Also replaces NaN values with 0, and deletes redundant columns. 
        Args: data(dataframe)

        Returns: data(dataframe) a normalized version of data
               
        """

        #extract all vaccines in different columns
        norm_df = self.data[["vaccines"]] #isolate column vaccines and split it
        norm_df[["v1","v2","v3","v4","v5","v6","v7"]] = norm_df["vaccines"].str.split(",", expand=True)        
        norm_df_drop = norm_df.drop(columns="vaccines") #delete column vaccines
        pd.set_option("display.max_columns", None)
        print(norm_df_drop.head())

        #Concatinate data and norm_df_drop
        self.data.reset_index(drop=True, inplace=True) #without this we get more NaN values in concat_df
        norm_df_drop.reset_index(drop=True, inplace=True) #without this we get more NaN values in concat_df
        concat_df = pd.concat([self.data,norm_df_drop],axis=1)          
        concat_df = concat_df.drop(columns="vaccines")   
        

        #Fill all NaN values with 0
        remove_nan_df = concat_df.fillna(0)              

        #copy the altered dataframe remove_nan_df to self.data
        self.data = remove_nan_df
        print(self.data.isna().sum())

        #Delete redundant columns from dataframe
        self.data = self.data.drop(columns=["daily_vaccinations_raw", "people_vaccinated_per_hundred",
         "people_fully_vaccinated_per_hundred","total_vaccinations_per_hundred"]) 
        print(self.data.isna().sum())
        self.data.info()
        



