from flask import Flask,request,jsonify
import requests
import currencyapicom


app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']


    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):
    client = currencyapicom.Client('cur_live_83lF0fCijY5kzpToPPmHlKG80ort6IcfWxahaCfS')
    result = client.latest(source, currencies=[target])
    converstion_factor = result['data'][target]['value']
    return converstion_factor

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()