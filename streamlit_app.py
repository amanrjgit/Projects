import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(page_title="Stock data",layout="wide")
input_data= st.text_input(label="Enter a stock",value="TSLA")
def update_value(input_data):
    try:
        # Interval required 1 minute
        tick = yf.Ticker(input_data)
        data = tick.history(period='1d', interval='1m')
        fcf=tick.info["freeCashflow"]
        d2e=tick.info["debtToEquity"]
        beta=tick.info["beta"]

        df = data[['Close']]

        sma = df.rolling(window=20).mean().dropna()
        rstd = df.rolling(window=20).std().dropna()

        upper_band = sma + 2 * rstd
        lower_band = sma - 2 * rstd

        upper_band = upper_band.rename(columns={'Close': 'upper'})
        lower_band = lower_band.rename(columns={'Close': 'lower'})
        bb = df.join(upper_band).join(lower_band)
        bb = bb.dropna()

        buyers = bb[bb['Close'] <= bb['lower']]
        sellers = bb[bb['Close'] >= bb['upper']]

        ####

        # declare figure
        fig = go.Figure()

        # Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'], name='market data'))

        fig.add_trace(go.Scatter(x=lower_band.index,
                                 y=lower_band['lower'],
                                 name='Lower Band',
                                 line_color='rgba(173,204,255,0.4)'
                                 ))

        fig.add_trace(go.Scatter(x=upper_band.index,
                                 y=upper_band['upper'],
                                 name='Upper Band',
                                 fill='tonexty',
                                 fillcolor='rgba(0, 75, 174, 0.35)',
                                 line_color='rgba(173,204,255,0.4)'
                                 ))
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['Close'],
                                 name='Close',
                                 line_color='#636EFA'
                                 ))
        fig.add_trace(go.Scatter(x=sma.index,
                                 y=sma['Close'],
                                 name='SMA',
                                 line_color='#FECB52'
                                 ))
        fig.add_trace(go.Scatter(x=buyers.index,
                                 y=buyers['Close'],
                                 name='Buyers',
                                 mode='markers',
                                 marker=dict(
                                     color='#00CC96',
                                     size=10,
                                 )
                                 ))
        fig.add_trace(go.Scatter(x=sellers.index,
                                 y=sellers['Close'],
                                 name='Sellers',
                                 mode='markers',
                                 marker=dict(
                                     color='#EF553B',
                                     size=10,
                                 )
                                 ))

        # Add titles
        fig.update_layout(
            title="Name : {}".format(tick.info["longName"]),
            yaxis_title="Stock Price ({} per Shares)".format(tick.info["financialCurrency"]),
            height=600,
            width=900,
            margin=dict(l=90, r=90, t=90, b=90, pad=3)
        )

        # X-Axes
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        return [fig,fcf,d2e,beta]
    except AttributeError:
        pass
    except KeyError:
        pass

output=update_value(input_data)

col1,col2=st.columns([4,1],gap="small")

with col1:
    st.plotly_chart(output[0], use_container_width=False)

with col2:
    st.metric(label="Free Cash Flow", value=output[1])

    st.metric(label="Debt to Equity", value=output[2])

    st.metric(label="Beta", value=output[3])
