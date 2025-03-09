import requests
import dotenv
import os
import json

# Load environment variables
dotenv.load_dotenv()

# Get auth token from environment variables
auth_token = os.getenv("VAPI_AUTH_TOKEN")
if not auth_token:
    print("Warning: VAPI_AUTH_TOKEN environment variable not set")
    exit(1)

headers = {
    'Authorization': f'Bearer {auth_token}'
}

def get_latest_call_id():
    try:
        print("Attempting to fetch latest call ID...")
        # Use the List Calls endpoint with limit=1 to get only the most recent call
        response = requests.get('https://api.vapi.ai/call?limit=1', headers=headers)
        
        if response.status_code == 200:
            calls_data = response.json()
            
            # Check if the response contains calls data
            if calls_data and 'calls' in calls_data and len(calls_data['calls']) > 0:
                latest_call = calls_data['calls'][0]
                latest_call_id = latest_call['id']
                print(f"Latest call ID: {latest_call_id}")
                return latest_call_id
            else:
                print("No calls found in the response")
                print(f"Response content: {json.dumps(calls_data, indent=2)}")
                return None
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def get_call_data(call_id):
    try:
        print(f"Fetching data for call ID: {call_id}")
        response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

# Main execution
if __name__ == "__main__":
    # Get the latest call ID
    latest_call_id = get_latest_call_id()
    
    if latest_call_id:
        # Get data for the latest call
        call_data = get_call_data(latest_call_id)
        
        if call_data:
            # Print formatted JSON for better readability
            print("Call Data:")
            print(json.dumps(call_data, indent=2))
        else:
            print("Failed to retrieve call data")
    else:
        print("Bugged Line")
