import streamlit as st
import pandas as pd

import os

def clean_df1(df1):
    df1 = df1[['Day', 'DTE', 'Expiry Date', 'Profit', 'India VIX']]
    return df1

def main():
    st.title("Data Cleaning App")
    st.set_page_config(page_title='BackTest PnL', layout='wide')
    file = st.file_uploader("Upload your Excel or CSV file", type=['xlsx', 'csv'])
    if file is not None:
        if '.csv' in file.name:
            df1 = pd.read_csv(file, skiprows=1, index_col=1)
        else:
            df1 = pd.read_excel(file, sheet_name='Result_1', skiprows=1, index_col=1)
        
        st.write(df1.columns)  # print column names
        
        df1 = clean_df1(df1)
        st.dataframe(df1.head())
        
        df1.index = pd.to_datetime(df1.index, format='mixed').strftime('%d-%m-%Y')
        st.dataframe(df1.index)
        
        # Specify the directory where you want to save the file
        output_dir = 'PNL_BACKTEST'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'df1.csv')
        
        df1.to_csv(output_file)
        st.success(f"Data cleaned and saved to {output_file}")

if __name__ == "__main__":
    main()