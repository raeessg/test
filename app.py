import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- Your Twilio Credentials ---
# Retrieve credentials from environment variables for security.
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
MESSAGING_SERVICE_SID = os.getenv('MESSAGING_SERVICE_SID')

# Ensure environment variables are loaded
if not all([ACCOUNT_SID, AUTH_TOKEN, MESSAGING_SERVICE_SID]):
    raise ValueError("One or more Twilio environment variables are not set. Please check your .env file.")

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app) 

# Initialize the Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- API Endpoint Definition ---
@app.route('/send-sms', methods=['POST'])
def send_sms():
    """Receives data from the webpage and sends an SMS message."""
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')
        # The 'to' number is sent from the webpage's input field
        to_number = data.get('to')

        if not all([lat, lon, to_number]):
            return jsonify({'error': 'Missing latitude, longitude, or to_number'}), 400

        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        message_body = f"Emergency Alert! A potential incident has been detected. Last known location: {google_maps_link}"

        # --- THIS IS THE UPDATED PART ---
        # We are now using the new snippet's logic to send a standard SMS.
        message = client.messages.create(
            messaging_service_sid=MESSAGING_SERVICE_SID,
            body=message_body,
            to=to_number  # The number from the webpage input
        )
        # --- END OF UPDATED PART ---

        print(f"SMS sent successfully! SID: {message.sid}")
        return jsonify({'status': 'success', 'sid': message.sid})

    except Exception as e:
        print(f"Error sending SMS: {e}")
        return jsonify({'error': str(e)}), 500

# --- Start the Server ---
if __name__ == '__main__':
    app.run(port=5000, debug=True)

