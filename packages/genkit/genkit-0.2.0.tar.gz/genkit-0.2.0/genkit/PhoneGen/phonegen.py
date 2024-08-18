import random
from .country_code import code

class PhoneGen:
    def __init__(self, country="IN"):
        """
        Initialize the PhoneGen class with a specific country code.
        
        Parameters:
        country (str): The country code to use for generating phone numbers. 
                       Defaults to 'IN' for India. (Optional)
        """
        self.codes = code
        self.code = self.codes.get(country.upper(), "+91")

        if country.upper() not in self.codes:
            self.error_message = f"Invalid country code '{country}'. Please use a valid ISO country code."
            self.code = "+91"
        else:
            self.error_message = None

    def generate(self, length=10):
        """
        Generate a random phone number with the specified length.
        
        Parameters:
        length (int): The length of the phone number to generate. 
                      Defaults to 10. (Optional)
        
        Returns:
        str: A phone number with the specified length and country code or an error message.
        """
        if self.error_message:
            return self.error_message

        if not isinstance(length, int) or length <= 0:
            return "Error: Length must be a positive integer."

        try:
            if self.code == "+91":
                number = str(random.randint(6, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(length - 1)])
            else:
                number = ''.join([str(random.randint(0, 9)) for _ in range(length)])
            return f"{self.code}{number}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
