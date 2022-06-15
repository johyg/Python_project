import handledata as hd
#import sqlite3
import pandas as pd
#import numpy as np

def main():        
    
    #data = pd.read_csv("vaccin_covid.csv")
    
    #Create HandleData object 
    data_handle = hd.HandleData("vaccin_covid.csv")

    #normalize data
    data_handle.normalize_data()
    
    #create database
    data_handle.create_database()

    #seed database
    data_handle.seed_database()

if __name__ == "__main__":
    main()