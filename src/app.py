from flask import Flask, request, jsonify
import requests
import json
import os
import yaml
from datetime import datetime

# Enable debug mode
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

app = Flask(__name__)

PUMBLE_WEBHOOK_URL = os.environ.get("PUMBLE_WEBHOOK_URL")
if not PUMBLE_WEBHOOK_URL:
    raise ValueError("PUMBLE_WEBHOOK_URL environment variable is not set")

def json_to_yaml(json_data):
    """Convert JSON to YAML string format."""
    try:
        yaml_str = yaml.dump(json_data, sort_keys=False, default_flow_style=False)
        return f"```Alertmanager\n{yaml_str}\n```"
    except Exception as e:
        print(f"Error converting JSON to YAML: {e}")
        return json.dumps(json_data, indent=2)

def send_to_pumble(message, username="Alertmanager Bot"):
    """Send a message to Pumble via webhook."""
    if DEBUG:
        print(f"DEBUG - Sending message to Pumble")
        print(f"DEBUG - Webhook URL: {PUMBLE_WEBHOOK_URL}")
    
    payload = {
        "text": message,
        "username": username
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(PUMBLE_WEBHOOK_URL, json=payload, headers=headers)
        if DEBUG:
            print(f"DEBUG - Response status: {response.status_code}")
            print(f"DEBUG - Response body: {response.text}")
        response.raise_for_status()
        print(f"Message sent to Pumble")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Pumble: {e}")

@app.route('/', methods=['POST'])
def webhook():
    """Receive and process alerts from Alertmanager."""
    try:
        if DEBUG:
            print(f"DEBUG - Received webhook request")
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if DEBUG:
            print(f"DEBUG - Request data: {json.dumps(data, indent=2)}")
        
        # Convert JSON to YAML format
        yaml_message = json_to_yaml(data)
        
        # Add status header for quick glance
        status = data.get("status", "unknown").upper()
        alert_name = data.get("groupLabels", {}).get("alertname", "Unknown Alert")
        header = f"🚨 *ALERT {status}*: {alert_name}\n\n"
        
        # Send the combined message to Pumble
        send_to_pumble(header + yaml_message)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error processing alert: {e}")
        if DEBUG:
            import traceback
            print(f"DEBUG - Error traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Make sure PyYAML is installed
    if not 'yaml' in globals():
        print("Please install PyYAML: pip install pyyaml")
        exit(1)
    
    # Set debug mode for Flask
    app.debug = DEBUG
    print(f"Starting server with DEBUG={'enabled' if DEBUG else 'disabled'}")
    app.run(host="0.0.0.0", port=9094)