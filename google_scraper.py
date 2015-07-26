import requests
from bs4 import BeautifulSoup

url = 'http://google.com'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "html.parser")
logo = soup.find(id='hplogo')
print(logo.prettify().encode('utf-8'))
# print(html)

