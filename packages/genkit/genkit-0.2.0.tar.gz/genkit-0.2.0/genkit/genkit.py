import time
import json
from .PhoneGen.phonegen import PhoneGen
from .EmailGen.emailgen import EmailGen
from .config import get_config
from .ZipKit.zipkit import ZipKit

class GenKit:
    @staticmethod
    def phonenumber(country="IN", n=1, type="string", save=False):
        """
        Generate a specified number of phone numbers for a given country.
        
        Parameters:
        country (str): The country code to use for generating phone numbers. 
                       Defaults to 'IN'. (Optional)
        n (int): The number of phone numbers to generate. 
                 Defaults to 1. (Optional)
        type (str): The format of the output. 'string' (default), 
                    'list', or 'dict'. Defaults to 'string'. (Optional)
        save (bool): Whether to save the generated phone numbers to a file. 
                     Defaults to False. (Optional)
        
        Returns:
        str | list | dict: The generated phone numbers in the specified format.
        """
        country = country.lower()
        config = get_config()
        phone_gen = PhoneGen(country)
        numbers = [phone_gen.generate() for _ in range(n)]

        output_type = config["output_types"].get(type, config["output_types"]["string"])
        result = output_type(numbers)
        
        if save:
            timestamp = int(time.time())
            filename = f"genkit_{timestamp}.txt"
            with open(filename, "w") as file:
                if type == "dict":
                    file.write(output_type(numbers))
                else:
                    file.write(result)
            print(f"Data saved to file: {filename}")       
        
        return result

    @staticmethod
    def email(domain="example.com", n=1, length=8, type="string", save=False):
        """
        Generate a specified number of email addresses for a given domain.
        
        Parameters:
        domain (str): The domain to use for generating email addresses. 
                      Defaults to 'example.com'. (Optional)
        n (int): The number of email addresses to generate. 
                 Defaults to 1. (Optional)
        length (int): The length of the username part of the email address. 
                      Defaults to 8. (Optional)
        type (str): The format of the output. 'string' (default), 
                    'list', or 'dict'. Defaults to 'string'. (Optional)
        save (bool): Whether to save the generated email addresses to a file. 
                     Defaults to False. (Optional)
        
        Returns:
        str | list | dict: The generated email addresses in the specified format.
        """
        config = get_config()
        email_gen = EmailGen(domain)
        emails = [email_gen.generate(length) for _ in range(n)]

        output_type = config["output_types"].get(type, config["output_types"]["string"])
        result = output_type(emails)
        
        if save:
            timestamp = int(time.time())
            filename = f"genkit_{timestamp}.txt"
            with open(filename, "w") as file:
                if type == "dict":
                    file.write(output_type(emails))
                else:
                    file.write(result)
            print(f"Data saved to file: {filename}")       
        
        return result
    
    @staticmethod
    def zipkit(country=None, city=None, state=None, find=None):
        """
        Get zip code information or list all zip codes based on filters.
        
        Parameters:
        country (str): The country code to list zip codes. If provided, lists all zip codes for the specified country.
        city (str): The city to filter zip codes. Optional.
        state (str): The state to filter zip codes. Optional.
        find (str): The zip code to find details for. If provided, returns details for that zip code.
        
        Returns:
        list | dict: A list of zip codes or details about a specific zip code.
        """

        country = country.lower() if country else None
        city = city.lower() if city else None
        state = state.lower() if state else None
        
        zip_kit = ZipKit()
        
        if find:
            # Find details for a specific zip code
            result = zip_kit.find(find.lower())
            if "error" in result:
                return {"error": result["error"]}
            return result
        
        if country:
            # List all zip codes based on country, city, and state
            result = zip_kit.list_zipcodes(country, city, state)
            if not result:
                return {"error": f"No zip codes found for the specified parameters."}
            return result
        
        return {"error": "Please provide either 'country' or 'find' parameter"}
    
    