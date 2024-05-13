import requests
url = 'http://153.33.147.226:8888'
a = requests.get(url).content
print(a)