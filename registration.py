"""
Client Registration Module
Handles new and existing client registration with privacy and security
"""

import datetime
import hashlib
import uuid
from typing import Dict, Optional


class ClientRegistration:
    """Manages client registration process"""
    
    def __init__(self):
        self.clients = {}
    
    def generate_client_id(self, email: Optional[str] = None) -> str:
        """Generate unique client ID"""
        if email:
            # Hash email for privacy
            return hashlib.sha256(email.encode()).hexdigest()[:16]
        else:
            # Anonymous client ID
            return str(uuid.uuid4())[:16]
    
    def register_new_client(self, data: Dict) -> Dict:
        """
        Register a new client
        
        Args:
            data: Dictionary containing client information
                - email (optional): Client email
                - name (optional): Client name
                - phone (optional): Phone number
                - anonymous (bool): Whether to register anonymously
                
        Returns:
            Dictionary with registration result
        """
        client_id = self.generate_client_id(data.get('email'))
        
        client_record = {
            'client_id': client_id,
            'registration_date': datetime.datetime.now().isoformat(),
            'is_anonymous': data.get('anonymous', False),
            'status': 'active'
        }
        
        # Store only non-sensitive data
        if not data.get('anonymous'):
            client_record['name'] = data.get('name', '')
            client_record['contact_preference'] = data.get('contact_preference', 'email')
        
        self.clients[client_id] = client_record
        
        return {
            'success': True,
            'client_id': client_id,
            'message': 'Registration successful'
        }
    
    def get_existing_client(self, client_id: str) -> Optional[Dict]:
        """Retrieve existing client information"""
        return self.clients.get(client_id)
    
    def update_client(self, client_id: str, data: Dict) -> Dict:
        """Update existing client information"""
        if client_id not in self.clients:
            return {
                'success': False,
                'message': 'Client not found'
            }
        
        self.clients[client_id].update(data)
        self.clients[client_id]['last_updated'] = datetime.datetime.now().isoformat()
        
        return {
            'success': True,
            'message': 'Client information updated'
        }


class ClientVerification:
    """Handles client identity verification for returning clients"""
    
    @staticmethod
    def verify_by_id(client_id: str, verification_code: str) -> bool:
        """Verify client identity using ID and verification code"""
        # In production, this would check against secure storage
        return len(verification_code) >= 6
    
    @staticmethod
    def send_verification_code(contact: str, method: str = 'email') -> Dict:
        """Send verification code to client"""
        # In production, this would integrate with email/SMS service
        verification_code = str(uuid.uuid4())[:6].upper()
        
        return {
            'success': True,
            'message': f'Verification code sent via {method}',
            'code': verification_code  # In production, don't return this
        }
