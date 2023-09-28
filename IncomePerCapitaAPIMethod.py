import requests
import xml.etree.ElementTree as ET

class BEAIncomeData:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://apps.bea.gov/api/data"

    def get_income_data(self, year, state_code):
        params = {
            "UserID": self.api_key,
            "method": "GetData",
            "datasetname": "Regional",
            "TableName": "CAINC1",
            "LineCode": 3,  # Line code for personal income
            "GeoFIPS": state_code,  # State code (e.g., "DE" for Delaware)
            "Year": year,
            "ResultFormat": "XML",  # Request XML format
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return self.parse_income_data(response.text)
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_income_data_by_county(self, year, county_code):
        params = {
            "UserID": self.api_key,
            "method": "GetData",
            "datasetname": "Regional",  # Replace with the correct dataset name
            "TableName": "CAINC1",      # Replace with the correct table name
            "LineCode": 3,  # Line code for income data (adjust as needed)
            "GeoFIPS": county_code,  # County code or codes
            "Year": year,
            "ResultFormat": "XML",  # Request XML format (or JSON if preferred)
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return self.parse_income_data(response.text)
        else:
            print(f"Error: {response.status_code}")
            return None

    # Helper method to parse the XML response
    def parse_income_data(self, xml_response):
        income_data = []
        root = ET.fromstring(xml_response)
        for data_element in root.findall(".//Data"):
            geo_name = data_element.get("GeoName")
            data_value = data_element.get("DataValue")
            income_data.append((geo_name, data_value))
        return income_data

# Usage
if __name__ == "__main__":
    api_key = "Your-36CharacterKey"
    bea_data = BEAIncomeData(api_key)

    # Default values
    year = 2020
    state_code = "DE"  # Replace with the desired state code 
    county_code = "45001"  # Replace with the desired county FIPS code

    print("Would you like to search by state or county?")
    print("1. State")
    print("2. County")
    choice = input("Enter your choice: ")

    if choice == "1":
        state_code = input("Enter the state code (e.g., DE for Delaware): ")
        year = input("Enter the year: ")

        # Calling state search method
        income_data = bea_data.get_income_data(year, state_code)
        if income_data is not None:
            print("Per Capita Personal Income Data:")
            for geo_name, data_value in income_data:
                print(f"{geo_name}: ${data_value}")
        else:
            print("Failed to fetch income data.")
    
    if choice == "2":
        county_code = input("Enter the county code (e.g., 45001 for Kent County, DE): ")
        year = input("Enter the year: ")
        
        # Calling county search method
        income_data = bea_data.get_income_data_by_county(year, county_code)
        if income_data is not None:
            print("Income data for the specified county:")
            for geo_name, data_value in income_data:
                print(f"{geo_name}: ${data_value}")
        else:
            print("Failed to fetch income data.")
    
