import time
import json
import requests
import zipfile
import io
url = "https://fra1.qualtrics.com/API/v3/surveys"
survey_id = "SV_39on4Kq5knkl0Ng"

# payload = {
#     "format" : "ndjson",
#     "startDate" : "2022-09-01T01:00:00Z",
#     "endDate": "2023-09-30T01:00:00Z"
# }
payload = "{\n  \"format\": \"csv\",\n  \"compress\": \"false\",\n  \"startDate\":\"1970-01-01T01:00:00Z\",\n  \"endDate\":\"2023-01-25T07:30:04.885156Z\"\n}"
headers = {
    'Content-Type': "application/json",
    'X-API-TOKEN': "d1P1huFnluKXSKRlvGDuYMnRRLdWiEFknverRYP7"
    }

result = requests.post(url=f"{url}/{survey_id}/export-responses",data=payload, headers=headers)

data = result.json()
progressId = data['result']['progressId']
print(data)
print(f"progressId : {progressId}")

file_ready = False
fileId = None
while not file_ready:
    time.sleep(5)
    get_fileId = requests.get(url=f"{url}/{survey_id}/export-responses/{progressId}",headers=headers)
    resp = get_fileId.json()
    fileId = resp['result'].get("fileId")
    if fileId :
        print("File is ready to download")
        print(f"fileId : {fileId}")
        file_ready = True


# Download fileId
# download_file = requests.get(url=f"{url}/{survey_id}/export-responses/e5082c2f-66d2-449f-bef4-387685dbdc83-def/file",headers=headers)
# download_file = requests.get(url=f"{url}/{survey_id}/export-responses/21e96dbc-0f82-4232-988b-afae61b6273b-def/file",headers=headers)
download_file = requests.get(url=f"{url}/{survey_id}/export-responses/{fileId }/file",headers=headers)

# TODO : Try to retrieve this file : e5082c2f-66d2-449f-bef4-387685dbdc83-def (json format)
# 21e96dbc-0f82-4232-988b-afae61b6273b-def (ndjson format)
import os
filepath_tmp = f"aura_surveys_2022_2023_tmp.csv"

print(f"Uploading response to local csv file {filepath_tmp}")
with open(f"{filepath_tmp}", "w+") as f:
    f.write(download_file.text)
print(f"Local csv file {filepath_tmp} successfully created !")
csv_file = download_file.text
import pandas as pd
df = pd.read_csv(filepath_tmp)
df.drop(labels=[0, 1], inplace=True)
filepath = "aura_surveys_2022_2023_cleaned.csv"
df.to_csv(filepath, index=False)
# print(json_resp)
# print(download_file.text)

# # Writing to sample.json
# with open("aura_surveys_sample_v1.ndjson", "w") as outfile:
#     outfile.write(nd_json_resp)
#     print('aura surveys written into aura_surveys_sample.json file !')