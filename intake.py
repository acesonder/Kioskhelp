"""
Intake Assessment Module
Handles initial client intake and needs assessment
"""

import datetime
from typing import Dict, List


class IntakeAssessment:
    """Manages client intake process and initial assessment"""
    
    def __init__(self):
        self.assessments = {}
        self.intake_questions = self._initialize_intake_questions()
    
    def _initialize_intake_questions(self) -> List[Dict]:
        """Initialize standard intake questions"""
        return [
            {
                'id': 'housing_status',
                'category': 'housing',
                'question': 'What is your current housing situation?',
                'type': 'multiple_choice',
                'options': [
                    'Stable housing',
                    'Temporary housing',
                    'Homeless',
                    'At risk of homelessness',
                    'Prefer not to say'
                ],
                'priority': 'high'
            },
            {
                'id': 'food_security',
                'category': 'food_security',
                'question': 'Do you have reliable access to nutritious food?',
                'type': 'yes_no',
                'priority': 'high'
            },
            {
                'id': 'healthcare_access',
                'category': 'healthcare',
                'question': 'Do you have access to healthcare services?',
                'type': 'yes_no',
                'priority': 'high'
            },
            {
                'id': 'mental_health_support',
                'category': 'mental_health',
                'question': 'Are you currently receiving mental health support?',
                'type': 'yes_no',
                'priority': 'medium'
            },
            {
                'id': 'employment_status',
                'category': 'employment',
                'question': 'What is your current employment status?',
                'type': 'multiple_choice',
                'options': [
                    'Employed full-time',
                    'Employed part-time',
                    'Unemployed',
                    'Unable to work',
                    'Student',
                    'Retired'
                ],
                'priority': 'medium'
            },
            {
                'id': 'legal_issues',
                'category': 'legal_support',
                'question': 'Do you need legal assistance?',
                'type': 'yes_no',
                'priority': 'medium'
            },
            {
                'id': 'transportation',
                'category': 'transportation',
                'question': 'Do you have reliable transportation?',
                'type': 'yes_no',
                'priority': 'low'
            },
            {
                'id': 'immediate_needs',
                'category': 'general',
                'question': 'What are your most immediate needs? (Select all that apply)',
                'type': 'checkbox',
                'options': [
                    'Shelter',
                    'Food',
                    'Medical care',
                    'Mental health services',
                    'Employment',
                    'Legal help',
                    'Transportation',
                    'Financial assistance',
                    'Education/Training'
                ],
                'priority': 'high'
            }
        ]
    
    def start_intake(self, client_id: str) -> Dict:
        """
        Start intake assessment for a client
        
        Args:
            client_id: Unique client identifier
            
        Returns:
            Dictionary with intake session information
        """
        intake_id = f"intake_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.assessments[intake_id] = {
            'intake_id': intake_id,
            'client_id': client_id,
            'start_time': datetime.datetime.now().isoformat(),
            'status': 'in_progress',
            'responses': {},
            'current_question': 0
        }
        
        return {
            'success': True,
            'intake_id': intake_id,
            'questions': self.intake_questions,
            'message': 'Intake assessment started'
        }
    
    def record_response(self, intake_id: str, question_id: str, response: any) -> Dict:
        """
        Record client response to intake question
        
        Args:
            intake_id: Unique intake session identifier
            question_id: Question identifier
            response: Client's response
            
        Returns:
            Dictionary with recording result
        """
        if intake_id not in self.assessments:
            return {
                'success': False,
                'message': 'Intake session not found'
            }
        
        self.assessments[intake_id]['responses'][question_id] = {
            'response': response,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'message': 'Response recorded'
        }
    
    def complete_intake(self, intake_id: str) -> Dict:
        """
        Complete intake assessment and generate summary
        
        Args:
            intake_id: Unique intake session identifier
            
        Returns:
            Dictionary with intake summary and recommendations
        """
        if intake_id not in self.assessments:
            return {
                'success': False,
                'message': 'Intake session not found'
            }
        
        assessment = self.assessments[intake_id]
        assessment['status'] = 'completed'
        assessment['end_time'] = datetime.datetime.now().isoformat()
        
        # Analyze responses to identify priority needs
        priority_needs = self._analyze_needs(assessment['responses'])
        
        return {
            'success': True,
            'intake_id': intake_id,
            'priority_needs': priority_needs,
            'completion_time': assessment['end_time'],
            'message': 'Intake assessment completed'
        }
    
    def _analyze_needs(self, responses: Dict) -> List[str]:
        """
        Analyze intake responses to identify priority needs
        
        Args:
            responses: Dictionary of question responses
            
        Returns:
            List of priority need categories
        """
        priority_needs = []
        
        # Housing assessment
        if 'housing_status' in responses:
            housing = responses['housing_status']['response']
            if housing in ['Homeless', 'At risk of homelessness', 'Temporary housing']:
                priority_needs.append('housing')
        
        # Food security
        if 'food_security' in responses:
            if responses['food_security']['response'] in ['No', 'no', False]:
                priority_needs.append('food_security')
        
        # Healthcare access
        if 'healthcare_access' in responses:
            if responses['healthcare_access']['response'] in ['No', 'no', False]:
                priority_needs.append('healthcare')
        
        # Mental health support
        if 'mental_health_support' in responses:
            if responses['mental_health_support']['response'] in ['No', 'no', False]:
                priority_needs.append('mental_health')
        
        # Immediate needs
        if 'immediate_needs' in responses:
            immediate = responses['immediate_needs']['response']
            if isinstance(immediate, list):
                for need in immediate:
                    category = self._map_immediate_need_to_category(need)
                    if category and category not in priority_needs:
                        priority_needs.append(category)
        
        return priority_needs
    
    def _map_immediate_need_to_category(self, need: str) -> str:
        """Map immediate need to assessment category"""
        mapping = {
            'Shelter': 'housing',
            'Food': 'food_security',
            'Medical care': 'healthcare',
            'Mental health services': 'mental_health',
            'Employment': 'employment',
            'Legal help': 'legal_support',
            'Transportation': 'transportation',
            'Financial assistance': 'financial',
            'Education/Training': 'education'
        }
        return mapping.get(need, '')
    
    def get_intake_summary(self, intake_id: str) -> Dict:
        """Get summary of completed intake assessment"""
        if intake_id not in self.assessments:
            return {
                'success': False,
                'message': 'Intake session not found'
            }
        
        return self.assessments[intake_id]
