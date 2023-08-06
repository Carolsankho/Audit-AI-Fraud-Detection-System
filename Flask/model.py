from flask import Flask, request, jsonify, render_template

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud 
import requests
API_KEY = "Sqq_MrTbSVGoX1xdHzJd0JhhIlvMN5DC7_G5uAmWbcMw"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


import pickle



model=pickle.load(open('knn.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def f():
    return render_template("index.html")

@app.route('/home')
def Home():
    return render_template('page-1.html')

@app.route('/riskpred', methods=['GET', 'POST'])
def About():
    if request.method == "POST":
        Sector_score=request.form['Sector_score']
        PARA_A=request.form['PARA_A']
        Risk_A=request.form['Risk_A']
        PARA_B=request.form['PARA_B']
        Risk_B=request.form['Risk_B']
        TOTAL=request.form['TOTAL']
        numbers=request.form['numbers']
        Money_Value=request.form['Money_Value']
        Score_MV=request.form['Score_MV']
        District_Loss=request.form['District_Loss']
        History=request.form['History']
        Score=request.form['Score']
        Inherent_Risk=request.form['Inherent_Risk']
        Audit_Risk=request.form['Audit_Risk']
        pred = [[float(Sector_score), float(PARA_A), float(Risk_A), float(PARA_B), float(Risk_B), float(TOTAL), float(numbers),float(Money_Value), float(Score_MV), float(District_Loss), float(History), float(Score), float(Inherent_Risk), float(Audit_Risk)]] 
        #print(pred)
        #output = model.predict(pred)
        #print(output)
        
        # NOTE: manually define and pass the array(s) of values to be scored in the next line

        payload_scoring = {"input_data": [{"fields": ["Sector_score","PARA_A","Risk_A","PARA_B","Risk_B","TOTAL","numbers","Money_Value","Score_MV","District_Loss","Risk_F","Score","Inherent_Risk","Audit_Risk"], "values": [[3.89,4.18,2.508,2.5,0.5,6.68,5,3.38,0.2,2,0,2.4,8.574,1.7148]]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/937225dc-23aa-409b-accb-c8efeacc43de/predictions?version=2023-05-19', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        print("--------------------------------------")
        pred=response_scoring.json()
        output=pred['predictions'][0]['values'][0][0]
        print(output)
        
        
        return render_template('page-2.html', pred=output)


if __name__=='__main__':
    app.run(debug=True,port=9000)