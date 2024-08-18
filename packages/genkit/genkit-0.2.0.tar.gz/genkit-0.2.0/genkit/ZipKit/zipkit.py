import random
from difflib import get_close_matches
from .utils.india_pincode_16082024 import datalist
from .utils.source_info import data_source
class ZipKit:
    def __init__(self):
        self.zipcode_data = datalist
        self.last_updated = "2024-08-16"  # Example last updated date
        
        # Country-specific disclaimers and data sources
        self.country_info = data_source

    def _find_similar(self, value, options, n=5):
        """
        Find similar options based on provided value.
        
        Parameters:
        value (str): The value to match.
        options (list): A list of possible options.
        n (int): Number of similar options to return. Defaults to 5.
        
        Returns:
        list: A list of similar options.
        """
        return get_close_matches(value, options, n=n)

    def list_zipcodes(self, country="IN", city=None, state=None):
        """
        List all zip codes based on provided parameters.
        
        Parameters:
        country (str): The country code to list zip codes. Defaults to 'IN'.
        city (str, optional): The city to filter by. Defaults to None.
        state (str, optional): The state to filter by. Defaults to None.
        
        Returns:
        list: A list of zip codes matching the specified parameters.
        """
        country = country.lower()
        if country not in self.zipcode_data:
            suggested_country = self._find_similar(country, self.zipcode_data.keys())
            if suggested_country:
                print(f"Sorry, we couldn't find a match for the country: {country}. Is the country name correct?\nDid you mean: {suggested_country[0].upper()}?")
                return {"error": f"No data available for country code: {country}. Did you mean: {suggested_country[0].upper()}?"}
            else:
                return {"error": f"No data available for country code: {country}"}
        
        zip_codes = self.zipcode_data[country]
        
        if city:
            city_list = [details['city'] for details in zip_codes.values()]
            suggested_city = self._find_similar(city, city_list)
            if suggested_city:
                print(f"Sorry, we couldn't find a match for the city: {city}. Is the city name correct?\nDid you mean: {suggested_city[0].upper()}?")
                return {"error": f"No zip codes found for city: {city}. Did you mean: {suggested_city[0].upper()}?"}
            else:
                return {"error": f"No zip codes found for city: {city}"}
        
        if state:
            state_list = [details['state'] for details in zip_codes.values()]
            suggested_state = self._find_similar(state, state_list)
            if suggested_state:
                print(f"Sorry, we couldn't find a match for the state: {state}. Is the state name correct?\nDid you mean: {suggested_state[0].upper()}?")
                return {"error": f"No zip codes found for state: {state}. Did you mean: {suggested_state[0].upper()}?"}
            else:
                return {"error": f"No zip codes found for state: {state}"}
        
        return list(zip_codes.keys())

    def find(self, code):
        """
        Find details for a given zip code or pincode.
        
        Parameters:
        code (str): The zip code or pincode to search for.
        
        Returns:
        dict: Details about the zip code or pincode, including country, city, and state.
        """
        for country, zip_codes in self.zipcode_data.items():
            if code in zip_codes:
                details = zip_codes[code]
                result = {
                    "country": country.upper(),
                    "zip_code": code,
                    "details": details
                }

                # Get disclaimer and data source based on the country
                country_info = self.country_info.get(country, {
                    "data_source": "Unknown",
                    "disclaimer": "No disclaimer available for this country."
                })
                
                # Print formatted information
                print("\n--- Details ---")
                print(f"Country: {country.upper()}")
                print(f"Zip Code: {code}")
                print(f"City: {details.get('city', 'N/A')}")
                print(f"State: {details.get('state', 'N/A')}")
                print(f"Circle name: {details.get('circle_name', 'N/A')}")
                print(f"Region name: {details.get('region_name', 'N/A')}")
                print(f"Office name: {details.get('office_name', 'N/A')}")
                print(f"Office type: {details.get('office_type', 'N/A')}")
                print(f"Delivery status: {details.get('delivery_status', 'N/A')}")

                # Print disclaimer and additional information
                print("\n--- Disclaimer ---")
                # print(f"This data was last updated on {self.last_updated}.")
                # print(f"Source of data: {country_info['data_source']}")
                # print(f"Disclaimer: {country_info['disclaimer']}")
                print("For the most accurate and up-to-date information, please verify with official sources.\n")

                return result
        
        # If the zip code is not found, suggest similar zip codes
        for country, zip_codes in self.zipcode_data.items():
            possible_matches = [code for code in zip_codes if code.startswith(code[:3])]  # Adjust logic if needed
            if possible_matches:
                similar_zip_codes = self._find_similar(code, possible_matches)
                if similar_zip_codes:
                    print(f"Sorry, we couldn't find details for the entered zip code or pin code: {code}. Is that correct? Did you mean one of these?  {', '.join(similar_zip_codes)}")
                    return {"error": f"Zip code or pincode not found. Did you mean one of these? {', '.join(similar_zip_codes)}"}
        
        return {"error": "Zip code or pincode not found"}
