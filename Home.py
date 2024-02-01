import streamlit as st 
import datetime
from page_rank import get_rank_for_multiple_keywords
from utils import load_json

date = datetime.date.today()

st.title("Find your page rank")
st.write(date)
# st.write("Reference taken from https://developers.google.com/custom-search/docs/xml_results")

#Inputs
with st.container(border=True):
    st.subheader(":gray[Inputs]")
    file = st.file_uploader("Upload your **:blue[Excel file]** containing keywords :gray[(This feature is under development)]")
    st.subheader("OR")
    keywords = st.text_area("Copy your keywords from **:blue[Excel]**", 
                            value="wiki")
#Website and total results configuration
with st.container(border=True):
    st.subheader(":gray[Website and total results configuration]")
    website_name_plus_domian = st.text_input("Enter your **:blue[website name with assoiciated domain.]**", value="wikipedia.org")

    total_results = st.slider(
        'How many **:blue[total results]** you want to fetch ?',
        min_value=0, 
        max_value=100, 
        value=10, 
        step=5
        )

#server location configuration    
location_file_path = './customizations/locations.json'
loaded_location_data = load_json(location_file_path)
# st.write(len(loaded_location_data))
# st.write(loaded_location_data[0])

with st.container(border=True):

    st.subheader(":gray[Server location configuration]")

    selected_country = st.selectbox(
        "Select your desired **:blue[location server]**", 
        options=[country["country_name"] for country in loaded_location_data],
        index=98
        )

    # Get the corresponding country code
    selected_country_code = next(
        (country["country_code"] for country in loaded_location_data if country["country_name"] == selected_country), 
        None
        )

    # st.write(selected_country_code)

submit = st.button("Find it")

if submit:
    
    with st.spinner(f"Please wait for few minutes..."):

        results = get_rank_for_multiple_keywords(
            keywords=keywords.split('\n'), 
            website_name_plus_domian=website_name_plus_domian.strip(), 
            selected_country_code=selected_country_code, 
            total_results=total_results
            )
        
        top_rankings, all_rankings = st.tabs(tabs=["Top Rankings","All Rankings"])

        with top_rankings:
            st.dataframe(results[0])
        with all_rankings:
            st.dataframe(results[1])

