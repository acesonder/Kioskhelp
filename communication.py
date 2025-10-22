"""
Communication Module
Handles client communication and messaging
"""

import datetime
from typing import Dict, List, Optional


class CommunicationSystem:
    """Manages client communication and notifications"""
    
    def __init__(self):
        self.messages = {}
        self.notifications = {}
    
    def send_message(self, client_id: str, message_type: str, 
                    content: str, method: str = 'email') -> Dict:
        """
        Send a message to a client
        
        Args:
            client_id: Unique client identifier
            message_type: Type of message (appointment, update, resource, etc.)
            content: Message content
            method: Delivery method (email, sms, app)
            
        Returns:
            Dictionary with send result
        """
        message_id = f"msg_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        message = {
            'message_id': message_id,
            'client_id': client_id,
            'type': message_type,
            'content': content,
            'method': method,
            'sent_at': datetime.datetime.now().isoformat(),
            'status': 'sent',
            'read': False
        }
        
        if client_id not in self.messages:
            self.messages[client_id] = []
        
        self.messages[client_id].append(message)
        
        return {
            'success': True,
            'message_id': message_id,
            'message': f'Message sent via {method}'
        }
    
    def get_client_messages(self, client_id: str, 
                           unread_only: bool = False) -> List[Dict]:
        """
        Get messages for a client
        
        Args:
            client_id: Unique client identifier
            unread_only: If True, return only unread messages
            
        Returns:
            List of messages
        """
        if client_id not in self.messages:
            return []
        
        messages = self.messages[client_id]
        
        if unread_only:
            messages = [m for m in messages if not m['read']]
        
        return messages
    
    def mark_message_read(self, client_id: str, message_id: str) -> Dict:
        """Mark a message as read"""
        if client_id not in self.messages:
            return {
                'success': False,
                'message': 'No messages found for client'
            }
        
        for msg in self.messages[client_id]:
            if msg['message_id'] == message_id:
                msg['read'] = True
                msg['read_at'] = datetime.datetime.now().isoformat()
                return {
                    'success': True,
                    'message': 'Message marked as read'
                }
        
        return {
            'success': False,
            'message': 'Message not found'
        }
    
    def create_notification(self, client_id: str, notification_type: str,
                          title: str, content: str, priority: str = 'normal') -> Dict:
        """
        Create a notification for a client
        
        Args:
            client_id: Unique client identifier
            notification_type: Type of notification
            title: Notification title
            content: Notification content
            priority: Priority level (low, normal, high, urgent)
            
        Returns:
            Dictionary with notification information
        """
        notification_id = f"notif_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        notification = {
            'notification_id': notification_id,
            'client_id': client_id,
            'type': notification_type,
            'title': title,
            'content': content,
            'priority': priority,
            'created_at': datetime.datetime.now().isoformat(),
            'read': False,
            'dismissed': False
        }
        
        if client_id not in self.notifications:
            self.notifications[client_id] = []
        
        self.notifications[client_id].append(notification)
        
        return {
            'success': True,
            'notification_id': notification_id,
            'message': 'Notification created'
        }
    
    def get_notifications(self, client_id: str, active_only: bool = True) -> List[Dict]:
        """Get notifications for a client"""
        if client_id not in self.notifications:
            return []
        
        notifications = self.notifications[client_id]
        
        if active_only:
            notifications = [n for n in notifications if not n['dismissed']]
        
        return notifications
    
    def dismiss_notification(self, client_id: str, notification_id: str) -> Dict:
        """Dismiss a notification"""
        if client_id not in self.notifications:
            return {
                'success': False,
                'message': 'No notifications found for client'
            }
        
        for notif in self.notifications[client_id]:
            if notif['notification_id'] == notification_id:
                notif['dismissed'] = True
                notif['dismissed_at'] = datetime.datetime.now().isoformat()
                return {
                    'success': True,
                    'message': 'Notification dismissed'
                }
        
        return {
            'success': False,
            'message': 'Notification not found'
        }


class AppointmentScheduler:
    """Manages client appointments with service providers"""
    
    def __init__(self):
        self.appointments = {}
    
    def schedule_appointment(self, client_id: str, provider_id: str,
                           appointment_type: str, date_time: str, 
                           notes: str = '') -> Dict:
        """
        Schedule an appointment for a client
        
        Args:
            client_id: Unique client identifier
            provider_id: Service provider identifier
            appointment_type: Type of appointment
            date_time: Appointment date and time (ISO format)
            notes: Additional notes
            
        Returns:
            Dictionary with appointment information
        """
        appointment_id = f"appt_{client_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        appointment = {
            'appointment_id': appointment_id,
            'client_id': client_id,
            'provider_id': provider_id,
            'type': appointment_type,
            'scheduled_time': date_time,
            'status': 'scheduled',
            'notes': notes,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        self.appointments[appointment_id] = appointment
        
        return {
            'success': True,
            'appointment_id': appointment_id,
            'appointment': appointment,
            'message': 'Appointment scheduled successfully'
        }
    
    def get_client_appointments(self, client_id: str, 
                               upcoming_only: bool = False) -> List[Dict]:
        """Get appointments for a client"""
        client_appointments = [
            appt for appt in self.appointments.values()
            if appt['client_id'] == client_id
        ]
        
        if upcoming_only:
            now = datetime.datetime.now().isoformat()
            client_appointments = [
                appt for appt in client_appointments
                if appt['scheduled_time'] > now and appt['status'] == 'scheduled'
            ]
        
        return client_appointments
    
    def update_appointment_status(self, appointment_id: str, 
                                 status: str) -> Dict:
        """
        Update appointment status
        
        Args:
            appointment_id: Unique appointment identifier
            status: New status (scheduled, confirmed, completed, cancelled, no_show)
            
        Returns:
            Dictionary with update result
        """
        if appointment_id not in self.appointments:
            return {
                'success': False,
                'message': 'Appointment not found'
            }
        
        self.appointments[appointment_id]['status'] = status
        self.appointments[appointment_id]['updated_at'] = datetime.datetime.now().isoformat()
        
        return {
            'success': True,
            'message': f'Appointment status updated to {status}'
        }
    
    def send_appointment_reminder(self, appointment_id: str, 
                                 communication_system: CommunicationSystem) -> Dict:
        """Send appointment reminder to client"""
        if appointment_id not in self.appointments:
            return {
                'success': False,
                'message': 'Appointment not found'
            }
        
        appointment = self.appointments[appointment_id]
        
        content = f"Reminder: You have an appointment scheduled for {appointment['scheduled_time']}. Type: {appointment['type']}"
        
        result = communication_system.send_message(
            client_id=appointment['client_id'],
            message_type='appointment_reminder',
            content=content
        )
        
        return result
