
##https://developers.facebook.com/tools/explorer/
ACCESS_TOKEN='EAACEdEose0cBAFSmtXjZBwD5weAUCywSOI1jopR03G2685GtQNOGXZBwdyBMnZCpLeqwlqF5Kp5IXZCbFYNtt4Dmzq2B8eTX9ezfVYNbwwzZAwrodX0ZBoai622J7zdaTy8vLRct3kMjyZB0YrgwNoygmS1Bca4PpkCJ8rmS5LkRbmXzzfThCWwovzN5y2rBakZD'

import requests

import json


base_url='https://graph.facebook.com/me'

fields='id,name,likes'

url='{0}?fields={1}&access_token={2}'.format(base_url,fields,ACCESS_TOKEN)

#print(url)


content=requests.get(url).json()
#print(json.dumps(content,indent=1))

#pip install facebook-sdk
import facebook
g=facebook.GraphAPI(ACCESS_TOKEN,version='2.7')
print(g.get_object(id='1577673735847735'))
