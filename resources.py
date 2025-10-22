"""
Resource Access Module
Provides access to community resources and educational materials
"""

import datetime
from typing import Dict, List, Optional


class Resource:
    """Represents a community resource"""
    
    def __init__(self, resource_id: str, title: str, category: str, 
                 description: str, content_type: str, url: Optional[str] = None):
        self.resource_id = resource_id
        self.title = title
        self.category = category
        self.description = description
        self.content_type = content_type  # article, video, guide, form, link
        self.url = url
        self.created_at = datetime.datetime.now().isoformat()


class ResourceLibrary:
    """Manages community resources and educational materials"""
    
    def __init__(self):
        self.resources = self._initialize_resources()
        self.access_log = {}
    
    def _initialize_resources(self) -> Dict[str, Resource]:
        """Initialize resource library"""
        return {
            'res_001': Resource(
                resource_id='res_001',
                title='Understanding Your Rights to Housing',
                category='housing',
                description='Comprehensive guide to tenant rights and housing assistance programs',
                content_type='guide',
                url='https://resources.example.org/housing-rights'
            ),
            'res_002': Resource(
                resource_id='res_002',
                title='Food Assistance Programs in Your Area',
                category='food_security',
                description='Directory of food banks, meal programs, and nutrition assistance',
                content_type='article',
                url='https://resources.example.org/food-assistance'
            ),
            'res_003': Resource(
                resource_id='res_003',
                title='Mental Health Crisis Resources',
                category='mental_health',
                description='Immediate help and crisis intervention services',
                content_type='guide',
                url='https://resources.example.org/crisis-help'
            ),
            'res_004': Resource(
                resource_id='res_004',
                title='Resume Building Workshop',
                category='employment',
                description='Video series on creating effective resumes and cover letters',
                content_type='video',
                url='https://resources.example.org/resume-workshop'
            ),
            'res_005': Resource(
                resource_id='res_005',
                title='Healthcare Enrollment Guide',
                category='healthcare',
                description='Step-by-step guide to enrolling in health insurance programs',
                content_type='guide',
                url='https://resources.example.org/healthcare-enrollment'
            ),
            'res_006': Resource(
                resource_id='res_006',
                title='Legal Aid Application Form',
                category='legal_support',
                description='Application form for free legal assistance',
                content_type='form',
                url='https://resources.example.org/legal-aid-form'
            ),
            'res_007': Resource(
                resource_id='res_007',
                title='Budgeting and Financial Planning',
                category='financial',
                description='Tools and guides for managing personal finances',
                content_type='article',
                url='https://resources.example.org/budgeting'
            ),
            'res_008': Resource(
                resource_id='res_008',
                title='Parenting Support Resources',
                category='family_services',
                description='Resources for parents and caregivers',
                content_type='guide',
                url='https://resources.example.org/parenting'
            ),
            'res_009': Resource(
                resource_id='res_009',
                title='Job Training Programs',
                category='employment',
                description='Information about available job training and certification programs',
                content_type='article',
                url='https://resources.example.org/job-training'
            ),
            'res_010': Resource(
                resource_id='res_010',
                title='Understanding Medicaid and Medicare',
                category='healthcare',
                description='Guide to public health insurance programs',
                content_type='guide',
                url='https://resources.example.org/medicaid-medicare'
            )
        }
    
    def search_resources(self, category: Optional[str] = None, 
                        keyword: Optional[str] = None) -> List[Dict]:
        """
        Search for resources by category or keyword
        
        Args:
            category: Resource category
            keyword: Search keyword
            
        Returns:
            List of matching resources
        """
        results = []
        
        for resource in self.resources.values():
            # Filter by category if provided
            if category and resource.category != category:
                continue
            
            # Filter by keyword if provided
            if keyword:
                keyword_lower = keyword.lower()
                if (keyword_lower not in resource.title.lower() and
                    keyword_lower not in resource.description.lower()):
                    continue
            
            results.append({
                'resource_id': resource.resource_id,
                'title': resource.title,
                'category': resource.category,
                'description': resource.description,
                'content_type': resource.content_type
            })
        
        return results
    
    def get_resource(self, resource_id: str) -> Optional[Dict]:
        """Get detailed information about a specific resource"""
        if resource_id not in self.resources:
            return None
        
        resource = self.resources[resource_id]
        
        return {
            'resource_id': resource.resource_id,
            'title': resource.title,
            'category': resource.category,
            'description': resource.description,
            'content_type': resource.content_type,
            'url': resource.url,
            'created_at': resource.created_at
        }
    
    def log_resource_access(self, client_id: str, resource_id: str) -> Dict:
        """
        Log when a client accesses a resource
        
        Args:
            client_id: Unique client identifier
            resource_id: Resource identifier
            
        Returns:
            Dictionary with logging result
        """
        if resource_id not in self.resources:
            return {
                'success': False,
                'message': 'Resource not found'
            }
        
        if client_id not in self.access_log:
            self.access_log[client_id] = []
        
        access_record = {
            'resource_id': resource_id,
            'accessed_at': datetime.datetime.now().isoformat()
        }
        
        self.access_log[client_id].append(access_record)
        
        return {
            'success': True,
            'message': 'Resource access logged'
        }
    
    def get_client_history(self, client_id: str) -> List[Dict]:
        """Get resource access history for a client"""
        if client_id not in self.access_log:
            return []
        
        history = []
        for access in self.access_log[client_id]:
            resource = self.resources.get(access['resource_id'])
            if resource:
                history.append({
                    'resource_id': resource.resource_id,
                    'title': resource.title,
                    'category': resource.category,
                    'accessed_at': access['accessed_at']
                })
        
        return history
    
    def get_recommended_resources(self, needs: List[str]) -> List[Dict]:
        """
        Get recommended resources based on client needs
        
        Args:
            needs: List of need categories
            
        Returns:
            List of recommended resources
        """
        recommendations = []
        
        for need in needs:
            category_resources = self.search_resources(category=need)
            recommendations.extend(category_resources)
        
        # Remove duplicates
        seen = set()
        unique_recommendations = []
        for resource in recommendations:
            if resource['resource_id'] not in seen:
                seen.add(resource['resource_id'])
                unique_recommendations.append(resource)
        
        return unique_recommendations
    
    def get_all_categories(self) -> List[str]:
        """Get list of all resource categories"""
        categories = set()
        for resource in self.resources.values():
            categories.add(resource.category)
        return sorted(list(categories))
