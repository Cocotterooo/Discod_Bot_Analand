import requests
import json

ApiKey = "whac_cLkztFqZsEzWxJAQmVUfKCsMrtrJ30TkYrXyjHhB8Oh"
response = requests.get("https://panel.whost.sh/api/client/servers/55190693", headers={
    'Accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': ApiKey
}).json()

print(json.dumps(response, indent=1))
