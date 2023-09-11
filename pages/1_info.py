import streamlit as st

import plotly.graph_objects as go
import pandas as pd
import openai
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from src.get_data import get_historical_price
from src.theme import *
# # Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.experimental_connection('stocks_db', type='sql')
# conn


# openai.api_key  = os.environ['OPENAI_API_KEY']

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

predict_tab, gpt_tab = st.tabs(['Predict', 'ChatGPT'])
with predict_tab:

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
    st.write(forecast.tail())

    fig1 = plot_plotly(m, forecast)

    st.plotly_chart(fig1, use_container_width=True)


    fig2 = plot_components_plotly(m, forecast)

    st.plotly_chart(fig2, use_container_width=True)

with gpt_tab:
    openai.api_key  = st.secrets["OPENAI_API_KEY"]
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    with st.spinner('Wait for it...'):
        response1 = get_completion(f'Top lý do để mua cổ phiếu {selected_stock}')
        response2 = get_completion(f'Phân tích SWOT cổ phiếu {selected_stock}')
    
        st.subheader(f'Lý do để mua cổ phiếu {selected_stock}:')
        st.write(response1)
        st.subheader(f'Phân tích SWOT cổ phiếu {selected_stock}:')
        st.write(response2)