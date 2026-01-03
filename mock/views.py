"""
Mock представления для тестирования контроля доступа.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from access.permissions import HasResourcePermission


class ProjectsPermission(HasResourcePermission):
    """Класс разрешений для ресурса projects."""
    resource_name = 'projects'
    action_name = 'read'


class ReportsPermission(HasResourcePermission):
    """Класс разрешений для ресурса reports."""
    resource_name = 'reports'
    action_name = 'read'


@api_view(['GET'])
@permission_classes([IsAuthenticated, ProjectsPermission])
def mock_projects(request):
    """Mock endpoint для ресурса projects."""
    mock_data = [
        {
            'id': 1,
            'name': 'Project Alpha',
            'description': 'First project',
            'status': 'active',
            'created_at': '2024-01-15T10:00:00Z'
        },
        {
            'id': 2,
            'name': 'Project Beta',
            'description': 'Second project',
            'status': 'in_progress',
            'created_at': '2024-01-20T14:30:00Z'
        },
        {
            'id': 3,
            'name': 'Project Gamma',
            'description': 'Third project',
            'status': 'completed',
            'created_at': '2024-01-25T09:15:00Z'
        }
    ]
    return Response({
        'message': 'Access granted to projects',
        'data': mock_data,
        'count': len(mock_data)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ReportsPermission])
def mock_reports(request):
    """Mock endpoint для ресурса reports."""
    mock_data = [
        {
            'id': 1,
            'title': 'Monthly Report January',
            'type': 'monthly',
            'generated_at': '2024-01-31T23:59:59Z',
            'file_url': '/reports/monthly-2024-01.pdf'
        },
        {
            'id': 2,
            'title': 'Quarterly Report Q1',
            'type': 'quarterly',
            'generated_at': '2024-03-31T23:59:59Z',
            'file_url': '/reports/quarterly-2024-q1.pdf'
        }
    ]
    return Response({
        'message': 'Access granted to reports',
        'data': mock_data,
        'count': len(mock_data)
    }, status=status.HTTP_200_OK)
