import re
from typing import Optional


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    if len(username) < 4 or len(username) > 20:
        return False, "Username must be between 4 and 20 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None


def validate_nickname(nickname: str) -> tuple[bool, Optional[str]]:
    if len(nickname) < 2 or len(nickname) > 50:
        return False, "Nickname must be between 2 and 50 characters"
    
    return True, None


def validate_birth_date(year: int, month: int, day: int) -> tuple[bool, Optional[str]]:
    if year < 1900 or year > 2025:
        return False, "Invalid birth year"
    
    if month < 1 or month > 12:
        return False, "Invalid birth month"
    
    if day < 1 or day > 31:
        return False, "Invalid birth day"
    
    return True, None