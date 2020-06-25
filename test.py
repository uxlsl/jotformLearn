import requests

formID = '201761789450158'
apiKey = '4424e671aec8c87a27f6b761cd3d01fa'


# 查看https://api.jotform.com/docs/#form-id-submissions
r = requests.get(f'https://api.jotform.com/form/{formID}/submissions?apiKey={apiKey}')
print(r.json())

