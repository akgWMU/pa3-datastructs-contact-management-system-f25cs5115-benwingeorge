from typing import List, Optional, Dict, Any

class Contact:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name.strip().lower() 
        self.phone = phone.strip()
        self.email = email.strip().lower()
    
    def __str__(self) -> str:
        return f"Contact(name='{self.name.title()}', phone='{self.phone}', email='{self.email}')"
    
    def __repr__(self) -> str:
        return self.__str__()