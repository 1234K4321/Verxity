import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Make sure you have the 'google-generativeai' library installed:
# pip install google-generativeai

# Replace with your actual Gemini API Key from environment variables.
# For this example, we'll assume it's in the environment,
# or you can paste it directly here.
api_key = os.getenv("GEMINI_API_KEY", "") 

genai.configure(api_key=api_key)

app = Flask(__name__)
CORS(app) # Enable CORS for communication from the add-in

# A robust prompt for the Gemini 2.5 Pro model to ensure structured JSON output
SYSTEM_PROMPT = """You are an expert financial analyst AI. Your task is to generate financial report data based on a user's request. The user will provide a natural language prompt, and you must respond with a JSON object. This JSON object must contain two keys: "tableData" and "formatting".

"tableData" should be a 2D array of strings representing a financial table. The first row must be the header.
"formatting" should be a dictionary with keys for different parts of the table (e.g., "header", "data_labels", "border", "numberFormat") and values that specify the formatting rules.

Use this exact JSON schema:
{
  "tableData": [
    ["Metric", "Q1 2024", "Q2 2024"],
    ["Revenue", 1000000, 1100000]
  ],
  "formatting": {
    "header": {
      "range": "A1:C1",
      "bold": true,
      "backgroundColor": "#4472C4",
      "fontColor": "#FFFFFF",
      "horizontalAlignment": "center"
    },
    "data_labels": {
      "range": "A2:A2",
      "bold": true
    },
    "border": {
      "range": "A1:C2",
      "style": "Continuous",
      "color": "#000000"
    },
    "numberFormat": {
      "range": "B2:C2",
      "format": "$#,##0"
    }
  }
}

Use the data and formatting rules that are most appropriate for the user's request. Do not include any text outside of the JSON object.
"""

model = genai.GenerativeModel('gemini-2.5-pro', system_instruction=SYSTEM_PROMPT)

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        request_data = request.get_json()
        user_prompt = request_data.get('prompt')

        if not user_prompt:
            return jsonify({'success': False, 'error': 'Prompt is missing.'}), 400

        # Send the user prompt to the Gemini API
        response = model.generate_content(
            user_prompt,
            generation_config=genai.GenerationConfig(response_mime_type='application/json')
        )
        
        # The API returns a text response that should be a JSON string
        json_string = response.text
        
        # Parse the JSON string into a Python dictionary
        response_payload = json.loads(json_string)
        
        return jsonify({
            'success': True,
            'message': 'Report generated successfully.',
            'tableData': response_payload['tableData'],
            'formatting': response_payload['formatting']
        }), 200

    except Exception as e:
        app.logger.error(f"Error calling Gemini API: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

