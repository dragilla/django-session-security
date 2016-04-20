Quick setup
===========

The purpose of this documentation is to get you started as fast as possible,
because your time matters and you probably have other things to worry about.

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
    ...

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
