import requests

from pydantic import BaseModel

from typing import Optional


class MachinaClient:

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def system_core_health_check(self):
        # Sending a GET request to the system health check endpoint
        url = f"{self.base_url}/system/core/health-check"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def system_core_session_check(self):
        # Sending a GET request to the public system health check endpoint
        url = f"{self.base_url}/system/core/session-check"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

# Define a main function to use the class
def main():
    # Example usage of MachinaClient
    client = MachinaClient(base_url="http://127.0.0.1:5000", api_key="your_api_key_here")

    # Call methods and print results
    try:
        health_check = client.system_core_health_check()
        print("Health Check:", health_check)

        session_check = client.system_core_session_check()
        print("Session Check:", session_check)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# This ensures the main function runs when the script is executed directly
if __name__ == "__main__":
    main()
