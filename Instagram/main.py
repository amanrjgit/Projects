import numpy as np
import pandas as pd
import streamlit as st
import base64

main_bg = "instagram/instagram-bg2.avif"
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


st.title("InstaBot Identifier")

col1, col2 = st.columns([1,1],gap="small")
with col2:
    input_data = st.text_input(label="Enter Username")
