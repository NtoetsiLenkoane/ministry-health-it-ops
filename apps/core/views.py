from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone


def index(request):
    """Home page"""
    if request.user.is_authenticated:
        return dashboard(request)
    return render(request, 'index.html')


@login_required
def dashboard(request):
    """Main dashboard"""
    # Import models dynamically to avoid circular imports
    from apps.assets.models import Asset
    from apps.helpdesk.models import HelpDeskTicket, TicketStatus
    from apps.visitors.models import Visitor
    
    # Get statistics
    total_assets = Asset.objects.filter(is_active=True).count()
    assets_in_maintenance = Asset.objects.filter(
        condition__name='Maintenance',
        is_active=True
    ).count()
    
    open_tickets = HelpDeskTicket.objects.filter(
        status__name__in=['Open', 'Assigned', 'In Progress'],
        is_active=True
    ).count()
    
    closed_tickets = HelpDeskTicket.objects.filter(
        status__name='Closed',
        is_active=True
    ).count()
    
    today_visitors = Visitor.objects.filter(
        check_in_date=timezone.now().date()
    ).count()
    
    context = {
        'total_assets': total_assets,
        'assets_in_maintenance': assets_in_maintenance,
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'today_visitors': today_visitors,
    }
    
    return render(request, 'dashboard.html', context)


@require_http_methods(['GET'])
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Ministry of Health IT Operations System is operational'
    })
