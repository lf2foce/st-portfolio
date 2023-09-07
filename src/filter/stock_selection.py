import streamlit as st
from src.get_data import stock_wide_format
import pandas as pd

def my_portfolio():
    stock_list = st.sidebar.multiselect('pick stock', ['VCB', 'HPG', 'CTD', 'VIC', 'SAB'],
        default=['VCB', 'HPG', 'VIC', 'SAB'] )

    conn = st.experimental_connection('stocks_db', type='sql')
    stocks_df_pivot = conn.query('''select * from stock_price_pivot''')
    stocks_df_pivot['date'] = pd.to_datetime(stocks_df_pivot['date'], format='%Y-%m-%d')
    stocks_df_pivot.set_index('date', inplace=True)
    return stocks_df_pivot[stock_list]
    # return stock_wide_format(stock_list) 