from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)

# Your SMS API endpoint
SMS_API = "https://way-bombm.onrender.com/send"

@app.route('/send', methods=['GET'])
def send_sms():
    # Get parameters
    phone = request.args.get('phone', '')
    count = request.args.get('count', '1')
    
    # Validate phone number
    if not phone or not re.match(r'^\d{10}$', phone):
        return jsonify({
            "failed": 1,
            "phone": phone if phone else "invalid",
            "success": False,
            "successful": 0,
            "total_sent": 0,
            "error": "Invalid phone number (10 digits required)"
        }), 400
    
    try:
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
                "total_sent": 0,
                "error": f"API returned {response.status_code}"
            })
            
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

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "SMS Gateway API"
    })

# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "SMS API Gateway",
        "endpoint": "/send?phone=1234567890&count=10",
        "example": "https://my-web.vercel.app/send?phone=9876543210&count=5",
        "health": "/health"
    })

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
