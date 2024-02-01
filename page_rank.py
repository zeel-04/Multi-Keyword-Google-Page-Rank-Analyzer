import requests
from bs4 import BeautifulSoup
import time
import random
import streamlit as st
import pandas as pd
from utils import load_json
# from Home import KEYWORD_PROCESSED

# user agent's
UAS = ['Mozilla/5.0 (compatible; bingbot/2.0; +http', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http', 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv', 'insomnia/8.1.0']

def get_page_result(
        keyword: str, 
        selected_country_code: str, 
        total_results: int
        ) -> list:

    url = "https://www.google.com/search"

    querystring = {"num":f"{total_results}","q":f"{'+'.join(keyword.split())}","gl":f"{selected_country_code}" ,"oq":f"{'+'.join(keyword.split())}","sourceid":"chrome","ie":"UTF-8"}

    user_agent_index = random.randint(1, len(UAS))
    user_agent = UAS[user_agent_index-1]
    # user_agent = "Mozilla/5.0 (X11; Linux x86_64)"
    print("user agent", user_agent)
    headers = {
        "User-Agent": user_agent
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    soup = BeautifulSoup(response.text, "html.parser")

    # with open(f'page_source.html', "w") as f:
    #     f.write(soup.prettify())
    # print(soup)

    # all_divs = soup.findAll('div', class_="Gx5Zad fP1Qef xpd EtOod pkphOe")
    
    all_divs = soup.findAll('div', class_=load_json("./config/main_google_serp_class.json")["google_serp_class"])
    print("length all_divs : ", len(all_divs))
    links = []
 
    for div in all_divs:
        a_tag = div.find('a')
        a_tag = a_tag['href'].split("http")[1]
        #splitting if ? comes first in extracted URL
        if "%3F" in a_tag:
            a_tag = a_tag.split("%3F")[0]
        else:
            a_tag = a_tag.split("&")[0]

        a_tag = 'http' + a_tag
        links.append(a_tag)
    return links

def get_rank_for_multiple_keywords(
        keywords: list, 
        website_name_plus_domian: str, 
        selected_country_code: str, 
        total_results: int
        ) -> list:

    #Top Rankings
    top_rankings_data = {
        "Website name": [],
        "Keyword" :[],
        "Rank" : [],
        "Link" : []
    }

    #All Rankings
    all_rankings_data = {
        "Website name": [],
        "Keyword" :[],
        "Rank" : [],
        "Link" : []
    }

    total_keywords = len(keywords)

    rank_and_link_for_multiple_keywords = dict()

    for i, keyword in enumerate(keywords):
        
        rank_and_link_for_multiple_keywords[keyword] = []

        results_for_keyword = get_page_result(
            keyword=keyword, 
            selected_country_code=selected_country_code, 
            total_results=total_results
            )
        
        #Extracting given website ranking
        for idx, website_link in enumerate(results_for_keyword):
            if website_name_plus_domian in website_link:
                rank_and_link_for_multiple_keywords[keyword].append((idx+1, website_link))

        #Creating all ranking dataframe
        if rank_and_link_for_multiple_keywords[keyword]:
            for rank_link in rank_and_link_for_multiple_keywords[keyword]:
                all_rankings_data["Website name"].append(website_name_plus_domian)
                all_rankings_data["Keyword"].append(keyword)
                all_rankings_data["Rank"].append(rank_link[0])
                all_rankings_data["Link"].append(rank_link[1])
        else:
            all_rankings_data["Website name"].append(website_name_plus_domian)
            all_rankings_data["Keyword"].append(keyword)
            all_rankings_data["Rank"].append(None)
            all_rankings_data["Link"].append(None)

        #Creating top ranking dataframe
        if rank_and_link_for_multiple_keywords[keyword]:
            top_rankings_data["Website name"].append(website_name_plus_domian)
            top_rankings_data["Keyword"].append(keyword)
            top_rankings_data["Rank"].append(rank_and_link_for_multiple_keywords[keyword][0][0])
            top_rankings_data["Link"].append(rank_and_link_for_multiple_keywords[keyword][0][1])
        else:
            top_rankings_data["Website name"].append(website_name_plus_domian)
            top_rankings_data["Keyword"].append(keyword)
            top_rankings_data["Rank"].append(None)
            top_rankings_data["Link"].append(None)


        st.session_state.KEYWORD_PROCESSED_PROGRESS = int((i+1)/total_keywords) * 100
        st.write(f"**:green[{int(((i+1)/total_keywords) * 100)}%]** task completed.")

        #sleep for random time to stay undetected
        random_sleep_time_in_sec = random.randint(1, 5)
        time.sleep(random_sleep_time_in_sec)
    # st.write(rank_for_multiple_keywords)
    return [pd.DataFrame(top_rankings_data), pd.DataFrame(all_rankings_data)]
