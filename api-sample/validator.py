#regex

import re

def validate_email(email):
    regexTemplate = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regexTemplate, email):
        return True
    else:
        return False