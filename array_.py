from typing import List, Optional, Dict, Any
from helper import Contact

class ArrayImpl:
    def __init__(self):
        self.contacts: List[Contact] = []
        self.size = 0
    
    def insert(self, name: str, phone: str, email: str) -> bool:
        if self.search(name) is not None:
            return False
        
        new_contact = Contact(name, phone, email)
        self.contacts.append(new_contact)
        self.size += 1
        return True
    
    def search(self, name: str) -> Optional[Contact]:
        search_name = name.strip().lower()
        for contact in self.contacts:
            if contact.name == search_name:
                return contact
        return None
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        contact = self.search(name)
        if contact is None:
            return False
        
        if phone is not None:
            contact.phone = phone.strip()
        if email is not None:
            contact.email = email.strip().lower()
            
        return True
    
    def delete(self, name: str) -> bool:
        search_name = name.strip().lower()
        for i, contact in enumerate(self.contacts):
            if contact.name == search_name:
                del self.contacts[i]  # O(n) operation due to shifting elements
                self.size -= 1
                return True
        return False
    
    def list_all_contacts(self, sorted_by_name: bool = False) -> List[Contact]:
        if sorted_by_name:
            return sorted(self.contacts, key=lambda x: x.name)
        return self.contacts.copy()
    
    