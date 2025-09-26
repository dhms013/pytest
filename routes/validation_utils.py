import re

# Regex patterns (compiled for efficiency)
# Name: only alphabets and spaces
NAME_REGEX = re.compile(r'^[a-zA-Z\s]+$')

# Phone Number: only numbers, 9 to 12 digits
PHONE_REGEX = re.compile(r'^\d{9,12}$')

# Email: enforced lowercase, format allows for multiple TLD segments (e.g., mail.co.us)
EMAIL_FORMAT_REGEX = re.compile(r'^[^\s@]+@[^\s@]+(\.[^\s@]+)+$')


def validate_user_fields(data, required_fields=None):
    # 1. Check for missing required fields (POST only)
    if required_fields:
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400

    # 2. Validate Name
    # The validation inside the block only runs if 'name' is IN data (optional for PUT)
    if 'name' in data:
        if not NAME_REGEX.match(data['name']):
            return {"error": "Invalid name: Only alphabets and spaces allowed"}, 422
    
    # 3. Validate Phone Number
    # The validation inside the block only runs if 'phoneNumber' is IN data (optional for PUT)
    if 'phoneNumber' in data:
        phone_number = data['phoneNumber']
        if not PHONE_REGEX.match(phone_number):
            if len(phone_number) < 9:
                return {"error": "Phone number is too short (minimum 9 digits)"}, 422
            elif len(phone_number) > 12:
                return {"error": "Phone number is too long (maximum 12 digits)"}, 422
            else:
                return {"error": "Invalid phone number format"}, 422
    
    # 4. Validate Email
    # The validation inside the block only runs if 'email' is IN data (optional for PUT)
    if 'email' in data:
        email = data['email']
        
        # A. Enforce strictly lowercase input (Strict format validation)
        if any(c.isupper() for c in email):
            return {"error": "Email must be in all lowercase letters."}, 422

        # B. Validate email format (Strict format validation)
        if not EMAIL_FORMAT_REGEX.match(email):
            return {"error": "Invalid email format"}, 422

    # If all checks pass
    return None, None
