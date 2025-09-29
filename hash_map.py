from typing import List, Optional, Dict
from helper import Contact

class HashMapImpl:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}
        self.size = 0
    
    def insert(self, name: str, phone: str, email: str) -> bool:
        search_name = name.strip().lower()
        if search_name in self.contacts:
            return False
        
        new_contact = Contact(name, phone, email)
        self.contacts[search_name] = new_contact
        self.size += 1
        return True
    
    def search(self, name: str) -> Optional[Contact]:
        search_name = name.strip().lower()
        return self.contacts.get(search_name)
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        search_name = name.strip().lower()
        contact = self.contacts.get(search_name)
        if contact is None:
            return False
        
        if phone is not None:
            contact.phone = phone.strip()
        if email is not None:
            contact.email = email.strip().lower()
            
        return True
    
    def delete(self, name: str) -> bool:
        search_name = name.strip().lower()
        if search_name in self.contacts:
            del self.contacts[search_name]
            self.size -= 1
            return True
        return False
    
    def list_all_contacts(self, sorted_by_name: bool = False) -> List[Contact]:
        contacts = list(self.contacts.values())
        if sorted_by_name:
            return sorted(contacts, key=lambda x: x.name)
        return contacts