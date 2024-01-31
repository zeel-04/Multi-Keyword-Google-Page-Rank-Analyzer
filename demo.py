import requests
from bs4 import BeautifulSoup
from page_rank import UAS
url = 'http://www.google.com/search?q=cars&num=0'

# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")

# # with open(f'page_source_{keyword}_{URLS[google_server]}.html', "w") as f:
# #     f.write(soup.prettify())

# all_divs = soup.findAll('div', class_="Gx5Zad fP1Qef xpd EtOod pkphOe")
# print(len(all_divs))
