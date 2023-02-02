import os
import json
import requests
from requests.auth import HTTPBasicAuth
from google.cloud import secretmanager

# TODO : Remember to authorize the access to the secret

DEFAULT_ROLE = "BUP002"  # Prospect
DEFAULT_CLASSIFICATION = "B"  # Non PIH Group

# map the customer_unified table to SAP Individual customer attributes
SAP_CUSTOMER_ATTRIBUTES_MAPPING = {
    "joined_customer_id" : "UUID",
    "phone_number" : "Phone",
    "email_address" : "Email",
    "last_name" : "LastName",
    "first_name" : "FirstName"
    # "CustomerABCClassificationCode": None,
    # "CountryCode": None,
    # "HouseNumber": None,
    # "Street": None,
    # "StreetPostalCode": None,
    # "StateCode": None,
    # "RoleCode": None,
    # "GenderCode": None,
    # "LanguageCode": None,
    # "TitleCode": None,
    }


def main(json):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    # request_json = request.get_json()
    request_json=json
    print(f"Executing {request_json['operation']} operation (received from Hightouch)")

    try:
        if request_json['operation'] == 'add':
            return create_customer(request_json['rows'], request_json['primary_key_column'])
        elif request_json['operation'] == 'change':
            return update_customer(request_json['rows'], request_json['primary_key_column'])
        else:
            return "Unknown value for parameter 'operation'", 400
    except:
        return "Function failed (see logs)", 400


def create_customer(customer_rows, primary_key_column):
    """Create a Customer entity object in the SAP C4C Database."""
    session = requests.Session()
    csrf_token = get_csrf_token(session)
    headers = {
        "x-csrf-token": csrf_token,
        "Content-Type": "application/json"
    }
    print("Creating new users..")
    errors_response = []
    for customer_row in customer_rows:
        print(customer_row)
        customer_sap = {}
        for customer_column , customer_value in customer_row.items():
            if customer_column in SAP_CUSTOMER_ATTRIBUTES_MAPPING.keys():
                if SAP_CUSTOMER_ATTRIBUTES_MAPPING[customer_column] != "UUID":
                    customer_sap[SAP_CUSTOMER_ATTRIBUTES_MAPPING[customer_column]] = customer_value if customer_value else "?"
                else:
                    object_id = customer_value
                    customer_sap["UUID"] = generate_uuid(object_id)
        customer_sap["RoleCode"] = DEFAULT_ROLE
        customer_sap["CustomerABCClassificationCode"] = DEFAULT_CLASSIFICATION
        print(customer_sap)
        # POST request to create customer in SAP C4C
        create_request = session.post(f"{os.environ['C4C_SAP_API_BASE_URL']}/IndividualCustomerCollection",
                                      data=json.dumps(customer_sap),
                                      headers=headers)
        print(create_request.text)
        if create_request.status_code != 201:
            print("user not created")
            errors_response.append({primary_key_column: customer_row[primary_key_column]})

    # Check errors
    if len(errors_response) > 0:
        return {"errors": errors_response}, 400
    else :
        print("User created")
    return {"message": "Users successfully created in SAP"}, 201


def update_customer(customer_rows, primary_key_column):
    """Update a Customer entity object in the SAP C4C Database."""
    session = requests.Session()
    csrf_token = get_csrf_token(session)
    headers = {
        "x-csrf-token": csrf_token,
        "Content-Type": "application/json"
    }
    print("Updating users..")
    errors_response = []

    for customer_row in customer_rows:
        customer_sap = {}
        object_id = None
        print(customer_row)
        for customer_column , customer_value in customer_row.items():
            if customer_column in SAP_CUSTOMER_ATTRIBUTES_MAPPING.keys():
                if SAP_CUSTOMER_ATTRIBUTES_MAPPING[customer_column] != "UUID":
                    customer_sap[SAP_CUSTOMER_ATTRIBUTES_MAPPING[customer_column]] = customer_value
                else :
                    object_id = customer_value
                    customer_sap["UUID"] = generate_uuid(object_id)
        customer_sap["RoleCode"] = DEFAULT_ROLE
        customer_sap["CustomerABCClassificationCode"] = DEFAULT_CLASSIFICATION

        # PATCH request to update customer in SAP C4C
        create_request = session.patch(f"{os.environ['C4C_SAP_API_BASE_URL']}/IndividualCustomerCollection('{object_id}')",
                                      data=json.dumps(customer_sap),
                                      headers=headers)
        if create_request.status_code != 204:
            errors_response.append({primary_key_column: customer_row[primary_key_column]})

    # Check errors
    if len(errors_response) > 0:
        return {"errors": errors_response}, 400

    return {"message": "Users successfully updated in SAP"}, 201

def get_secret_data(project_id, secret_id):
    """Get the C4C SAP API password."""
    client = secretmanager.SecretManagerServiceClient()
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_detail})
    data = response.payload.data.decode("UTF-8")
    return data


def get_csrf_token(session):
    """
    Request the X-CSFR-Token of C4C SAP API. (See following link documentation)
    https://github.com/SAP/C4CODATAAPIDEVGUIDE#csrf-token
    """
    headers = {
        "x-csrf-token": "fetch",
    }
    print("Fetching x-csfr-token")
    c4c_odata_api_pswd = get_secret_data(
        os.environ["GCP_PROJECT"], os.environ["C4C_SAP_API_LOGIN"]
    )
    basic_auth = HTTPBasicAuth(os.environ['C4C_SAP_API_LOGIN'], c4c_odata_api_pswd)
    login_res = session.get(os.environ['C4C_SAP_API_BASE_URL'], headers=headers, auth=basic_auth)
    print(f'Retrieved X-CSRF-Token -> {login_res.status_code}')
    return login_res.headers['x-csrf-token']


def generate_uuid(object_id) -> str:
    """
    Generates the correct UUID field for SAP C4C API based on the object_id (joined_customer_id) by adding the dash '-' character.
    :param object_id:
    :return:
    """
    # E.g : 00000001000201DCAF9A4F5AA6DA5B3A joined_id will give 00000000-0002-01DC-AF9A-4F5AA6DA5B3A
    uuid_list = [object_id[:8], object_id[8:12], object_id[12:16], object_id[16:20], object_id[20:]]
    full_uuid = "-".join(uuid_list)
    return full_uuid

if __name__ == "__main__":
    os.environ['C4C_SAP_API_LOGIN'] = "C4CDATAREADER"
    os.environ['C4C_SAP_API_BASE_URL'] = "https://my346965.crm.ondemand.com/sap/c4c/odata/v1/c4codataapi"
    os.environ["GCP_PROJECT"] = "dbt-test-yannis"
    # hightouch_json = {
    #   "operation": "add",
    #   "primary_key_column": "joined_customer_id",
    #   "rows": [
    #     {
    #       "email_address": "customer_a@email.con",
    #       "first_name": "BJoneManual",
    #       "joined_customer_id": "74836477220601505680000000888999",
    #       "last_name": "BDoeManual",
    #       "merged_customer": "bxyz",
    #       "phone_number": "+32100200300"
    #     }
    #   ],
    #   "metadata": {
    #     "api_version": 1,
    #     "sync_run_id": -1,
    #     "sync_id": -1
    #   }
    # }
    hightouch_json = {
      "operation": "add",
      "primary_key_column": "joined_customer_id",
      "rows": [
        {
          "joined_customer_id": "25856386863121830890000000099999",
          "email_address": "na702043@gmail.com",
          "phone_number": "966552629901",
          "first_name": "Nawaf9",
          "last_name": " ",
          "merged_customers": [
            "DrwxSr7/mNCgWLAzkJDUfsa1ZXNIcIF1OYAFIymhVQw="
          ]
        }
      ],
      "metadata": {
        "api_version": 1,
        "sync_run_id": 122819103,
        "sync_id": 76992
      }
    }
    main(hightouch_json)
