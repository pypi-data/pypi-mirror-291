import requests

from pydantic import BaseModel

from typing import Optional


class MachinaCoreClient:

    def __init__(self, base_url: str, api_key: str):

        self.base_url = base_url

        self.api_key = api_key

    def system_health_check(self):
        # Imagine this is your method to check the system health
        return {"status": "System is healthy"}

    def system_public_health_check(self):
        # Imagine this is your method to check the public system health
        return {"status": "Public system is healthy"}

# Define a main function to use the class
def main():

    # Example usage of MachinaCoreClient
    client = MachinaCoreClient(base_url="http://127.0.0.1:5000", api_key="your_api_key_here")

    # Call methods and print results
    health_check = client.system_health_check()
    print("Health Check:", health_check)

    public_health_check = client.system_public_health_check()
    print("Public Health Check:", public_health_check)

# This ensures the main function runs when the script is executed directly
if __name__ == "__main__":
    main()
