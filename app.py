from flask import Flask, request, jsonify
import currencyapicom

app = Flask(__name__)

@app.route('/', methods=['POST'])  # Webhook route
def index():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging logs

        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = float(data['queryResult']['parameters']['unit-currency']['amount'])
        target_currency = data['queryResult']['parameters']['currency-name']

        # Fetch exchange rate
        conversion_factor = fetch_conversion_factor(source_currency, target_currency)
        final_amount = round(amount * conversion_factor, 2)

        response = {
            'fulfillmentText': f"{amount} {source_currency} is approximately {final_amount} {target_currency}."
        }
        print("Response:", response)
        return jsonify(response)
    
    except Exception as e:
        print("Error:", e)
        return jsonify({'fulfillmentText': "Sorry, I couldn't process the request."})

def fetch_conversion_factor(source, target):
    try:
        client = currencyapicom.Client('cur_live_83lF0fCijY5kzpToPPmHlKG80ort6IcfWxahaCfS')
        result = client.latest(source, currencies=[target])
        return result['data'][target]['value']
    
    except Exception as e:
        print("Error fetching conversion factor:", e)
        return 1  # Default to 1 if API fails

# Vercel expects a callable named `handler`
from vercel_wsgi import handle_request

def handler(event, context):
    return handle_request(app, event, context)
