"""
Smart Case Management Module
Manages client cases with intelligent tracking and coordination
"""

import datetime
from typing import Dict, List, Optional
from enum import Enum


class CaseStatus(Enum):
    """Case status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class CasePriority(Enum):
    """Case priority enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CaseManager:
    """Smart case management system"""
    
    def __init__(self):
        self.cases = {}
        self.case_notes = {}
        self.case_activities = {}
    
    def create_case(self, client_id: str, needs: List[str], 
                   priority: str = 'medium', description: str = '') -> Dict:
        """
        Create a new case for a client
        
        Args:
            client_id: Unique client identifier
            needs: List of identified needs
            priority: Case priority level
            description: Case description
            
        Returns:
            Dictionary with case information
        """
        case_id = f"case_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        case = {
            'case_id': case_id,
            'client_id': client_id,
            'needs': needs,
            'priority': priority,
            'description': description,
            'status': CaseStatus.OPEN.value,
            'created_at': datetime.datetime.now().isoformat(),
            'assigned_services': [],
            'goals': [],
            'progress_metrics': {}
        }
        
        self.cases[case_id] = case
        self.case_activities[case_id] = []
        
        # Log case creation
        self._log_activity(case_id, 'case_created', 
                          f'Case created with priority: {priority}')
        
        return {
            'success': True,
            'case_id': case_id,
            'case': case,
            'message': 'Case created successfully'
        }
    
    def update_case_status(self, case_id: str, status: str, 
                          notes: str = '') -> Dict:
        """
        Update case status
        
        Args:
            case_id: Unique case identifier
            status: New status
            notes: Status update notes
            
        Returns:
            Dictionary with update result
        """
        if case_id not in self.cases:
            return {
                'success': False,
                'message': 'Case not found'
            }
        
        old_status = self.cases[case_id]['status']
        self.cases[case_id]['status'] = status
        self.cases[case_id]['updated_at'] = datetime.datetime.now().isoformat()
        
        # Log status change
        activity_note = f'Status changed from {old_status} to {status}'
        if notes:
            activity_note += f' - {notes}'
        
        self._log_activity(case_id, 'status_update', activity_note)
        
        return {
            'success': True,
            'message': f'Case status updated to {status}'
        }
    
    def add_case_note(self, case_id: str, note: str, 
                     author: str = 'system') -> Dict:
        """
        Add a note to a case
        
        Args:
            case_id: Unique case identifier
            note: Note content
            author: Note author
            
        Returns:
            Dictionary with result
        """
        if case_id not in self.cases:
            return {
                'success': False,
                'message': 'Case not found'
            }
        
        if case_id not in self.case_notes:
            self.case_notes[case_id] = []
        
        note_entry = {
            'note_id': f"note_{len(self.case_notes[case_id]) + 1}",
            'content': note,
            'author': author,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        self.case_notes[case_id].append(note_entry)
        
        self._log_activity(case_id, 'note_added', f'Note added by {author}')
        
        return {
            'success': True,
            'message': 'Note added successfully'
        }
    
    def set_case_goals(self, case_id: str, goals: List[Dict]) -> Dict:
        """
        Set goals for a case
        
        Args:
            case_id: Unique case identifier
            goals: List of goal dictionaries with 'description' and 'target_date'
            
        Returns:
            Dictionary with result
        """
        if case_id not in self.cases:
            return {
                'success': False,
                'message': 'Case not found'
            }
        
        formatted_goals = []
        for i, goal in enumerate(goals):
            formatted_goals.append({
                'goal_id': f"goal_{i + 1}",
                'description': goal.get('description', ''),
                'target_date': goal.get('target_date', ''),
                'status': 'not_started',
                'created_at': datetime.datetime.now().isoformat()
            })
        
        self.cases[case_id]['goals'] = formatted_goals
        
        self._log_activity(case_id, 'goals_set', 
                          f'Set {len(formatted_goals)} goals for case')
        
        return {
            'success': True,
            'goals': formatted_goals,
            'message': f'Set {len(formatted_goals)} goals'
        }
    
    def update_goal_status(self, case_id: str, goal_id: str, 
                          status: str) -> Dict:
        """
        Update status of a specific goal
        
        Args:
            case_id: Unique case identifier
            goal_id: Goal identifier
            status: New status (not_started, in_progress, completed, cancelled)
            
        Returns:
            Dictionary with result
        """
        if case_id not in self.cases:
            return {
                'success': False,
                'message': 'Case not found'
            }
        
        for goal in self.cases[case_id]['goals']:
            if goal['goal_id'] == goal_id:
                old_status = goal['status']
                goal['status'] = status
                goal['updated_at'] = datetime.datetime.now().isoformat()
                
                if status == 'completed':
                    goal['completed_at'] = datetime.datetime.now().isoformat()
                
                self._log_activity(case_id, 'goal_updated',
                                 f'Goal {goal_id} status: {old_status} -> {status}')
                
                return {
                    'success': True,
                    'message': f'Goal status updated to {status}'
                }
        
        return {
            'success': False,
            'message': 'Goal not found'
        }
    
    def track_progress(self, case_id: str, metric: str, value: any) -> Dict:
        """
        Track progress metrics for a case
        
        Args:
            case_id: Unique case identifier
            metric: Metric name
            value: Metric value
            
        Returns:
            Dictionary with result
        """
        if case_id not in self.cases:
            return {
                'success': False,
                'message': 'Case not found'
            }
        
        if metric not in self.cases[case_id]['progress_metrics']:
            self.cases[case_id]['progress_metrics'][metric] = []
        
        self.cases[case_id]['progress_metrics'][metric].append({
            'value': value,
            'recorded_at': datetime.datetime.now().isoformat()
        })
        
        return {
            'success': True,
            'message': f'Progress metric {metric} recorded'
        }
    
    def get_case_summary(self, case_id: str) -> Optional[Dict]:
        """
        Get comprehensive case summary
        
        Args:
            case_id: Unique case identifier
            
        Returns:
            Dictionary with case summary
        """
        if case_id not in self.cases:
            return None
        
        case = self.cases[case_id].copy()
        
        # Add notes
        case['notes'] = self.case_notes.get(case_id, [])
        
        # Add recent activities
        activities = self.case_activities.get(case_id, [])
        case['recent_activities'] = activities[-10:]  # Last 10 activities
        
        # Calculate progress
        total_goals = len(case.get('goals', []))
        completed_goals = sum(1 for g in case.get('goals', []) 
                            if g['status'] == 'completed')
        
        case['progress_percentage'] = (
            (completed_goals / total_goals * 100) if total_goals > 0 else 0
        )
        
        return case
    
    def get_client_cases(self, client_id: str, 
                        active_only: bool = False) -> List[Dict]:
        """
        Get all cases for a client
        
        Args:
            client_id: Unique client identifier
            active_only: If True, return only active cases
            
        Returns:
            List of cases
        """
        client_cases = [
            case for case in self.cases.values()
            if case['client_id'] == client_id
        ]
        
        if active_only:
            active_statuses = [CaseStatus.OPEN.value, CaseStatus.IN_PROGRESS.value]
            client_cases = [
                case for case in client_cases
                if case['status'] in active_statuses
            ]
        
        return client_cases
    
    def _log_activity(self, case_id: str, activity_type: str, 
                     description: str) -> None:
        """Log activity for a case"""
        activity = {
            'activity_id': f"act_{len(self.case_activities[case_id]) + 1}",
            'type': activity_type,
            'description': description,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.case_activities[case_id].append(activity)
    
    def generate_case_insights(self, case_id: str) -> Dict:
        """
        Generate intelligent insights about a case
        
        Args:
            case_id: Unique case identifier
            
        Returns:
            Dictionary with insights and recommendations
        """
        if case_id not in self.cases:
            return {
                'success': False,
                'message': 'Case not found'
            }
        
        case = self.cases[case_id]
        insights = {
            'case_id': case_id,
            'recommendations': [],
            'risk_factors': [],
            'success_indicators': []
        }
        
        # Analyze case age
        created = datetime.datetime.fromisoformat(case['created_at'])
        age_days = (datetime.datetime.now() - created).days
        
        if age_days > 90 and case['status'] == CaseStatus.OPEN.value:
            insights['risk_factors'].append(
                f'Case has been open for {age_days} days without progress'
            )
            insights['recommendations'].append(
                'Consider case review and priority escalation'
            )
        
        # Analyze goals
        goals = case.get('goals', [])
        if goals:
            completed = sum(1 for g in goals if g['status'] == 'completed')
            completion_rate = (completed / len(goals)) * 100
            
            if completion_rate >= 75:
                insights['success_indicators'].append(
                    f'High goal completion rate: {completion_rate:.0f}%'
                )
            elif completion_rate < 25 and age_days > 30:
                insights['risk_factors'].append(
                    f'Low goal completion rate: {completion_rate:.0f}%'
                )
                insights['recommendations'].append(
                    'Review goals and barriers to completion'
                )
        
        # Analyze priority vs. status
        if case['priority'] == CasePriority.CRITICAL.value:
            if case['status'] not in [CaseStatus.IN_PROGRESS.value, CaseStatus.RESOLVED.value]:
                insights['risk_factors'].append(
                    'Critical priority case not actively in progress'
                )
                insights['recommendations'].append(
                    'Immediate attention required for critical case'
                )
        
        return insights
