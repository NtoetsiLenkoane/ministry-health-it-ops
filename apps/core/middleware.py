"""
Audit logging middleware
"""
from apps.core.models import AuditLog
from django.utils.deprecation import MiddlewareMixin


class AuditLogMiddleware(MiddlewareMixin):
    """Middleware to log user actions"""
    
    def process_request(self, request):
        # Capture request for later use
        request.start_time = __import__('time').time()
        return None
    
    def process_response(self, request, response):
        if request.user.is_authenticated:
            # Log certain actions
            if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                action = 'UPDATE'
                if request.method == 'POST':
                    action = 'CREATE'
                elif request.method == 'DELETE':
                    action = 'DELETE'
                
                try:
                    ip_address = self.get_client_ip(request)
                    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
                    
                    AuditLog.objects.create(
                        user=request.user,
                        action=action,
                        object_type=request.path.split('/')[1],
                        object_id='',
                        object_repr=request.path,
                        ip_address=ip_address,
                        user_agent=user_agent,
                    )
                except Exception:
                    pass  # Don't fail the request if logging fails
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
