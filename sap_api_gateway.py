import requests
import json
from google.cloud import secretmanager

# headers = {
#     "Authorization": "Basic QzRDREFUQVJFQURFUjpQaWhAMTIzNCM=",
#     # TODO : Base64encode "username:password" then use it as "Basic [encoding_result]"
#     "X-CSRF-Token": "fetch",
#     # "Accept" : "*/*",
#     # "Accept-Encoding":"gzip, deflat, br",
#     # "Connection" : "keep-alive",
#     # "User-Agent" : "PostmanRuntime/7.30.0",
#     # "Host" : "my346965.crm.ondemand.com"
# }
#
# s = requests.Session()
# # s.headers['User-Agent'] = 'PostmanRuntime/7.30.0'
#
# login_res = s.get("https://my346965.crm.ondemand.com/sap/c4c/odata/v1/c4codataapi/",headers=headers)
# # print(login_res.cookies['csfrtoken'])
# print(login_res.status_code)
# print(login_res.headers)
# print(login_res.headers['x-csrf-token'])
#
# # # TODO : Prepare headers for post request
# headers["x-csrf-token"] = login_res.headers['x-csrf-token']
# headers["Content-Type"] = "application/json"
# #
# data = {
#     "CustomerABCClassificationCode": "B",
#     "Phone": "+1 1234-5678-9101",
#     "Email": "arg.yanv4@mail.con",
#     "CountryCode": "BE",
#     "HouseNumber": "",
#     "Street": "",
#     "StreetPostalCode": "",
#     "RoleCode": "BUP002",
#     "GenderCode": "1",
#     "LanguageCode": "EN",
#     "LastName": "Doe",
#     "TitleCode": "",
#     "FirstName": "John",
#     "StateCode": ""
# }
# print("Creating new user..")
# res = s.post("https://my346965.crm.ondemand.com/sap/c4c/odata/v1/c4codataapi/IndividualCustomerCollection", data=json.dumps(data),
#        headers=headers)
# print(res.status_code)
# print(res.content)

if __name__ == "__main__":
    def generate_uuid(object_id) -> int:
        """
        Generates the UUID field for SAP C4C API based on the object_id (joined_customer_id) by adding the dash '-' character.
        :param object_id:
        :return:
        """
        # E.g : 00000001000201DCAF9A4F5AA6DA5B3A joined_id will give 00000000-0002-01DC-AF9A-4F5AA6DA5B3A
        uuid_list = [ object_id[:8], object_id[8:12], object_id[12:16], object_id[16:20], object_id[20:]]
        full_uuid = "-".join(uuid_list)
        return full_uuid

    original_id = "59154313539729028300000000000000"
    object_id = original_id
    res = generate_uuid(object_id)
    print(f"Original id is : {object_id}")
    print(f"UUID is : {res}")


    cust_id_1 = "859020892674153410000000000000"
    cust_id_2 = "26023671551725281850000000000000"
    cust_id_3 = "66793293475496124750000000000000"
    print('Len customer 1 :')
    print(len(cust_id_1))

    print('Len customer 2 :')
    print(len(cust_id_2))

    print('Len customer 3 :')
    print(len(cust_id_3))