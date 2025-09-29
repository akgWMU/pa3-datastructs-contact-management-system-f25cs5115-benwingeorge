from typing import List, Optional
from helper import Contact

class BSTNode:
    def __init__(self, contact: Contact):
        self.contact = contact
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BstImpl:
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.size = 0
    
    def insert(self, name: str, phone: str, email: str) -> bool:
        if self.search(name) is not None:
            return False
        
        new_contact = Contact(name, phone, email)
        self.root = self._insert_recursive(self.root, new_contact)
        self.size += 1
        return True
    
    def _insert_recursive(self, node: Optional[BSTNode], contact: Contact) -> BSTNode:
        if node is None:
            return BSTNode(contact)
        
        if contact.name < node.contact.name:
            node.left = self._insert_recursive(node.left, contact)
        else:
            node.right = self._insert_recursive(node.right, contact)
        
        return node
    
    def search(self, name: str) -> Optional[Contact]:
        search_name = name.strip().lower()
        return self._search_recursive(self.root, search_name)
    
    def _search_recursive(self, node: Optional[BSTNode], name: str) -> Optional[Contact]:
        if node is None:
            return None
        
        if name == node.contact.name:
            return node.contact
        elif name < node.contact.name:
            return self._search_recursive(node.left, name)
        else:
            return self._search_recursive(node.right, name)
    
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
        if self.search(name) is None:
            return False
        
        self.root = self._delete_recursive(self.root, search_name)
        self.size -= 1
        return True
    
    def _delete_recursive(self, node: Optional[BSTNode], name: str) -> Optional[BSTNode]:
        if node is None:
            return None
        
        if name < node.contact.name:
            node.left = self._delete_recursive(node.left, name)
        elif name > node.contact.name:
            node.right = self._delete_recursive(node.right, name)
        else:
            # Node to delete found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Node has two children - find inorder successor
                successor = self._find_min(node.right)
                node.contact = successor.contact
                node.right = self._delete_recursive(node.right, successor.contact.name)
        
        return node
    
    def _find_min(self, node: BSTNode) -> BSTNode:
        while node.left:
            node = node.left
        return node
    
    def list_all_contacts(self, sorted_by_name: bool = False) -> List[Contact]:
        contacts = []
        self._inorder_traversal(self.root, contacts)
        
        if not sorted_by_name:
            # BST naturally returns sorted order, so shuffle if not sorted requested
            return contacts
        return contacts
    
    def _inorder_traversal(self, node: Optional[BSTNode], contacts: List[Contact]) -> None:
        if node:
            self._inorder_traversal(node.left, contacts)
            contacts.append(node.contact)
            self._inorder_traversal(node.right, contacts)