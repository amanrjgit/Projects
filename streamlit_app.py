
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from requests_html import HTMLSession
def news_url(url):
    session = HTMLSession()
    web_page = url
    respone = session.get(web_page)
    page_html = respone.html
    video_frame= page_html.find('a.link.caas-button')
    video_attrs = video_frame[-1].attrs
    return video_attrs["href"]

st.set_page_config(page_title="Stock Moniter- Aman Kumar Jaiswar",layout="wide")
input_data= st.text_input(label="Enter a stock symbol",value="TSLA")
def update_value(input_data):
    try:
        # Interval required 1 minute
        tick = yf.Ticker(input_data)
        data = tick.history(period='1d', interval='1m')

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

        return fig
    except AttributeError:
        pass
    except KeyError:
        pass


def year_graph(input_data):
    try:
        # Interval required 1 minute
        tick = yf.Ticker(input_data)
        data = tick.history(period='5y', interval='1d')
        fcf=tick.info.get("freeCashflow")
        d2e=tick.info.get("debtToEquity")
        beta=tick.info.get("beta")
        news = tick.news
        pout=tick.info.get("payoutRatio")
        tpe=tick.info.get("trailingPE")
        p2b=tick.info.get("priceToBook")
        logo=tick.info.get("logo_url")

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
                    dict(count=1, label="1 year", step="year", stepmode="backward"),
                    dict(count=3, label="3 year", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        return [fig,fcf,d2e,beta,pout,tpe,p2b,logo,news]
    except AttributeError:
        pass
    except KeyError:
        pass


hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

output=update_value(input_data)

yearly=year_graph(input_data)

tab1,tab2,tab3 = st.tabs(["Recent","5 years","News"])

if output==None:
    with tab1:
        st.warning("No Data Found \n Please Check The Symbol")
    with tab2:
        st.warning("No Data Found \n Please Check The Symbol")
    with tab3:
        st.warning("No Data Found \n Please Check The Symbol")

else:
    tab1.subheader("Minutely graph for 1 day")
    with tab1:
        try:
            st.image(yearly[7],width=50)
            st.markdown(hide_img_fs, unsafe_allow_html=True)
        except:
            pass
        col1,col2=st.columns([4,1],gap="small")

        with col1:
            st.plotly_chart(output, use_container_width=False,config={"displayModeBar":False})


        with col2:
            st.metric(label="Free Cash Flow", value=yearly[1])

            st.metric(label="Debt to Equity", value=yearly[2])

            st.metric(label="Beta", value=yearly[3])

            st.metric(label="Payout Ratio",value=yearly[4])

            st.metric(label="Trailing PE", value=yearly[5])

            st.metric(label="Price to Book ratio", value=yearly[6])

    tab2.subheader("Dayly graph for 5 years")
    with tab2:
        try:
            st.image(yearly[7],width=50)
            st.markdown(hide_img_fs, unsafe_allow_html=True)
        except:
            pass
        col1,col2=st.columns([4,1],gap="small")

        with col1:
            st.plotly_chart(yearly[0], use_container_width=False,config={"displayModeBar":False})

        with col2:
            st.write(" ")

            st.metric(label="Free Cash Flow", value=yearly[1])

            st.metric(label="Debt to Equity", value=yearly[2])

            st.metric(label="Beta", value=yearly[3])

            st.metric(label="Payout Ratio",value=yearly[4])

            st.metric(label="Trailing PE", value=yearly[5])

            st.metric(label="Price to Book ratio", value=yearly[6])

    with tab3:
        all_news=yearly[8]

        for i in range(len(all_news)):
            ncol1,ncol2= st.columns([1,5])
            with ncol1:
                try:
                    st.image(all_news[i]["thumbnail"]["resolutions"][1]["url"])

                    st.markdown(hide_img_fs, unsafe_allow_html=True)
                except KeyError:
                    continue
            with ncol2:
                latest_news=news_url(all_news[i]["link"])
                st.header(all_news[i]["title"])
                if latest_news.startswith("mailto"):
                    st.subheader("click here to [read more]({})".format(all_news[i]["link"]))
                else:
                    st.subheader("click here to [read more]({})".format(latest_news))
