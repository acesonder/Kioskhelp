"""
Consent Management Module
Handles client consent for data processing and service provision
"""

import datetime
from typing import Dict, List


class ConsentManager:
    """Manages client consent and permissions"""
    
    CONSENT_TYPES = [
        'data_processing',
        'data_sharing',
        'service_referral',
        'communication',
        'case_management',
        'research_participation'
    ]
    
    def __init__(self):
        self.consents = {}
    
    def record_consent(self, client_id: str, consent_data: Dict) -> Dict:
        """
        Record client consent
        
        Args:
            client_id: Unique client identifier
            consent_data: Dictionary containing consent information
                - consent_type: Type of consent
                - granted: Boolean indicating consent status
                - notes: Optional notes
                
        Returns:
            Dictionary with consent recording result
        """
        if client_id not in self.consents:
            self.consents[client_id] = []
        
        consent_record = {
            'consent_id': f"consent_{len(self.consents[client_id]) + 1}",
            'consent_type': consent_data.get('consent_type'),
            'granted': consent_data.get('granted', False),
            'timestamp': datetime.datetime.now().isoformat(),
            'notes': consent_data.get('notes', ''),
            'version': '1.0'
        }
        
        self.consents[client_id].append(consent_record)
        
        return {
            'success': True,
            'consent_id': consent_record['consent_id'],
            'message': 'Consent recorded successfully'
        }
    
    def get_client_consents(self, client_id: str) -> List[Dict]:
        """Retrieve all consents for a client"""
        return self.consents.get(client_id, [])
    
    def check_consent(self, client_id: str, consent_type: str) -> bool:
        """
        Check if client has granted specific consent
        
        Args:
            client_id: Unique client identifier
            consent_type: Type of consent to check
            
        Returns:
            Boolean indicating whether consent is granted
        """
        client_consents = self.consents.get(client_id, [])
        
        # Find most recent consent of this type
        relevant_consents = [
            c for c in client_consents 
            if c['consent_type'] == consent_type
        ]
        
        if not relevant_consents:
            return False
        
        # Return most recent consent status
        return relevant_consents[-1]['granted']
    
    def revoke_consent(self, client_id: str, consent_type: str) -> Dict:
        """
        Revoke a specific consent
        
        Args:
            client_id: Unique client identifier
            consent_type: Type of consent to revoke
            
        Returns:
            Dictionary with revocation result
        """
        consent_record = {
            'consent_type': consent_type,
            'granted': False,
            'notes': 'Consent revoked by client'
        }
        
        return self.record_consent(client_id, consent_record)
    
    def get_consent_summary(self, client_id: str) -> Dict:
        """Get summary of all client consents"""
        consents = self.get_client_consents(client_id)
        
        summary = {}
        for consent_type in self.CONSENT_TYPES:
            summary[consent_type] = self.check_consent(client_id, consent_type)
        
        return {
            'client_id': client_id,
            'consents': summary,
            'total_consents': len(consents),
            'last_updated': consents[-1]['timestamp'] if consents else None
        }
