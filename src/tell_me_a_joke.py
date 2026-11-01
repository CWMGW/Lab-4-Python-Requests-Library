import json
import logging
import requests

# Configure logging to write to logs/lab4.log
logging.basicConfig(filename='logs/lab4.log', level=logging.INFO)

url = 'https://icanhazdadjoke.com/'
headers = {'Accept': 'application/json'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        logging.info("LAB4_JOKE_HTTP_OK")
        
        data = response.json()
        joke_text = data.get("joke", "")
        
        logging.info("LAB4_JOKE_JSON_OK")
        
        # Save full JSON artifact
        with open("data/joke.json", "w") as f:
            json.dump(data, f, indent=4)
            
        # Save joke text artifact
        with open("data/joke.txt", "w") as f:
            f.write(joke_text)
            
        # Print only the joke line to stdout (no extra text)
        print(joke_text)
        logging.info("LAB4_JOKE_PRINTED")
        
    else:
        logging.error("LAB4_ERR")
        print(f"Error: Received status code {response.status_code}", file=sys.stderr)

except requests.RequestException as e:
    logging.error("LAB4_ERR")
    print(f"Network error: {e}", file=sys.stderr)