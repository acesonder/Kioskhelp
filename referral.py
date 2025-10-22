"""
Referral System Module
Manages referrals to service providers based on client needs
"""

import datetime
from typing import Dict, List, Optional


class ServiceProvider:
    """Service provider information"""
    
    def __init__(self, provider_id: str, name: str, services: List[str], 
                 contact: Dict, capacity: str = 'available'):
        self.provider_id = provider_id
        self.name = name
        self.services = services
        self.contact = contact
        self.capacity = capacity


class ReferralSystem:
    """Manages client referrals to service providers"""
    
    def __init__(self):
        self.referrals = {}
        self.providers = self._initialize_providers()
    
    def _initialize_providers(self) -> Dict[str, ServiceProvider]:
        """Initialize service provider directory"""
        return {
            'housing_001': ServiceProvider(
                provider_id='housing_001',
                name='City Housing Services',
                services=['emergency_shelter', 'transitional_housing', 'permanent_housing'],
                contact={'phone': '555-0101', 'email': 'housing@cityservices.org'}
            ),
            'food_001': ServiceProvider(
                provider_id='food_001',
                name='Community Food Bank',
                services=['food_pantry', 'meal_programs', 'nutrition_education'],
                contact={'phone': '555-0102', 'email': 'info@foodbank.org'}
            ),
            'health_001': ServiceProvider(
                provider_id='health_001',
                name='Community Health Clinic',
                services=['primary_care', 'mental_health', 'dental_care', 'prescriptions'],
                contact={'phone': '555-0103', 'email': 'appointments@healthclinic.org'}
            ),
            'mental_001': ServiceProvider(
                provider_id='mental_001',
                name='Mental Health Support Center',
                services=['counseling', 'crisis_intervention', 'support_groups'],
                contact={'phone': '555-0104', 'email': 'support@mentalhealth.org', 
                        'crisis_line': '555-CRISIS'}
            ),
            'employment_001': ServiceProvider(
                provider_id='employment_001',
                name='Workforce Development Center',
                services=['job_placement', 'skills_training', 'resume_help', 'interview_prep'],
                contact={'phone': '555-0105', 'email': 'jobs@workforce.org'}
            ),
            'legal_001': ServiceProvider(
                provider_id='legal_001',
                name='Legal Aid Society',
                services=['legal_consultation', 'court_assistance', 'document_help'],
                contact={'phone': '555-0106', 'email': 'help@legalaid.org'}
            ),
            'family_001': ServiceProvider(
                provider_id='family_001',
                name='Family Services Center',
                services=['childcare', 'parenting_classes', 'family_counseling'],
                contact={'phone': '555-0107', 'email': 'info@familyservices.org'}
            )
        }
    
    def find_providers_for_need(self, need_category: str) -> List[ServiceProvider]:
        """
        Find service providers that can address a specific need
        
        Args:
            need_category: Category of need (housing, food_security, etc.)
            
        Returns:
            List of matching service providers
        """
        need_to_service_mapping = {
            'housing': ['emergency_shelter', 'transitional_housing', 'permanent_housing'],
            'food_security': ['food_pantry', 'meal_programs'],
            'healthcare': ['primary_care', 'dental_care', 'prescriptions'],
            'mental_health': ['counseling', 'crisis_intervention', 'mental_health'],
            'employment': ['job_placement', 'skills_training'],
            'legal_support': ['legal_consultation', 'court_assistance'],
            'family_services': ['childcare', 'parenting_classes', 'family_counseling']
        }
        
        target_services = need_to_service_mapping.get(need_category, [])
        matching_providers = []
        
        for provider in self.providers.values():
            if any(service in provider.services for service in target_services):
                matching_providers.append(provider)
        
        return matching_providers
    
    def create_referral(self, client_id: str, need_category: str, 
                       priority: str = 'medium', notes: str = '') -> Dict:
        """
        Create a referral for a client
        
        Args:
            client_id: Unique client identifier
            need_category: Category of need
            priority: Referral priority (low, medium, high, critical)
            notes: Additional notes about the referral
            
        Returns:
            Dictionary with referral information
        """
        # Find appropriate providers
        providers = self.find_providers_for_need(need_category)
        
        if not providers:
            return {
                'success': False,
                'message': f'No providers found for {need_category}'
            }
        
        # Create referral
        referral_id = f"ref_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        referral = {
            'referral_id': referral_id,
            'client_id': client_id,
            'need_category': need_category,
            'priority': priority,
            'providers': [p.provider_id for p in providers],
            'status': 'pending',
            'created_at': datetime.datetime.now().isoformat(),
            'notes': notes
        }
        
        self.referrals[referral_id] = referral
        
        return {
            'success': True,
            'referral_id': referral_id,
            'providers': [{
                'name': p.name,
                'contact': p.contact,
                'services': p.services
            } for p in providers],
            'message': 'Referral created successfully'
        }
    
    def create_multiple_referrals(self, client_id: str, 
                                 needs: List[str], priority: str = 'medium') -> Dict:
        """
        Create multiple referrals based on client needs
        
        Args:
            client_id: Unique client identifier
            needs: List of need categories
            priority: Overall priority level
            
        Returns:
            Dictionary with all created referrals
        """
        referrals = []
        
        for need in needs:
            result = self.create_referral(client_id, need, priority)
            if result['success']:
                referrals.append(result)
        
        return {
            'success': True,
            'referrals': referrals,
            'total_referrals': len(referrals),
            'message': f'Created {len(referrals)} referrals'
        }
    
    def update_referral_status(self, referral_id: str, status: str, 
                              notes: str = '') -> Dict:
        """
        Update referral status
        
        Args:
            referral_id: Unique referral identifier
            status: New status (pending, contacted, scheduled, completed, cancelled)
            notes: Update notes
            
        Returns:
            Dictionary with update result
        """
        if referral_id not in self.referrals:
            return {
                'success': False,
                'message': 'Referral not found'
            }
        
        self.referrals[referral_id]['status'] = status
        self.referrals[referral_id]['updated_at'] = datetime.datetime.now().isoformat()
        
        if notes:
            if 'status_history' not in self.referrals[referral_id]:
                self.referrals[referral_id]['status_history'] = []
            
            self.referrals[referral_id]['status_history'].append({
                'status': status,
                'notes': notes,
                'timestamp': datetime.datetime.now().isoformat()
            })
        
        return {
            'success': True,
            'message': f'Referral status updated to {status}'
        }
    
    def get_client_referrals(self, client_id: str) -> List[Dict]:
        """Get all referrals for a client"""
        client_referrals = [
            ref for ref in self.referrals.values() 
            if ref['client_id'] == client_id
        ]
        return client_referrals
    
    def get_referral_details(self, referral_id: str) -> Optional[Dict]:
        """Get detailed information about a referral"""
        if referral_id not in self.referrals:
            return None
        
        referral = self.referrals[referral_id].copy()
        
        # Add provider details
        provider_details = []
        for provider_id in referral['providers']:
            if provider_id in self.providers:
                provider = self.providers[provider_id]
                provider_details.append({
                    'id': provider.provider_id,
                    'name': provider.name,
                    'services': provider.services,
                    'contact': provider.contact,
                    'capacity': provider.capacity
                })
        
        referral['provider_details'] = provider_details
        
        return referral
