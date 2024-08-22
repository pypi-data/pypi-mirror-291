import requests
import json

def fetch_all_problems():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            problems = data['result']['problems']
            with open('codeforces_problems.json', 'w') as f:
                json.dump(problems, f, indent=4)
            print(f"Downloaded {len(problems)} problems and saved to codeforces_problems.json")
        else:
            print("Error fetching problems:", data.get('comment', 'No comment'))
    else:
        print(f"Failed to connect to Codeforces API. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_all_problems()
