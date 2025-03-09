from fastapi import FastAPI
import requests
import dotenv
import json
import os

dotenv.load_dotenv()

app = FastAPI()

auth_token = os.getenv("VAPI_AUTH_TOKEN")
call_id = "4be883eb-c408-43ad-84e5-1e162bcfabb2"

headers = {
    'Authorization': f'Bearer {auth_token}'
}

def get_call_data():
    response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)

@app.get("/basic_info")
def basic_info():
    call_data = get_call_data()
    if call_data:
        return call_data
    return {"error": "Failed to retrieve call data"}

if __name__ == "__main__":
    call_data = get_call_data()

    if call_data:
        print("Call data:")
        print(json.dumps(call_data, indent=2))
    else:
        print("Failed to retrieve call data.")