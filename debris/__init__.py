# I keep utility and wrapper code here
# So simply do `from debris import foo' to use the feature `foo'

import os, cgi, sys, logging
from contextlib import contextmanager

from google.appengine.ext.webapp import template as gae_template
from google.appengine.api import users

TEMPLATE_GROUP = 'srid' # /templates/srid/
def template(response, name, values):
    """Render the given template to the `response' object"""
    # find templates in ../templates/
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'templates',
                        TEMPLATE_GROUP,
                        name)
    
    # generate the greeting urls (login/logout)
    user = users.get_current_user()
    if user:
        greeting = "Welcome %s! <a href=\"%s\">Logout</a>" % \
                   (user.nickname(), users.create_logout_url("/"))
    else:
        greeting = "<a href=\"%s\">Login</a>" % users.create_login_url("/")
        
    values.update({
        'auth_greeting': greeting
    })
    response.out.write(gae_template.render(path, values))
    

def SHELL():
    """Break the application and run the PDB shell"""
    from pdb import Pdb
    Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__).set_trace(sys._getframe().f_back)

def form_to_db(request, model_instance):
    """Set table attributes from form values"""
    for key, field in model_instance.fields().items():
        value = request.get(key, default_value=None)
        
        field_type = field.data_type
        if field_type is basestring:
            field_type = str # basestring cannot be initiated
            
        # Skip fields that are not part of form (value == None), except in the
        # case of HTML checkbox where the corresponding form field in request.get
        # is 'absent by design' if the checkbox is unchecked
        # See http://code.google.com/appengine/docs/python/tools/webapp/requestdata.html
        # to understand how Google works around this HTML spec wart.
        if value == None and field_type is not bool:
            continue
        
        if value is not None:
            value = cgi.escape(value)
            
        field_value = field_type(value)
        setattr(model_instance, key, field_value)

def rst2html(text):
    from docutils import core
    parts = core.publish_parts(
        text,
        writer_name='html4css1',
        settings_overrides={
            '_disable_config': True,
            'embed_stylesheet': False,
            'stylesheet_path': 'static/html4css1/html4css1.css',
            'template': 'static/docutils/html4css1/template.txt'
        })
    return parts['fragment']
    
register = gae_template.create_template_register()
@register.filter
def rstify(text):
    return rst2html(text)
    
gae_template.register_template_library('debris') # this module itself


@contextmanager
def StringIO():
    """Add support for 'with' statement to StringIO - http://bugs.python.org/issue1286
    """
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
        
    sio = StringIO()
    
    try:
        yield sio
    finally:
        sio.close()
