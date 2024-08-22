__all__ = ['fetch_data', 'fetch_data_csv', 'fetch_data_text']

import requests

def fetch_data(query):
    """Fetch data from the API and return the raw response."""
    response = requests.get(f'https://webstore-scrapper.onrender.com/search?query={query}')
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")

def fetch_data_csv(query, file_name='output.csv'):
    """Fetch data from the API and save it as a CSV file."""
    data = fetch_data(query)
    with open(file_name, 'wb') as f:
        f.write(data)
    print(f"Data saved to {file_name}")

def fetch_data_text(query, file_name='output.txt'):
    """Fetch data from the API and save it as a plain text file."""
    data = fetch_data(query)
    with open(file_name, 'wb') as f:
        f.write(data)
    print(f"Data saved to {file_name}")