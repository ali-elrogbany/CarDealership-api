from rest_framework.permissions import BasePermission

class IsManagerOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.method == 'POST'):
            return True
        elif request.user:
            if (request.user.is_authenticated) and ('Manager' in request.user.groups.values_list('name',flat = True)):
                return True
        return False