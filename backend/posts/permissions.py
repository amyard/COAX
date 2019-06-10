from rest_framework import permissions

from backend.common.utils import get_ip_from_request
from backend.posts.models import IpAccess


class IpAccessPermission(permissions.BasePermission):
    message = 'Sorry, you don\'t have permissions to view this page'

    def has_permission(self, request, view):
        ip_addr = get_ip_from_request(request)
        if IpAccess.objects.filter(ip = ip_addr).exists():
            return True
        return False