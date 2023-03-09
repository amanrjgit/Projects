import numpy as np
import pandas as pd
import streamlit as st
import base64
import plotly.graph_objects as go
from instagrapi import Client

#client = Client()
#client.login("test_ing4747", "testing123")

def details(username):
    #dict(client.user_info_by_username(username))
    pass


st.set_page_config(page_title="InstaBot Identifier- Aman Kumar Jaiswar",layout="wide")

# image

main_bg = "bg.jpg"
main_bg_ext = "jpg"

with open(main_bg, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
st.markdown(
    f"""
<style>
.stApp {{
    background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
    background-size: cover
}}
</style>
""",
    unsafe_allow_html=True
)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 60,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Fakeness", 'font': {'size': 50}},
    delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 250], 'color': 'cyan'},
            {'range': [250, 400], 'color': 'royalblue'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 490}}))

fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})



col1, col2 = st.columns([1,1],gap="small")
with col1:
    st.image("insta.png")
    st.markdown(hide_img_fs, unsafe_allow_html=True)

with col2:
    st.title("InstaBot Identifier")
    input_data = st.text_input(label="Search for a username")
    st.plotly_chart(fig)
