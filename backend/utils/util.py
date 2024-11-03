import phonenumbers
import random
from phonenumbers.phonenumberutil import region_code_for_country_code, country_code_for_region

def generate_random_phone_number(country_code):
    """
    Generates a random, verified phone number for a given country.
    
    Args:
        country_code (str): Two-letter ISO country code (e.g., 'US', 'VN').
        
    Returns:
        str: A verified random phone number in international format, or None if unable to generate.
    """
    try:
        # Get the numeric country dialing code
        dialing_code = country_code_for_region(country_code)
        
        # Generate a random 7-10 digit number (typical length for local phone numbers)
        local_number = random.randint(10**6, 10**10 - 1)  # Adjust for realistic length per country
        phone_number_str = f"+{dialing_code}{local_number}"
        
        # Parse and verify the number using phonenumbers
        parsed_number = phonenumbers.parse(phone_number_str, country_code)
        
        # Ensure the number is valid; try again if not
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        else:
            # Retry until a valid number is generated
            return generate_random_phone_number(country_code)
    
    except Exception as e:
        print(f"Error generating phone number: {e}")
        return None