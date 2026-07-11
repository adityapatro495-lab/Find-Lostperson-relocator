from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Role-based access control for the administrator dashboard.
    See Project Report Appendix G.3 and Section 4.3.5."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, 'userprofile', None)
        if not request.user.is_authenticated or not profile or profile.role != 'ADMIN':
            raise PermissionDenied('Administrator access required.')
        return view_func(request, *args, **kwargs)
    return wrapper
