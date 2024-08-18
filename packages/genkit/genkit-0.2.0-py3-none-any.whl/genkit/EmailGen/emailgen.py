import random
import string

class EmailGen:
    def __init__(self, domain="example.com"):
        """
        Initialize the EmailGen class with a specific domain.
        
        Parameters:
        domain (str): The domain to use for generating email addresses. 
                      Defaults to 'example.com'. (Optional)
        """
        if not isinstance(domain, str) or "@" in domain:
            self.error_message = "Invalid domain. Domain must be a valid string without '@'."
            self.domain = "example.com"
        else:
            self.error_message = None
            self.domain = domain

    def generate(self, length=8):
        """
        Generate a random email address with the specified username length.
        
        Parameters:
        length (int): The length of the username part of the email address. 
                      Defaults to 8. (Optional)
        
        Returns:
        str: A random email address with the specified username length and domain or an error message.
        """
        if self.error_message:
            return self.error_message

        if not isinstance(length, int) or length <= 0:
            return "Error: Length must be a positive integer."

        try:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            return f"{username}@{self.domain}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
