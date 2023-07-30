import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.get_data import stock_wide_format
from src.greeting import get_local_IP_address
from my_chart.heatmap import stock_heatmap

st.set_page_config(
        page_title="Fidelity Account View by Gerard Bentley",
        page_icon="📊",
        initial_sidebar_state="expanded",
        layout="wide",
    )

stock_list = ['VCB', 'HPG', 'VIC', 'FPT', 'FRT']
print(stock_list)

stocks_df_pivot = stock_wide_format(stock_list)
# print(stocks_df_pivot.head())
df_month_resample = stocks_df_pivot.resample('M').last()
df_month_resample = df_month_resample.reset_index().melt('date', var_name='Ticker', value_name='Adj_Close')
df_month_resample.columns = ['Date', 'Ticker', 'Adj_Close']
df_month_resample['pct'] = df_month_resample.sort_values('Date').groupby(['Ticker'])['Adj_Close'].pct_change()
print(df_month_resample.head())

df_month_resample = df_month_resample.dropna()

fig1 = px.bar(df_month_resample, x='Date', y='pct', text=[f'{i:.1%}' for i in df_month_resample['pct']],
    color='Ticker', barmode='group',
    title="Monthly returns",
    labels={"pct": "return", "Date": "End of Month"}
    ) #, orientation='h'

fig1.update_traces(textfont_size=16, textangle=0)#, marker_color=colors
# fig1.update_layout(template="plotly_white")

st.plotly_chart(fig1, use_container_width=True)

stocks_df_pivot = stocks_df_pivot.fillna(method='bfill')
stocks_df_normalize = stocks_df_pivot/stocks_df_pivot.iloc[0,:] # normalize

fig2 = px.line(stocks_df_normalize, x=stocks_df_normalize.index, y=stocks_df_normalize.columns)
st.plotly_chart(fig2, use_container_width=True)


fig3 = stock_heatmap(stocks_df_pivot)
st.plotly_chart(fig3, use_container_width=True)



df_long_pct = stocks_df_pivot.resample('W-MON').last().pct_change()
df_long_pct = df_long_pct.reset_index().melt('date', var_name='Ticker', value_name='weekly_return')

fig4 = px.violin(df_long_pct,y='Ticker',x='weekly_return', color='Ticker', orientation='h')\
    .update_traces(side='positive', width=2, meanline_visible=True, points = False)
fig4.update_layout(xaxis_zeroline=False)
st.plotly_chart(fig4, use_container_width=True)

