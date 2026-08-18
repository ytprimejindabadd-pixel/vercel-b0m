from flask import Flask, request, jsonify, Response
import requests
import time
import json

app = Flask(__name__)

# Your existing API endpoint
SMS_API = "https://way-bombm.onrender.com/send"

@app.route('/send', methods=['GET'])
def send_sms():
    try:
        # Get parameters from URL
        phone = request.args.get('phone', '')
        count = request.args.get('count', '1')
        
        if not phone:
            return jsonify({
                "success": False,
                "error": "Phone number required"
            }), 400
        
        # Call your existing API
        response = requests.get(
            f"{SMS_API}?phone={phone}&count={count}",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Return only required fields
            return jsonify({
                "failed": data.get("failed", 0),
                "phone": data.get("phone", phone),
                "success": data.get("success", False),
                "successful": data.get("successful", 0),
                "total_sent": data.get("total_sent", 0)
            })
        else:
            return jsonify({
                "failed": 1,
                "phone": phone,
                "success": False,
                "successful": 0,
                "total_sent": 0
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            "failed": 1,
            "phone": phone,
            "success": False,
            "successful": 0,
            "total_sent": 0,
            "error": "Request timeout"
        }), 504
        
    except Exception as e:
        return jsonify({
            "failed": 1,
            "phone": phone,
            "success": False,
            "successful": 0,
            "total_sent": 0,
            "error": str(e)
        }), 500

# Root endpoint
@app.route('/')
def home():
    return jsonify({
        "service": "SMS API",
        "endpoint": "/send?phone=1234567890&count=10"
    })

# Vercel serverless handler
def handler(request):
    return app(request)

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
