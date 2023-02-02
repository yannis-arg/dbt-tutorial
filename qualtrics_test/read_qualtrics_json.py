import json

# Opening JSON file
with open('aura_surveys_sample.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
print(json_object)
# for key,resp_list in json_object.items():
#     for resp in resp_list :
#         print(f"{resp['responseId']} : {resp['values']}")