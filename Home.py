import streamlit as st 
import datetime
from page_rank import get_rank_for_multiple_keywords, URLS

date = datetime.date.today()

#Global Variables
# COOKIE = f"1P_JAR={date}-05; AEC=Ae3NU9Pn9ypz-ZHWsvlIUNVVH5BbyJkBlFx39j-kvzDp5h46ppLkurtmBA; NID=511%3DUbkUFrHoi4apDPF6kg08zYfSt0BdPS6pHXm5yf6QcPPrwqV9cBtbzDRPnk9PjzfRx5tYSNt021_UNOPeRnCgL-xhufU-6Tq2-EzhrCSEDwpGQfPka4GWO10HR-3ksgheonp3UsmjjMV8HsXRZXKQwQBg_kX-HfsUIisfYqhjer0"

st.title("Find your page rank")
st.write(date)
st.write("Reference taken from https://developers.google.com/custom-search/docs/xml_results")

with st.container(border=True):
    st.subheader(":gray[Inputs]")
    file = st.file_uploader("Upload your **:red[Excel file]** containing keywords :gray[(This feature is under development)]")
    st.subheader("OR")
    keywords = st.text_area("Copy your keywords from **:red[Excel]**", 
                            value=" ")

with st.container(border=True):
    st.subheader(":gray[Website and total results configuration]")
    cols = st.columns(2)
    with cols[0]:
        website_name = st.text_input("Enter your **:red[website name]**", value=" ")
    with cols[1]:
        domain = st.text_input("Enter your **:red[website domain]**", value=" ")

    total_results = st.slider('How many :red[totatotal resultsl results] you want to fetch ?',min_value=0, max_value=100, value=10, step=5)

with st.container(border=True):
    st.subheader(":gray[Google server configuration]")
    google_server = st.selectbox("Select your desired **:red[google server]**", options=list(URLS.keys()))

# with st.container(border=True):
#     st.subheader(":gray[Cookies]")
#     cookie = st.text_area("Enter your new **:red[Cookie]** if the current one does not work",value=COOKIE, height=150)

submit = st.button("Find it")

if submit:
    
    with st.spinner(f"Please wait for few minutes..."):
        results = get_rank_for_multiple_keywords(keywords=keywords.split('\n'), website_name=website_name, domain=domain, google_server=google_server, total_results=total_results)
        total_keywords = len(keywords)
        st.dataframe(results)

