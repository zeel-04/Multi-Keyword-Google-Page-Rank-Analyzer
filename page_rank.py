import requests
from bs4 import BeautifulSoup
import time
import random
import streamlit as st
import pandas as pd
# from Home import KEYWORD_PROCESSED

URLS = {
    ".com" : "https://www.google.com/search",
    ".com.au" : "https://www.google.com.au/search",
    ".co.in" : "https://www.google.co.in/search",
    ".ca" : "https://www.google.ca/search",
}

# user agent's
UAS = ['Mozilla/5.0 (compatible; bingbot/2.0; +http', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http', 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv', 'insomnia/8.1.0']

def get_page_result(keyword: str, google_server: str, total_results: int) -> list:

    url = URLS[google_server]

    querystring = {"num":f"{total_results}","q":f"{'+'.join(keyword.split())}","oq":f"{'+'.join(keyword.split())}","sourceid":"chrome","ie":"UTF-8"}

    user_agent_index = random.randint(1, len(UAS))
    user_agent = UAS[user_agent_index-1]
    # user_agent = "Mozilla/5.0 (X11; Linux x86_64)"
    print("user agent", user_agent)
    headers = {
        "User-Agent": user_agent
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    soup = BeautifulSoup(response.text, "html.parser")

    # with open(f'page_source_{keyword}_{URLS[google_server]}.html', "w") as f:
    #     f.write(soup.prettify())

    all_divs = soup.findAll('div', class_="Gx5Zad fP1Qef xpd EtOod pkphOe")
    print("length all_divs : ", len(all_divs))
    links = []

    for div in all_divs:
        a_tag = div.find('a')
        links.append(a_tag['href'][7:])

    return links

def get_rank_for_multiple_keywords(keywords: list, website_name: str, domain: str, google_server: str, total_results: int) -> pd.DataFrame:

    full_website_name = website_name+domain
    data = {
        "Website name": [],
        "Keyword" :[],
        "Top Rank" : [],
        "All Ranks" : []
    }

    total_keywords = len(keywords)

    rank_for_multiple_keywords = dict()

    for i, keyword in enumerate(keywords):

        rank_for_multiple_keywords[keyword] = []
        results_for_keyword = get_page_result(keyword=keyword, google_server=google_server, total_results=total_results)

        for idx, website_link in enumerate(results_for_keyword):

            if website_name+domain in website_link:
                rank_for_multiple_keywords[keyword].append(idx+1)

        # KEYWORD_PROCESSED += 1
        data["Website name"].append(full_website_name)
        data["Keyword"].append(keyword)
        if rank_for_multiple_keywords[keyword]:
            data["Top Rank"].append(min(rank_for_multiple_keywords[keyword]))
            data["All Ranks"].append(rank_for_multiple_keywords[keyword])
        else:
            data["Top Rank"].append(None)
            data["All Ranks"].append(None)

        st.session_state.KEYWORD_PROCESSED_PROGRESS = int((i+1)/total_keywords) * 100
        st.write(f"**:green[{int(((i+1)/total_keywords) * 100)}%]** task completed.")

        random_sleep_time_in_sec = random.randint(1, 5)
        time.sleep(random_sleep_time_in_sec)

    return pd.DataFrame(data)
