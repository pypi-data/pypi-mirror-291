# GenKit

**GenKit** is a versatile Python package designed to generate random data such as phone numbers and email addresses, and to retrieve and filter zip code information. Whether you're developing, testing, or just need random data generation utilities, **GenKit** is the tool for you.

## Features

- **Zip Code Information**
  - Retrieve zip code information based on country, city, and state.
  - List all zip codes for a country or find specific zip code details.
- **Phone Number Generation**
  - Generate random phone numbers for different countries.
  - Supports output in string, list, and dictionary formats.
  - Option to save generated phone numbers to a file.
- **Email Address Generation**
  - Generate random email addresses with customizable domains and username lengths.
  - Multiple output formats: string, list, and dictionary.
  - Option to save generated email addresses to a file.

## Installation

You can easily install genkit using pip. Run the following command to install it:

```

pip install genkit

```

## Usage

### Zip Code Information

The `zipkit` method provides a simple way to retrieve zip code information based on your filters. You can find specific details about a zip code or get a list of zip codes filtered by country, state, and city.

#### Features

- **Find Zip Code Details**
  Get detailed information about a specific zip code.
- **Filter Zip Codes**
  Retrieve a list of zip codes based on country, state, or city filters, or a combination of these.
  ##### **Parameters**

  | Parameters               | Default   | Description                                                                                                                         |
  | ------------------------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
  | **country** (str) | IN(India) | The country for which you want to retrieve zip code information                                                                     |
  | **state**  (str)  | optional  | The state within the country to filter zip codes.                                                                                   |
  | **city**  (str)   | optional  | The city within the state to filter zip codes.                                                                                      |
  | **find** (str)     |           | A specific zip code to look up. If provided, this overrides other filters and returns the details for the specified zip<br /> code. |

#### Examples

```
from genkit import GenKit

gk = GenKit()
zipcode_info = gk.zipkit(country="US", state="CA", city="San Francisco")
print(zipcode_info)

# Example of finding a specific zip code
zipcode_details = gk.zipkit(find="682301")
print(zipcode_details)
```

#### **Example Output:**

```python
print(zipcode_details)
{
  "Country": "IN",
  "Zip Code": "682301",
  "City": "ERNAKULAM",
  "State": "Kerala",
  "Circle name": "Kerala Circle",
  "Region name": "Kochi Region",
  "Office name": "Tripunithura SO",
  "Office type": "SO",
  "Delivery status": "Delivery"
}
```

#### Supported Countries

Currently, **GenKit** supports zip code information for:

- **India (IN)**
- **United States (US)**

More countries will be added in future updates.

### Phone Number Generation

The `phonenumber` method in **GenKit** allows you to generate random phone numbers. You can specify the country, the number of phone numbers to generate, the output format, and whether the numbers should be saved to a file.

#### Features

- **Generate Random Phone Numbers**
  Generate one or more random phone numbers based on the specified country. The numbers can be returned in various formats and saved to a file if needed. 
- **Output Formats**
  - **String** : A phone number as a string.
  - **List** : A list of phone numbers.
  - **Dictionary** : A dictionary with the data as the key and a list of phone numbers as the value.

#### **Parameters**

| Parameters               | Default   | Description                                                                      |
| ------------------------ | --------- | -------------------------------------------------------------------------------- |
| **country** (str) | IN(India) | The country code (e.g., "IN" for India, "US" for the United States).             |
| **n**  (int)      | 1         | The state within the country to filter zip codes.                                |
| **type**  (str)   | string    | The format of the generated phone number(s). Can be "string", "list", or "dict". |
| **save**  (bool)  | True      | Whether to save the generated phone numbers to a text file.                      |

Use 2-digit ISO codes to generate

#### Examples

#### Generating a Single Phone Number

```
from genkit import GenKit

# Generate a phone number for India (default)
print(GenKit.phonenumber())

# Generate a phone number for the US
print(GenKit.phonenumber("US"))


```

#### Generating Multiple Phone Numbers

To generate multiple phone numbers, use the `n` parameter to specify the quantity. You can also specify the output format using the `type` parameter.

```
from genkit import GenKit

# Generate 5 phone numbers for India and return as a list
print(GenKit.phonenumber("IN", n=5, type="list"))

# Generate 3 phone numbers for the US and return as a dictionary
print(GenKit.phonenumber("US", n=3, type="dict"))

```

#### Saving to a File

You can save the generated phone numbers to a text file. The file will be named `genkit_TIMESTAMP.txt`, where `TIMESTAMP` is the current timestamp.

```
from genkit import GenKit

# Generate 5 phone numbers for India and save to a file
GenKit.phonenumber("IN", n=5, save=True)

# Generate 3 phone numbers for the US in dictionary format and save to a file
GenKit.phonenumber("US", n=3, type="dict", save=True)


```

### Email Address Generation

The `email` method in **GenKit** helps you generate random email addresses. You can customize the domain, the length of the emails, the output format, and whether the emails should be saved to a file.

#### Features

- **Generate Random Email Addresses**
  Generate one or more random email addresses with customizable domains and username lengths.
- **Output Formats**
  - **String** : A email address as a string.
  - **List** : A list of email addresses.
  - **Dictionary** : A dictionary with the data as the key and a list of email as the value.

#### Parameters

| Parameters               | Default     | Description                                                               |
| ------------------------ | ----------- | ------------------------------------------------------------------------- |
| **domain** (str)   | example.com | The email domain to use (e.g., "example.com").                            |
| **length**  (int) | 8           | The length of the generated email username.                               |
| **type**  (str)   | string      | The format of the generated email(s). Can be "string", "list", or "dict". |
| **n** (int)        | 1           | The number of email addresses to generate.                                |
| **save**  (bool)  | True        | Whether to save the generated email addresses to a text file.             |

#### Examples

#### Generating a Single Email Address

```
from genkit import GenKit

# Generate a random email address
print(GenKit.emailkit())

# Generate a random email address with a custom domain
print(GenKit.emailkit(domain="customdomain.com"))
```

#### Generating Multiple Email Addresses

To generate multiple email addresses, use the `n` parameter to specify the quantity. You can also specify the output format using the `type` parameter.

```
from genkit import GenKit

# Generate 5 random email addresses and return as a list
print(GenKit.emailkit(n=5, type="list"))

# Generate 3 random email addresses with a custom domain and return as a dictionary
print(GenKit.emailkit(domain="customdomain.com", n=3, type="dict"))
```

#### Saving to a File

You can save the generated email addresses to a text file. The file will be named `genkit_TIMESTAMP.txt`, where `TIMESTAMP` is the current timestamp.

```
from genkit import GenKit

# Generate 5 random email addresses and save to a file
GenKit.emailkit(n=5, save=True)

# Generate 3 random email addresses with a custom domain in dictionary format and save to a file
GenKit.emailkit(domain="customdomain.com", n=3, length=10, type="dict", save=True)
```

## Authors

For any questions or issues, please contact:

- **Author** : [Suhail Shaji](https://github.com/suhailshaji)
- **Email** : [suhailshaji@gmail.com]()

## Feedback

If you have any feedback, please reach out to us at
suhailshaji@gmail.com

## License

[MIT](https://choosealicense.com/licenses/mit/)

## 🔗 Connect

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/suhailshaji)
