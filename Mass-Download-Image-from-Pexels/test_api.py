import urllib.request
import json

# Load API key from api.key file
try:
    with open('api.key', 'r') as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print("Error: api.key file not found. Please create an api.key file with your Pexels API key.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading api.key: {e}")
    sys.exit(1)

def test_api_key():
    url = "https://api.pexels.com/v1/search?query=test&per_page=1"
    headers = {
        "Authorization": API_KEY,
        "User-Agent": "Mozilla/5.0"
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if "photos" in data:
                print("API Key is working correctly!")
                print(f"Total results: {data['total_results']}")
            else:
                print("Error: Invalid API response")
                print(data)
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")
        if e.code == 401:
            print("Invalid API Key. Please verify your key.")
        elif e.code == 403:
            print("Forbidden. Possible reasons:")
            print("- API key is invalid or expired")
            print("- API key is not being sent correctly")
            print("- Your IP address might be blocked")
        else:
            print("API request failed. Check your connection or API key.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_api_key()
