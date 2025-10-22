"""
Client Assessment Module
Handles detailed client needs assessment and questionnaires
"""

import datetime
from typing import Dict, List, Optional


class ClientAssessment:
    """Comprehensive client assessment system"""
    
    def __init__(self):
        self.assessments = {}
        self.assessment_templates = self._initialize_assessment_templates()
    
    def _initialize_assessment_templates(self) -> Dict:
        """Initialize assessment question templates by category"""
        return {
            'housing': {
                'name': 'Housing Needs Assessment',
                'questions': [
                    {
                        'id': 'current_situation',
                        'text': 'Describe your current living situation',
                        'type': 'text'
                    },
                    {
                        'id': 'housing_stability',
                        'text': 'How long have you been in your current housing?',
                        'type': 'multiple_choice',
                        'options': ['Less than 1 month', '1-6 months', '6-12 months', 'Over 1 year']
                    },
                    {
                        'id': 'safety_concerns',
                        'text': 'Do you have any safety concerns in your current housing?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'affordability',
                        'text': 'Are you able to afford your current housing?',
                        'type': 'yes_no'
                    }
                ]
            },
            'mental_health': {
                'name': 'Mental Health Assessment',
                'questions': [
                    {
                        'id': 'current_support',
                        'text': 'Are you currently working with a mental health professional?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'medication',
                        'text': 'Are you taking any medications for mental health?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'support_interest',
                        'text': 'Would you be interested in mental health support services?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'crisis_support',
                        'text': 'Do you need immediate crisis support?',
                        'type': 'yes_no',
                        'priority': 'critical'
                    }
                ]
            },
            'employment': {
                'name': 'Employment Assessment',
                'questions': [
                    {
                        'id': 'work_history',
                        'text': 'Do you have previous work experience?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'job_search',
                        'text': 'Are you currently looking for work?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'barriers',
                        'text': 'What barriers do you face in finding employment?',
                        'type': 'checkbox',
                        'options': [
                            'Lack of transportation',
                            'Childcare needs',
                            'Health issues',
                            'Criminal record',
                            'Lack of education/training',
                            'Language barriers',
                            'No barriers'
                        ]
                    },
                    {
                        'id': 'training_interest',
                        'text': 'Would you be interested in job training programs?',
                        'type': 'yes_no'
                    }
                ]
            },
            'healthcare': {
                'name': 'Healthcare Access Assessment',
                'questions': [
                    {
                        'id': 'insurance',
                        'text': 'Do you have health insurance?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'primary_care',
                        'text': 'Do you have a primary care physician?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'ongoing_conditions',
                        'text': 'Do you have any ongoing health conditions?',
                        'type': 'yes_no'
                    },
                    {
                        'id': 'medication_access',
                        'text': 'Can you afford your medications?',
                        'type': 'yes_no'
                    }
                ]
            }
        }
    
    def create_assessment(self, client_id: str, categories: List[str]) -> Dict:
        """
        Create a new assessment for a client
        
        Args:
            client_id: Unique client identifier
            categories: List of assessment categories to include
            
        Returns:
            Dictionary with assessment information
        """
        assessment_id = f"assess_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        questions = []
        for category in categories:
            if category in self.assessment_templates:
                template = self.assessment_templates[category]
                for q in template['questions']:
                    questions.append({
                        'category': category,
                        'question': q
                    })
        
        self.assessments[assessment_id] = {
            'assessment_id': assessment_id,
            'client_id': client_id,
            'categories': categories,
            'questions': questions,
            'responses': {},
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'active'
        }
        
        return {
            'success': True,
            'assessment_id': assessment_id,
            'questions': questions,
            'message': 'Assessment created successfully'
        }
    
    def submit_response(self, assessment_id: str, question_id: str, 
                       category: str, response: any) -> Dict:
        """
        Submit response to an assessment question
        
        Args:
            assessment_id: Unique assessment identifier
            question_id: Question identifier
            category: Question category
            response: Client's response
            
        Returns:
            Dictionary with submission result
        """
        if assessment_id not in self.assessments:
            return {
                'success': False,
                'message': 'Assessment not found'
            }
        
        key = f"{category}_{question_id}"
        self.assessments[assessment_id]['responses'][key] = {
            'question_id': question_id,
            'category': category,
            'response': response,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'message': 'Response recorded'
        }
    
    def complete_assessment(self, assessment_id: str) -> Dict:
        """
        Complete assessment and generate results
        
        Args:
            assessment_id: Unique assessment identifier
            
        Returns:
            Dictionary with assessment results and recommendations
        """
        if assessment_id not in self.assessments:
            return {
                'success': False,
                'message': 'Assessment not found'
            }
        
        assessment = self.assessments[assessment_id]
        assessment['status'] = 'completed'
        assessment['completed_at'] = datetime.datetime.now().isoformat()
        
        # Analyze responses and generate insights
        insights = self._generate_insights(assessment)
        
        return {
            'success': True,
            'assessment_id': assessment_id,
            'insights': insights,
            'recommended_services': insights.get('services', []),
            'priority_level': insights.get('priority', 'medium'),
            'message': 'Assessment completed successfully'
        }
    
    def _generate_insights(self, assessment: Dict) -> Dict:
        """
        Generate insights from assessment responses
        
        Args:
            assessment: Assessment data
            
        Returns:
            Dictionary with insights and recommendations
        """
        responses = assessment['responses']
        categories = assessment['categories']
        
        insights = {
            'needs_identified': [],
            'services': [],
            'priority': 'low',
            'critical_flags': []
        }
        
        # Check for critical needs
        for key, response_data in responses.items():
            if response_data.get('question_id') == 'crisis_support':
                if response_data['response'] in ['Yes', 'yes', True]:
                    insights['critical_flags'].append('mental_health_crisis')
                    insights['priority'] = 'critical'
                    insights['services'].append('crisis_counseling')
        
        # Analyze housing needs
        if 'housing' in categories:
            housing_stable = self._check_response(responses, 'housing_stability')
            housing_affordable = self._check_response(responses, 'affordability')
            
            if not housing_stable or not housing_affordable:
                insights['needs_identified'].append('housing_support')
                insights['services'].append('housing_assistance')
                if insights['priority'] != 'critical':
                    insights['priority'] = 'high'
        
        # Analyze employment needs
        if 'employment' in categories:
            job_search = self._check_response(responses, 'job_search')
            training_interest = self._check_response(responses, 'training_interest')
            
            if job_search or training_interest:
                insights['needs_identified'].append('employment_support')
                insights['services'].extend(['job_placement', 'skills_training'])
        
        # Analyze healthcare needs
        if 'healthcare' in categories:
            has_insurance = self._check_response(responses, 'insurance')
            
            if not has_insurance:
                insights['needs_identified'].append('healthcare_access')
                insights['services'].append('health_insurance_enrollment')
        
        return insights
    
    def _check_response(self, responses: Dict, question_id: str) -> bool:
        """Check if a response indicates a positive answer"""
        for key, response_data in responses.items():
            if response_data.get('question_id') == question_id:
                response = response_data['response']
                return response in ['Yes', 'yes', True]
        return False
    
    def get_assessment_results(self, assessment_id: str) -> Optional[Dict]:
        """Retrieve assessment results"""
        return self.assessments.get(assessment_id)
