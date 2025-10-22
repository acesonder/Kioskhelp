"""
Self-Help Tools Module
Provides interactive tools for client self-assessment and support
"""

import datetime
from typing import Dict, List, Optional


class SelfHelpTools:
    """Collection of self-help tools for clients"""
    
    def __init__(self):
        self.tool_usage = {}
        self.saved_tools = {}
    
    def get_available_tools(self) -> List[Dict]:
        """Get list of all available self-help tools"""
        return [
            {
                'tool_id': 'budgeting',
                'name': 'Budget Planning Tool',
                'category': 'financial',
                'description': 'Create and manage your personal budget',
                'interactive': True
            },
            {
                'tool_id': 'housing_checklist',
                'name': 'Housing Search Checklist',
                'category': 'housing',
                'description': 'Track your housing search progress',
                'interactive': True
            },
            {
                'tool_id': 'wellness_tracker',
                'name': 'Wellness Tracker',
                'category': 'mental_health',
                'description': 'Track your daily wellness and mood',
                'interactive': True
            },
            {
                'tool_id': 'goal_planner',
                'name': 'Goal Planning Tool',
                'category': 'general',
                'description': 'Set and track personal goals',
                'interactive': True
            },
            {
                'tool_id': 'job_search_organizer',
                'name': 'Job Search Organizer',
                'category': 'employment',
                'description': 'Track job applications and interviews',
                'interactive': True
            },
            {
                'tool_id': 'crisis_plan',
                'name': 'Personal Crisis Plan',
                'category': 'mental_health',
                'description': 'Create a plan for mental health crises',
                'interactive': True
            },
            {
                'tool_id': 'resource_finder',
                'name': 'Community Resource Finder',
                'category': 'general',
                'description': 'Find resources based on your needs',
                'interactive': True
            }
        ]
    
    def use_budgeting_tool(self, client_id: str, income: float, 
                          expenses: Dict[str, float]) -> Dict:
        """
        Use the budgeting tool
        
        Args:
            client_id: Unique client identifier
            income: Monthly income
            expenses: Dictionary of expense categories and amounts
            
        Returns:
            Budget analysis and recommendations
        """
        total_expenses = sum(expenses.values())
        remaining = income - total_expenses
        
        analysis = {
            'tool_id': 'budgeting',
            'client_id': client_id,
            'income': income,
            'total_expenses': total_expenses,
            'remaining': remaining,
            'expense_breakdown': expenses,
            'recommendations': [],
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Generate recommendations
        if remaining < 0:
            analysis['recommendations'].append(
                f'Your expenses exceed income by ${abs(remaining):.2f}. '
                'Consider reviewing expenses for possible reductions.'
            )
        elif remaining < income * 0.1:
            analysis['recommendations'].append(
                'Your budget is tight. Consider building an emergency fund.'
            )
        else:
            analysis['recommendations'].append(
                f'You have ${remaining:.2f} available. '
                'Consider saving for emergencies or future goals.'
            )
        
        # Analyze expense categories
        for category, amount in expenses.items():
            percentage = (amount / income) * 100 if income > 0 else 0
            if percentage > 30 and category != 'housing':
                analysis['recommendations'].append(
                    f'{category.title()} is {percentage:.0f}% of income. '
                    'This seems high - consider if reductions are possible.'
                )
        
        self._log_tool_usage(client_id, 'budgeting', analysis)
        
        return {
            'success': True,
            'analysis': analysis,
            'message': 'Budget analysis completed'
        }
    
    def use_wellness_tracker(self, client_id: str, mood: int, 
                           sleep_hours: float, notes: str = '') -> Dict:
        """
        Track daily wellness
        
        Args:
            client_id: Unique client identifier
            mood: Mood rating (1-10)
            sleep_hours: Hours of sleep
            notes: Optional notes
            
        Returns:
            Wellness entry
        """
        entry = {
            'tool_id': 'wellness_tracker',
            'client_id': client_id,
            'mood': mood,
            'sleep_hours': sleep_hours,
            'notes': notes,
            'date': datetime.datetime.now().date().isoformat(),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Generate insights
        insights = []
        if mood <= 3:
            insights.append(
                'Your mood is quite low. Consider reaching out to support services.'
            )
        if sleep_hours < 6:
            insights.append(
                'You may not be getting enough sleep. Good sleep is important for wellbeing.'
            )
        elif sleep_hours > 10:
            insights.append(
                'You may be sleeping more than usual. Consider discussing with healthcare provider.'
            )
        
        entry['insights'] = insights
        
        self._log_tool_usage(client_id, 'wellness_tracker', entry)
        
        return {
            'success': True,
            'entry': entry,
            'message': 'Wellness entry recorded'
        }
    
    def use_goal_planner(self, client_id: str, goal: str, 
                        steps: List[str], target_date: str) -> Dict:
        """
        Create a goal plan
        
        Args:
            client_id: Unique client identifier
            goal: Goal description
            steps: List of steps to achieve goal
            target_date: Target completion date
            
        Returns:
            Goal plan
        """
        plan = {
            'tool_id': 'goal_planner',
            'client_id': client_id,
            'goal': goal,
            'steps': [
                {
                    'step_number': i + 1,
                    'description': step,
                    'completed': False
                }
                for i, step in enumerate(steps)
            ],
            'target_date': target_date,
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'active'
        }
        
        self._log_tool_usage(client_id, 'goal_planner', plan)
        
        return {
            'success': True,
            'plan': plan,
            'message': 'Goal plan created'
        }
    
    def use_job_search_organizer(self, client_id: str, 
                                company: str, position: str,
                                application_date: str, status: str) -> Dict:
        """
        Track job application
        
        Args:
            client_id: Unique client identifier
            company: Company name
            position: Position applied for
            application_date: Date of application
            status: Application status
            
        Returns:
            Application entry
        """
        entry = {
            'tool_id': 'job_search_organizer',
            'client_id': client_id,
            'company': company,
            'position': position,
            'application_date': application_date,
            'status': status,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        self._log_tool_usage(client_id, 'job_search_organizer', entry)
        
        return {
            'success': True,
            'entry': entry,
            'message': 'Job application tracked'
        }
    
    def create_crisis_plan(self, client_id: str, warning_signs: List[str],
                          coping_strategies: List[str], 
                          support_contacts: List[Dict]) -> Dict:
        """
        Create a personal crisis plan
        
        Args:
            client_id: Unique client identifier
            warning_signs: List of warning signs
            coping_strategies: List of coping strategies
            support_contacts: List of support contact dictionaries
            
        Returns:
            Crisis plan
        """
        plan = {
            'tool_id': 'crisis_plan',
            'client_id': client_id,
            'warning_signs': warning_signs,
            'coping_strategies': coping_strategies,
            'support_contacts': support_contacts,
            'emergency_numbers': [
                {'service': 'Crisis Hotline', 'number': '988'},
                {'service': 'Emergency Services', 'number': '911'}
            ],
            'created_at': datetime.datetime.now().isoformat()
        }
        
        self._save_tool_data(client_id, 'crisis_plan', plan)
        
        return {
            'success': True,
            'plan': plan,
            'message': 'Crisis plan created and saved'
        }
    
    def _log_tool_usage(self, client_id: str, tool_id: str, data: Dict) -> None:
        """Log tool usage"""
        if client_id not in self.tool_usage:
            self.tool_usage[client_id] = []
        
        usage_entry = {
            'tool_id': tool_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'data': data
        }
        
        self.tool_usage[client_id].append(usage_entry)
    
    def _save_tool_data(self, client_id: str, tool_id: str, data: Dict) -> None:
        """Save tool data for future access"""
        if client_id not in self.saved_tools:
            self.saved_tools[client_id] = {}
        
        self.saved_tools[client_id][tool_id] = data
    
    def get_tool_history(self, client_id: str, tool_id: Optional[str] = None) -> List[Dict]:
        """
        Get tool usage history for a client
        
        Args:
            client_id: Unique client identifier
            tool_id: Optional specific tool ID
            
        Returns:
            List of tool usage entries
        """
        if client_id not in self.tool_usage:
            return []
        
        history = self.tool_usage[client_id]
        
        if tool_id:
            history = [entry for entry in history if entry['tool_id'] == tool_id]
        
        return history
    
    def get_saved_tool_data(self, client_id: str, tool_id: str) -> Optional[Dict]:
        """Get saved data for a specific tool"""
        if client_id not in self.saved_tools:
            return None
        
        return self.saved_tools[client_id].get(tool_id)
