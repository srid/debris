# I keep utility and wrapper code here
# So simply do `from debris import foo' to use the feature `foo'

import os, cgi, sys, logging, re
from contextlib import contextmanager

from google.appengine.ext.webapp import template as gae_template
from google.appengine.api import users

from docutils import core


TEMPLATE_GROUP = 'srid' # /templates/srid/
def template(response, name, values):
    """Render the given template to the `response' object"""
    # find templates in ../templates/
    path = os.path.join(os.path.dirname(__file__),
                        '..',
                        'templates',
                        TEMPLATE_GROUP,
                        name)

    # Values common to all templates go here    
    values.update({
        'is_admin':    users.is_current_user_admin(),
        'login_url':   users.create_login_url("/"),
        'logout_url':  users.create_logout_url("/")
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
        
        # if __form_set_<key>__ is defined, use it instead of 'setattr'
        try:
            setter = getattr(model_instance, '__form_set_%s__' % key)
            field_value = value # need not to apply `field_type` as that will be done by the above custom setter
        except AttributeError:
            setter = lambda v: setattr(model_instance, key, v)
            field_value = field_type(value)
            
        setter(field_value)

def rst2html(text):
    parts = core.publish_parts(
        text,
        writer_name='html4css1',
        settings_overrides={
            '_disable_config': True,
            'embed_stylesheet': False,
            'stylesheet_path': 'data/html4css1/html4css1.css',
            'template': 'data/docutils/html4css1/template.txt'
        })
    return parts['fragment']
    
register = gae_template.create_template_register()
@register.filter
def rstify(text):
    return rst2html(text)
    
display_tag_re = re.compile('([a-z])([A-Z])')
@register.filter
def display_tag(tag):
    """Display tag in readable way.
    Eg: display_tag("GoogleAppEngine") = "Google App Engine"
    """
    return display_tag_re.sub(r'\1 \2', tag)
    
@register.filter
def display_tags(tag_list):
    tags = []
    for tag in tag_list:
        tags.append('<a href="/tag/%s">%s</a>' % (tag, display_tag(tag)))
    return ', '.join(tags)
    
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
