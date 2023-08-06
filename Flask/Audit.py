import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Sqq_MrTbSVGoX1xdHzJd0JhhIlvMN5DC7_G5uAmWbcMw"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": ["Sector_score","PARA_A","Risk_A","PARA_B","Risk_B","TOTAL","numbers","Money_Value","Score_MV","District_Loss","Risk_F","Score","Inherent_Risk","Audit_Risk"], "values": [[3.89,4.18,2.508,2.5,0.5,6.68,5,3.38,0.2,2,0,2.4,8.574,1.7148]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/937225dc-23aa-409b-accb-c8efeacc43de/predictions?version=2023-05-19', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
print("--------------------------------------")
pred=response_scoring.json()
output=pred['predictions'][0]['values'][0][0]
print(output)