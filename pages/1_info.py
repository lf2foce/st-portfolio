import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from prophet import Prophet

# # Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.experimental_connection('stocks_db', type='sql')

# conn

from src.get_data import get_historical_price

stocks = ['VCB', 'HPG', 'MWG', 'CTD','FRT', 'FPT', 'VIC']
selected_stock = st.selectbox('Pick stock for scanning', stocks)

data_load_state = st.text('Load data...')
data = get_historical_price(selected_stock)
data = data.droplevel('Symbols', axis=1)
data_load_state.text('Loading data...done!')

st.write(data.tail())

# def plot_raw_data():
#     fig=go.Figure()
#     fig.add_trace(go.Scatter(x=data.index, y=data.open, name='Open'))
#     fig.add_trace(go.Scatter(x=data.index, y=data.close, name='Close'))
#     fig.update_layout(title_text='Time series', xaxis)

# df = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
# df.columns = [col.replace("AAPL.", "") for col in df.columns]

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=list(data.index), y=list(data.close)))

# Set title
fig.update_layout(
    title_text="Time series with range slider and selectors"
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
st.plotly_chart(fig, use_container_width=True)

data_train = data[['close']].reset_index()
data_train.columns = ['ds', 'y']
st.dataframe(data_train)
m = Prophet()
m.fit(data_train)
future = m.make_future_dataframe(periods=30)
future.tail()
forecast = m.predict(future)