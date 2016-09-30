import requests
from bs4 import BeautifulSoup
import json
import re
import shutil

# Http proxy
proxies = {
    'http': 'http://127.0.0.1:8087',
    'https': 'http://127.0.0.1:8087',
}

# Youtube video home page
download_url = "https://www.youtube.com/playlist?list=PL0A0C8CFFE9712B76"
# Youtube home page
web_url = "https://www.youtube.com"

# Video Down
url_down = "http://www.clipconverter.cc/check.php"

response = requests.get(download_url, proxies=proxies, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all(id='pl-load-more-destination')

# Save file name
file_name_lists = list()
# Save urls
url_lists = list()
# Get video name and url
for row in table:
    for a_url in row.find_all(class_='pl-video-title-link'):
        file_name_lists.append(a_url.string)
        url_lists.append(a_url['href'])

count = 0
while True:
    if len(url_lists) <= count:
        break
    else:
        # Video down url
        print("Request ", file_name_lists[count], " Please wait...")
        try:
            response = requests.post(url_down, proxies=proxies, verify=False, data = {'mediaurl': web_url + url_lists[count]})
            playercode = json.loads(response.text)['url'][0]['url']
            playercode = re.search(r'(http.*)#type', playercode)
            playercode = playercode.group(1) + "&title=" + file_name_lists[count].strip(' ').strip('\n')

            res = requests.get(playercode, stream=True,  proxies=proxies, verify=False)
            print("Save ", file_name_lists[count], " Please wait...")
            full_file_name = file_name_lists[count].strip(' ').strip('\n') + '.mp4'
            f = open(full_file_name, 'wb')
            shutil.copyfileobj(res.raw, f)
            f.close()
            print(full_file_name, " ---- OK")
            count+=1
        except Exception:
            print("Get a error, Retrying...")
