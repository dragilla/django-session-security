.. image:: https://secure.travis-ci.org/yourlabs/django-session-security.png?branch=master

This app provides a mechanism to logout inactive authenticated users. An
inactive browser should be logged out automatically if the user left his
workstation, to protect sensitive data that may be displayed in the browser. It
may be useful for CRMs, intranets, and such projects.
In addition this app lets you log in again and continue your work where you left 
off.

For example, if the user leaves for a coffee break, this app can force logout
after say 5 minutes of inactivity.

Why not just set the session to expire after X minutes ?
--------------------------------------------------------

Or "Why does this app even exist" ? Here are the reasons:

- if the user session expires before the user is done reading a page: he will
  have to login again.
- if the user session expires before the user is done filling a form: his work
  will be lost, and he will have to login again, and probably yell at you, dear
  django dev ... at least I know I would !

This app allows to short circuit those limitations in session expiry.

How does it work ?
------------------

When the user loads a page, SessionSecurity middleware will set the last
activity to now. The last activity is stored as datetime
in ``request.session['_session_security']``. To avoid having the middleware
update that last activity datetime for a URL, add the url to
``settings.SESSION_SECURITY_PASSIVE_URLS``.

When the user moves mouse, click, scroll or press a key, SessionSecurity will
save the DateTime as a JavaScript attribute. It will send the number of seconds
since when the last user activity was recorded to PingView, next time it should
ping.

First, a warning should be shown after ``settings.SESSION_SECURITY_WARN_AFTER``
seconds. The warning displays a text like "Your session is about to expire,
move the mouse to extend it".

Before displaying this warning, SessionSecurity will upload the time since the
last client-side activity was recorded. The middleware will take it if it is
shorter than what it already has - ie. another more recent activity was
detected in another browser tab. The PingView will respond with the number of
seconds since the last activity - all browser tab included.

If there was no other, more recent, activity recorded by the server: it will
show the warning. Otherwise it will update the last activity in javascript from
the PingView response.

Same goes to expire after ``settings.SESSION_SECURITY_EXPIRE_AFTER`` seconds.
Javascript will first make an ajax request to PingView to ensure that another
more recent activity was not detected anywhere else - in any other browser tab.

If the app is configured to let the user login again after session timeout (to 
continue his work) then pre-logout the user session is backuped up and restored
quickly after logout. This way he can continue his work as if the session never
expired. For the relogin mechanism the same login action (view and template) is
used as for normal login. The login window opens on top of the working application. The
user operates on it normally - using same security mechanisms as with the normal
login. Then after login the modal window is closed.

How to install ?
----------------
Install the package::

    pip install -e git+git://github.com/dragilla/django-session-security.git@beta#egg=django-session-security==master

For static file service, add to ``settings.INSTALLED_APPS``::

    'session_security',

Add to ``settings.MIDDLEWARE_CLASSES``, **after** django's AuthenticationMiddleware::

    'session_security.middleware.SessionSecurityMiddleware',

Ensure settings.TEMPLATE_CONTEXT_PROCESSORS has::

    'django.core.context_processors.request'

Add to urls::

    url(r'session_security/', include('session_security.urls')),

Duplicate your login action in urls to allow an extra parameter (relogin)::

    ...
    url(r'^login/$', 'my_login', name='login'),
    url(r'^login/(?P<relogin>\d+)$', 'my_login', name='login'),

Add extra option to you login view::

    def my_login(request, relogin=0):
    ...
    
Pass this extra parameter to template::
  
    return {
        ...
        'relogin': relogin,
    }
    
After successful login in your view, redirect the user to close the modal window::
    
    if the_user_has_logged_in_correctly:
        if relogin == '1':
            return redirect('session_security_after_relogin')
        ...
    
At this point, we're going to assume that you have `django.contrib.staticfiles
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ working.
This means that `static files are automatically served with runserver
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#runserver>`_,
and that you have to run `collectstatic when using another server
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic>`_
(fastcgi, uwsgi, and whatnot). If you don't use django.contrib.staticfiles,
then you're on your own to manage staticfiles.

After jQuery, add to your base template::
    
    {% url 'my_app:my_login' as post_url %}
    {% include 'session_security/all.html' with post_url=post_url %}

Requirements
------------

- Python 2.7 or 3
- jQuery 1.7+
- Django 1.4+
- django.contrib.staticfiles or django-staticfiles (included in Pinax) or
  you're on your own

Resources
---------

- `Git graciously hosted
  <https://github.com/dragilla/django-session-security/>`_ by `GitHub
  <http://github.com>`_,
