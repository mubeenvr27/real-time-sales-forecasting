import requests
import json
import time

def test_lambda():
    # Wait a moment for the container to start
    time.sleep(2)
    
    url = "http://localhost:9000/2015-03-31/functions/function/invocations"
    payload = {
        "body": json.dumps({
            "date": "2024-06-30",
            "sales": 35,
            "stock": 70
        })
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except requests.exceptions.ConnectionError:
        print("Connection failed - is the Lambda container running?")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_lambda()