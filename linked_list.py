from typing import List, Optional
from helper import Contact

class ListNode:
    def __init__(self, contact: Contact):
        self.contact = contact
        self.next: Optional['ListNode'] = None

class LinkedListImpl:
    def __init__(self):
        self.head: Optional[ListNode] = None
        self.size = 0
    
    def insert(self, name: str, phone: str, email: str) -> bool:
        if self.search(name) is not None:
            return False
        
        new_contact = Contact(name, phone, email)
        new_node = ListNode(new_contact)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return True
    
    def search(self, name: str) -> Optional[Contact]:
        search_name = name.strip().lower()
        current = self.head
        while current:
            if current.contact.name == search_name:
                return current.contact
            current = current.next
        return None
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        search_name = name.strip().lower()
        current = self.head
        while current:
            if current.contact.name == search_name:
                if phone is not None:
                    current.contact.phone = phone.strip()
                if email is not None:
                    current.contact.email = email.strip().lower()
                return True
            current = current.next
        return False
    
    def delete(self, name: str) -> bool:
        search_name = name.strip().lower()
        
        # Handle empty list
        if not self.head:
            return False
        
        # Handle deletion of head node
        if self.head.contact.name == search_name:
            self.head = self.head.next
            self.size -= 1
            return True
        
        # Handle deletion of other nodes
        current = self.head
        while current.next:
            if current.next.contact.name == search_name:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def list_all_contacts(self, sorted_by_name: bool = False) -> List[Contact]:
        contacts = []
        current = self.head
        while current:
            contacts.append(current.contact)
            current = current.next
        
        if sorted_by_name:
            return sorted(contacts, key=lambda x: x.name)
        return contacts
