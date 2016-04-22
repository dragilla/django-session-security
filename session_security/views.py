""" One view method for AJAX requests by SessionSecurity objects. """
import time

from datetime import datetime, timedelta

from annoying.decorators import render_to
from django.contrib import auth
from django.views import generic
from django import http
from django.middleware.csrf import rotate_token, get_token

from .utils import get_last_activity

__all__ = ['PingView', ]


class PingView(generic.View):
    """
    This view is just in charge of returning the number of seconds since the
    'real last activity' that is maintained in the session by the middleware.
    """

    def get(self, request, *args, **kwargs):
        if '_session_security' not in request.session:
            # It probably has expired already
            return http.HttpResponse('logout')

        last_activity = get_last_activity(request.session)
        inactive_for = (datetime.now() - last_activity).seconds
        return http.HttpResponse(inactive_for)


@render_to('session_security/after_relogin.html')
def session_security_after_relogin(request):
    rotate_token(request)
    return {
        'token': get_token(request),
        'relogin': request.session.get('relogin'),
        'warn_after': request.session.get('warn_after'),
        'expire_after': request.session.get('expire_after')
    }
