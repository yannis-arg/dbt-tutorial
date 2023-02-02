import json

# aura_survey_row = {"responseId":"R_2eUs33vUUZNFhXe","values":{"startDate":"2022-12-25T11:19:55Z","endDate":"2022-12-25T11:21:52Z","status":0,"ipAddress":"37.211.251.10","progress":33,"duration":117,"finished":0,"recordedDate":"2023-01-01T11:21:57.581Z","_recordId":"R_2eUs33vUUZNFhXe","distributionChannel":"anonymous","userLanguage":"EN","QID14_TEXT":"asghar.alibaba61@gmail.com","QID15_TEXT":"Asghar Baba","QID16_TEXT":"0097339626298","QID17":1,"QID18":3,"QID19":3,"QID1_NPS_GROUP":2,"QID1":7,"QID2":3,"QID3":2,"outlet":"Divan","Source_DERIVED95guxfc":"","outlet_DERIVED9wlnmjt":"Divan","outlet_DERIVEDaswe9ql":"Hospitality","outlet_DERIVEDpndiqvu":"Lusail Boulevard"},"labels":{"status":"IP Address","finished":"False","QID17":"Male","QID18":"35 +","QID19":"TOURIST","QID1_NPS_GROUP":"Passive","QID2":"Sometimes","QID3":"Satisfied"},"displayedFields":["QID1","QID16_TEXT","QID14_TEXT","QID3","QID2","QID19","QID18","QID17","QID15_TEXT","QID1_NPS_GROUP"],"displayedValues":{"QID1":[0,1,2,3,4,5,6,7,8,9,10],"QID3":[1,2,3,4,5],"QID2":[1,2,3,4,5],"QID19":[1,2,3],"QID18":[1,2,3],"QID17":[1,2],"QID1_NPS_GROUP":[1,1,1,1,1,1,1,2,2,3,3]}}
#
#
# def get_keys(obj, stack):
#     for k, v in obj.items():
#         k2 = ([k] if k else []) + stack  # don't return empty keys
#         if v and isinstance(v, dict):
#             for c in get_keys(v, k2):
#                 yield c
#         elif v and isinstance(v, list):
#             for c in get_keys(v, k2):
#                 yield c
#         else:  # leaf
#             yield k2
#
# with open("aura_surveys_schema_v2.json","r") as schema_file :
#     schema_json = json.load(schema_file)
#     schema_keys = list(get_keys(schema_json,[]))
#     print(f"Schema keys : \n {schema_keys}")
#     row_keys = list(get_keys(aura_survey_row,[]))
#     print(f"Row keys : \n {row_keys}")

# dict_test = {"name":"yannis","firstname":None}
# new_dict = {}
#
# for k,v in dict_test.items():
#     new_dict[k] = v
# print(new_dict)

id = "15943713913455766200000000000000"
id_2 = "58969568523772956650000000000000"
print(len(id))
print(len(id_2))