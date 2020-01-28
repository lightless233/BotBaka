import json
import re

import requests
from bs4 import BeautifulSoup

url = "https://3g.dxy.cn/newh5/view/pneumonia"
response = requests.get(url, timeout=12)
soup = BeautifulSoup(response.content)
text = soup.find(id="getAreaStat").text

print(text)
pattern = r"window\.getAreaStat = (.+)}catch\(e\){}"

result = re.search(pattern, text)
print(result.group(1))

# j = re.search(pattern, text).group(0)[0]
# results = json.loads(j)
