import requests
import time

project_key = "udp"

payload = {
  "instructions": [
    {
      "kind": "updateMaintainerMember",
       "value": "5b99649e8d378b16a013e839"
      }
  ]
}

headers = {
  "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
  "Authorization": "api-791e23d8-7554-49bb-bccb-cda920330ffa"
}

fileread = open('udp-missing-maintainers.txt', 'r')

for flag_key in enumerate(fileread):
        feature_flag_key = flag_key[1].strip()
        url = "https://app.launchdarkly.com/api/v2/flags/" + project_key + "/" + feature_flag_key
        print(url)
        response = requests.patch(url, json=payload, headers=headers)
        time.sleep(3)
        data = response.json()
