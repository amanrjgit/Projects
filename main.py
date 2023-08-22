import streamlit as st
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="SSC CGL/CHSL Marks Calculator - Aman Kumar Jaiswar",layout="wide")
st.title("SSC tier 1 Marks calculator")

def calculate_marks(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    question_panels = soup.find_all(class_='question-pnl')

    not_attempted = 0

    s1_right = 0
    s2_right = 0
    s3_right = 0
    s4_right = 0

    s1_wrong = 0
    s2_wrong = 0
    s3_wrong = 0
    s4_wrong = 0

    sec = soup.find_all(class_='section-lbl')
    sections = []

    for j in range(len(sec)):
        sub = sec[j].find_all(class_='bold')
        sections.append(sub[0].get_text())

    for i in range(1,min(100, len(question_panels)+1)):
        bold_elements = question_panels[i].find_all(class_='bold')
        right_ans = question_panels[i].find(class_='rightAns')

        if i<26:
            if right_ans.get_text()[0] == bold_elements[5].get_text():
                s1_right += 1
            elif bold_elements[5].get_text() == ' -- ':
                not_attempted += 1
            else:
                s1_wrong += 1
            i += 1
        elif (i>25 and i<51):
            if right_ans.get_text()[0] == bold_elements[5].get_text():
                s2_right += 1
            elif bold_elements[5].get_text() == ' -- ':
                not_attempted += 1
            else:
                s2_wrong += 1
            i += 1
        elif (i>50 and i<76):
            if right_ans.get_text()[0] == bold_elements[5].get_text():
                s3_right += 1
            elif bold_elements[5].get_text() == ' -- ':
                not_attempted += 1
            else:
                s3_wrong += 1
            i += 1
        elif (i>75 and i<101):
            if right_ans.get_text()[0] == bold_elements[5].get_text():
                s4_right += 1
            elif bold_elements[5].get_text() == ' -- ':
                not_attempted += 1
            else:
                s4_wrong += 1
            i += 1
        else:
            pass

    right = s1_right+s2_right+s3_right+s4_right
    wrong = 100 - not_attempted - right
    marks = right * 2 - wrong * 0.5
    return sections,s1_right,s2_right,s3_right,s4_right,s1_wrong,s2_wrong,s3_wrong,s4_wrong,not_attempted

answer_key_url = st.text_input("Enter Answer Key URL:")
st.button("Calculate Marks")
col1,col2,col3,col4 = st.columns([1,1,1,1])

if answer_key_url:
    try:
        sections,s1_right,s2_right,s3_right,s4_right,s1_wrong,s2_wrong,s3_wrong,s4_wrong,not_attempted = calculate_marks(answer_key_url)
    except:
        st.warning("Please enter a valid Answer Key URL.")

    with col1:
        st.subheader("Correct Questions")
        st.metric(label=sections[0], value=s1_right)
        st.metric(label=sections[1], value=s2_right)
        st.metric(label=sections[2], value=s3_right)
        st.metric(label=sections[3], value=s4_right)
    with col2:
        st.subheader("Incorrect Questions")
        st.metric(label=sections[0], value=s1_wrong)
        st.metric(label=sections[1], value=s2_wrong)
        st.metric(label=sections[2], value=s3_wrong)
        st.metric(label=sections[3], value=s4_wrong)
    with col3:
        st.subheader("Sectional Marks")
        st.metric(label=sections[0], value=(2*s1_right-0.5*s1_wrong))
        st.metric(label=sections[1], value=(2*s2_right-0.5*s2_wrong))
        st.metric(label=sections[2], value=(2*s3_right-0.5*s3_wrong))
        st.metric(label=sections[3], value=(2*s4_right-0.5*s4_wrong))
    with col4:
        st.subheader("Total")
        right = s1_right + s2_right + s3_right + s4_right
        wrong = 100 - not_attempted - right
        marks = right * 2 - wrong * 0.5
        st.metric(label="Total Attempted", value=(100-not_attempted))
        st.metric(label="Total Correct", value=right)
        st.metric(label="Total Incorrect", value=wrong)
        st.metric(label="Total Marks", value=marks)
else:
    st.warning("Please enter a valid Answer Key URL.")